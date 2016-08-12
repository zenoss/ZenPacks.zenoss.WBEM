##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from pywbem import CIMError
try:
    from elementtree.ElementTree import fromstring
except ImportError, arg:
    from xml.etree.ElementTree import fromstring

from pywbem.twisted_client import (
    EnumerateClassNames as BaseEnumerateClassNames,
    EnumerateClasses as BaseEnumerateClasses,
    EnumerateInstanceNames as BaseEnumerateInstanceNames,
    EnumerateInstances as BaseEnumerateInstances
)


class HandleResponceMixin():
    """Override base parseErrorAndResponse from pywbem.twisted_client module
    to catch XML parsing error"""

    def parseErrorAndResponse(self, data):
        """Parse returned XML for errors, then convert into
        appropriate Python objects."""
        try:
            xml = fromstring(data)
        except Exception:
            self.deferred.errback(
                CIMError(
                    0, 'Incorrect XML response for {0}'.format(self.classname)
                )
            )
            return

        error = xml.find('.//ERROR')

        if error is None:
            self.deferred.callback(self.parseResponse(xml))
            return

        try:
            code = int(error.attrib['CODE'])
        except ValueError:
            code = 0

        self.deferred.errback(CIMError(code, error.attrib['DESCRIPTION']))


class EnumerateInstances(HandleResponceMixin, BaseEnumerateInstances):
    pass


class EnumerateInstanceNames(HandleResponceMixin, BaseEnumerateInstanceNames):
    pass


class EnumerateClasses(HandleResponceMixin, BaseEnumerateClasses):
    pass


class EnumerateClassNames(HandleResponceMixin, BaseEnumerateClassNames):
    pass
