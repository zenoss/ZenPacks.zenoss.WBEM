##############################################################################
#
# Copyright (C) Zenoss, Inc. 2012, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
import collections
import logging
log = logging.getLogger('zen.WBEMParser')
from ZenPacks.zenoss.WBEM.utils import result_errmsg


class WBEMParser(object):
    '''Parser for WBEM XML output'''

    @staticmethod
    def find_item(items, key, value):
        ''' return dictionary based on tag given a
            list of dictionaries
        '''
        if not isinstance(items, list):
            log.warn('find_item only accepts list: {}'.format(items))
            return
        for i in items:
            if i.get(key) == value:
                return i
        return

    @staticmethod
    def get_merged_items(items):
        '''return list of dictionaries'''
        output = []
        if not isinstance(items, list):
            log.warn('get_merged_items only accepts list: {}'.format(items))
            return output
        for i in items:
            if not isinstance(i, dict):
                log.warn('get_merged_items cannot parse non-dict item: {}'.format(i))
                continue
            vals = i.values()
            if len(vals) == 0:
                log.warn('get_merged_items found empty dict: {}'.format(i))
                continue
            if len(vals) > 1:
                log.warn('get_merged_items found multiple entries for: {}'.format(i))
                continue
            try:
                merged = WBEMParser.get_merged(vals[0])
                output.append(merged)
            except Exception as e:
                log.warn('Error ({}) occurred while parsing {} ({})'.format(e, i, vals[0]))
        return output

    @staticmethod
    def get_merged(items):
        '''return recursively merged dictionnary'''
        def merge_dict(target, source):
            for k, v in source.items():
                if (k in target and isinstance(target[k], dict)
                        and isinstance(source[k], collections.Mapping)):
                    merge_dict(target[k], source[k])
                else:
                    target[k] = source[k]
        new = {}
        for i in items:
            if not isinstance(i, dict):
                continue
            merge_dict(new, i)
        return new
    @staticmethod
    def find_single(input, id, value_only=True):
        '''Search through results and return if match found'''
        found = WBEMParser.get_recursively(input, str(id), value_only=value_only)
        if found is not None and len(found) == 1:
            return found[0]

    @staticmethod
    def get_datapoint_value(result, comp_id, ds_id, dp_id):
        '''Attempt to traverse results and return output'''
        # if component id is provided, then first attempt to filter results for it
        if comp_id is not None:
            # first try finding the single result
            comp_found = WBEMParser.find_single(result, comp_id, True)
            if comp_found is not None:
                # return a number if we found one
                try:
                    test = float(comp_found)
                    return comp_found
                # otherwise maybe this is just an index?
                except ValueError:
                    comp_found = WBEMParser.find_single(result, comp_id, False)
                    if comp_found is not None:
                        result = comp_found
                except Exception as e:
                    raise e
            else:
                # otherwise try narrowing our results
                comp_found = WBEMParser.find_single(result, comp_id, False)
                if comp_found is not None:
                    result = comp_found

        # try finding a single result for our dp
        dp_found = WBEMParser.find_single(result, dp_id, True)
        if dp_found is not None:
            return dp_found

        # otherwise try narrowing further by datasource id
        ds_found = WBEMParser.find_single(result, ds_id, True)
        if ds_found is not None:
            result = ds_found

        # before trying to find the datapoint once more
        dp_found = WBEMParser.find_single(result, dp_id, True)
        if dp_found is not None:
            return dp_found

        return None

    @staticmethod
    def get_recursively(search_dict, field, match_key=True, match_value=True, value_only=False):
        """
            Return list of recursive dictionary search results.
            Optionally match field by key or value
            Optionally return either list of dictonaries or other objects
        """
        def add_to(key, value):
            found = []
            if match_key and key == field:
                if value_only:
                    found.append(value)
                else:
                    found.append(search_dict)
            elif match_value and value == field:
                if value_only:
                    found.append(key)
                else:
                    found.append(search_dict)
            return found

        fields_found = []

        for key, value in search_dict.iteritems():
            fields_found.extend(add_to(key, value))

            if isinstance(value, dict):
                fields_found.extend(WBEMParser.get_recursively(value, field, match_key, match_value, value_only))

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        fields_found.extend(WBEMParser.get_recursively(item, field, match_key, match_value, value_only))

        return fields_found

    @classmethod
    def is_numeric(cls, value):
        '''Return True if data is numerical'''
        value_type = value.__class__.__name__
        if value_type in ['int', 'float']:
            return True
        if value_type in ['str', 'unicode']:
            try:
                test = float(value)
                return True
            except ValueError:
                pass
        return False

    @staticmethod
    def parse_results(results):
        '''clean up WBEM output'''
        # numeric types
        numtypes = ['Uint64', 'Uint16', 'Sint32', 'Uint32', 'Uint8']
        output = []
        for instance in results:
            info = {}
            for k, v in instance.items():
                k = str(k).strip()
                # convert various numeric types to int
                if v.__class__.__name__ in numtypes:
                    v = int(v)
                # leave a list alone
                elif isinstance(v, list):
                    continue
                # otherwise set to stripped string
                else:
                    v = str(v).strip()
                info[k] = v
            output.append(info)
        return output

    @staticmethod
    def parse_multiple(results):
        '''Parse multiple WBEM results'''
        output = {}
        if len(results) > 0:
            for result in results:
                # expecting a boolean, wbem output tuple
                if len(result) != 2:
                    log.warn("WBEM: Unexpected output ({})".format(result))
                    continue
                success, instances = result
                if not success:
                    msg = result_errmsg(instances)
                    if not 'Connection was closed cleanly' in msg:
                        log.warn('WBEM Query Failed: {}'.format(msg))
                    continue
                if not instances:
                    continue
                klass = instances[0].classname
                # return a list of dictionaries
                output[klass] = WBEMParser.parse_results(instances)
        return output
