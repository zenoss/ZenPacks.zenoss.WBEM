##############################################################################
#
# Copyright (C) Zenoss, Inc. 2017,2018 all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import logging
log = logging.getLogger('zen.WBEM')

from twisted.internet import defer
from twisted.python import failure

from Products.ZenEvents import ZenEventClasses
from Products.ZenUtils.Utils import prepId

from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource import PythonDataSourcePlugin

from ZenPacks.zenoss.WBEM import dependencies
dependencies.import_wbem_libs()

from pywbem import CIMDateTime
from pywbem.twisted_agent import (
    ExecQuery,
    OpenEnumerateInstances,
)

from ZenPacks.zenoss.WBEM.utils import (
    result_errmsg,
    convert_to_timestamp,
)

class WBEMDataSourcePlugin(PythonDataSourcePlugin):
    proxy_attributes = (
        'zWBEMPort',
        'zWBEMUsername',
        'zWBEMPassword',
        'zWBEMUseSSL',
        'zWBEMRequestTimeout',
        'zWBEMMaxObjectCount',
        'zWBEMOperationTimeout',
    )

    @classmethod
    def config_key(cls, datasource, context):
        params = cls.params(datasource, context)
        query = params.get('query', '')
        if context.zWBEMMaxObjectCount <= 0:
            return (
                context.device().id,
                datasource.getCycleTime(context),
                datasource.rrdTemplate().id,
                datasource.id,
                datasource.plugin_classname,
                params.get('namespace'),
                params.get('query_language'),
                query,
            )

        return (
            context.device().id,
            datasource.getCycleTime(context),
            datasource.plugin_classname,
            params.get('namespace'),
            params.get('query_language'),
            get_classname(query),
        )

    @classmethod
    def params(cls, datasource, context):
        params = {}

        params['namespace'] = datasource.talesEval(
            datasource.namespace, context)

        params['query_language'] = datasource.query_language
        params['query'] = datasource.talesEval(
            ' '.join(string_to_lines(datasource.query)), context)

        params['result_component_key'] = datasource.talesEval(
            datasource.result_component_key, context).replace(' ', '')

        params['result_component_value'] = datasource.talesEval(
            datasource.result_component_value, context).replace(' ', '')

        params['result_timestamp_key'] = datasource.talesEval(
            datasource.result_timestamp_key, context)

        params['classname'] = get_classname(params['query'])

        return params

    def collect(self, config):

        ds0 = config.datasources[0]

        credentials = (ds0.zWBEMUsername, ds0.zWBEMPassword)

        if ds0.zWBEMMaxObjectCount > 0:
            property_filter = ds0.params.get('property_filter', (None, None))
            factory = OpenEnumerateInstances(
                credentials,
                namespace=ds0.params['namespace'],
                classname=ds0.params['classname'],
                host=config.manageIp,
                port=ds0.zWBEMPort,
                ssl=ds0.zWBEMUseSSL,
                MaxObjectCount=ds0.zWBEMMaxObjectCount,
                OperationTimeout=ds0.zWBEMOperationTimeout,
                PropertyFilter=property_filter,
                ResultComponentKey=ds0.params['result_component_key']
            )
            factory.deferred.addCallback(
                check_if_complete, ds0,
                ds0.params['namespace'],
                ds0.params['classname'],
                PropertyFilter=property_filter,
                ResultComponentKey=ds0.params['result_component_key']
            )
        else:
            factory = ExecQuery(
                credentials,
                ds0.params['query_language'],
                ds0.params['query'],
                config.manageIp,
                ds0.zWBEMPort,
                ds0.zWBEMUseSSL,
                namespace=ds0.params['namespace'])

        return add_timeout(factory, ds0.zWBEMRequestTimeout)

    def onSuccess(self, results, config):
        data = self.new_data()
        ds0 = config.datasources[0]

        if not isinstance(results, list):
            results = [results]

        log.debug('Monitoring template name: {}'.format(ds0.template))
        log.debug('Monitoring query: {}'.format(ds0.params['query']))
        for instance in results:
            try:
                log.debug('Monitoring result: {0}'.format(instance.__dict__))
            except AttributeError:
                log.debug('Monitoring result is empty')

        # Convert datasources to a dictionary with result_component_value as
        # the key. This allows us to avoid an inner loop below.
        datasources = dict(
            (x.params.get('result_component_value', ''), x) \
            for x in config.datasources)

        result_component_key = \
            ds0.params['result_component_key']

        for result in results:
            result_key_value = None

            if result_component_key:
                result_component_keys = result_component_key.split(',')
                if len(result_component_keys) > 1:
                    result_key_value = ",".join([result[key] for key in result_component_keys])
                    datasource = datasources.get(result_key_value)
                else:
                    result_key_value = result[result_component_key]
                    datasource = datasources.get(result_key_value)

                if not datasource:
                    log.debug("No datasource for result: %r", result.items())
                    continue

            else:
                datasource = ds0

            if result_key_value:
                result_component_value = datasource.params.get(
                    'result_component_value')

                if result_component_value != result_key_value:
                    continue

            component_id = prepId(datasource.component)

            # Determine the timestamp that the value was collected.
            result_timestamp_key = datasource.params.get(
                'result_timestamp_key')

            timestamp = None

            if result_timestamp_key and result_timestamp_key in result:
                cim_date = result[result_timestamp_key]
                timestamp = convert_to_timestamp(cim_date)

            if not timestamp:
                timestamp = 'N'

            for datapoint in datasource.points:
                if datapoint.id in result:
                    value = result[datapoint.id]
                    if isinstance(value, CIMDateTime):
                        value = convert_to_timestamp(value)
                    data['values'][component_id][datapoint.id] = \
                        (value, timestamp)

        data['events'].append({
            'eventClassKey': 'wbemCollectionSuccess',
            'eventKey': 'wbemCollection',
            'summary': 'WBEM: successful collection',
            'device': config.id,
            'eventClass': ds0.eventClass,
            'severity': ZenEventClasses.Clear
        })

        return data

    def onError(self, result, config):
        errmsg = 'WBEM: %s' % result_errmsg(result)
        ds0 = config.datasources[0]

        if isinstance(result, failure.Failure) and isinstance(result.value, defer.CancelledError):
            errmsg = 'WBEM: %s' % 'request time exceeds value of zWBEMRequestTimeout'

        log.error('%s %s', config.id, errmsg)

        data = self.new_data()
        data['events'].append({
            'eventClassKey': 'wbemCollectionError',
            'eventKey': 'wbemCollection',
            'summary': errmsg,
            'device': config.id,
            'severity': ds0.severity,
            'eventClass': ds0.eventClass
        })

        return data
