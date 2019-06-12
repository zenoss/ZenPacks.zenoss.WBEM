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

import re

from twisted.internet import ssl, reactor, defer
from twisted.internet.error import TimeoutError
from twisted.python import failure

from zope.component import adapts
from zope.interface import implements

from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import RRDDataSourceInfo
from Products.Zuul.interfaces import IRRDDataSourceInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource \
    import PythonDataSource, PythonDataSourcePlugin

from ZenPacks.zenoss.WBEM.utils import (
    addLocalLibPath,
)

addLocalLibPath()

CIM_CLASSNAME = re.compile(r'from\s+([\w_]+)', re.I)


def get_classname(query):
    """Extract class name from a CQL query"""
    match = CIM_CLASSNAME.findall(query)
    return match[0] if match else ''


def string_to_lines(string):
    if isinstance(string, (list, tuple)):
        return string
    elif hasattr(string, 'splitlines'):
        return string.splitlines()

    return None


class WBEMDataSource(PythonDataSource):
    """Datasource used to capture datapoints from WBEM providers."""

    ZENPACKID = 'ZenPacks.zenoss.WBEM'

    sourcetypes = ('WBEM',)
    sourcetype = sourcetypes[0]

    plugin_classname = 'ZenPacks.zenoss.WBEM.dsplugins.WBEMDataSourcePlugin'

    namespace = ''
    query_language = 'CQL'  # hard-coded for now.
    query = ''
    result_component_key = ''
    result_component_value = ''
    result_timestamp_key = ''

    _properties = PythonDataSource._properties + (
        {'id': 'namespace', 'type': 'string'},
        {'id': 'query_language', 'type': 'string'},
        {'id': 'query', 'type': 'lines'},
        {'id': 'result_component_key', 'type': 'string'},
        {'id': 'result_component_value', 'type': 'string'},
        {'id': 'result_timestamp_key', 'type': 'string'},
        )


class IWBEMDataSourceInfo(IRRDDataSourceInfo):
    cycletime = schema.TextLine(
        title=_t(u'Cycle Time (seconds)'))

    namespace = schema.TextLine(
        group=_t('WBEM'),
        title=_t('Namespace'))

    query = schema.Text(
        group=_t(u'WBEM'),
        title=_t('CQL Query'),
        xtype='twocolumntextarea')

    result_component_key = schema.TextLine(
        group=_t(u'WBEM Results'),
        title=_t(u'Result Component Key'))

    result_component_value = schema.TextLine(
        group=_t(u'WBEM Results'),
        title=_t(u'Result Component Value'))

    result_timestamp_key = schema.TextLine(
        group=_t(u'WBEM Results'),
        title=_t(u'Result Timestamp Key'))


class WBEMDataSourceInfo(RRDDataSourceInfo):
    implements(IWBEMDataSourceInfo)
    adapts(WBEMDataSource)

    testable = False

    cycletime = ProxyProperty('cycletime')

    namespace = ProxyProperty('namespace')
    result_component_key = ProxyProperty('result_component_key')
    result_component_value = ProxyProperty('result_component_value')
    result_timestamp_key = ProxyProperty('result_timestamp_key')

    @property
    def query(self):
        return "\n".join(self._object.query)

    @query.setter
    def query(self, val):
        self._object.query = string_to_lines(val)


def add_timeout(factory, seconds):
    """Return new Deferred that will errback TimeoutError after seconds."""
    deferred_with_timeout = defer.Deferred()
    deferred = factory.deferred

    def fire_timeout():
        deferred.cancel()
        if not deferred_with_timeout.called:
            deferred_with_timeout.errback(failure.Failure(TimeoutError()))

    delayed_timeout = reactor.callLater(seconds, fire_timeout)
    factory.deferred_timeout = delayed_timeout

    def handle_result(result):
        if delayed_timeout.active():
            delayed_timeout.cancel()

        if not deferred_with_timeout.called:
            if isinstance(result, failure.Failure):
                deferred_with_timeout.errback(result)
            else:
                deferred_with_timeout.callback(result)

    deferred.addBoth(handle_result)
    return deferred_with_timeout
