##############################################################################
#
# Copyright (C) Zenoss, Inc. 2017, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from ZenPacks.zenoss.WBEM.utils import addLocalLibPath
addLocalLibPath()

from pywbem import CIMError
from pywbem import twisted_client
try:
    from elementtree.ElementTree import fromstring
except ImportError, arg:
    from xml.etree.ElementTree import fromstring


class HandleResponseMixin():
    """Override base parseErrorAndResponse from pywbem.twisted_client module
    to catch XML parsing error"""

    def parseErrorAndResponse(self, data):
        """Parse returned XML for errors, then convert into
        appropriate Python objects."""
        try:
            xml = fromstring(data)
        except Exception:
            raise (
                CIMError(
                    0, 'Incorrect XML response for {0}'.format(self.classname)
                )
            )

        error = xml.find('.//ERROR')

        if error is not None:
            msg = error.get('DESCRIPTION')
            if msg and "context cannot be found" in msg:
                error.set("DESCRIPTION",
                          "Response is not complete for {} classname. "
                          "Please check zWBEMOperationTimeout and "
                          "zWBEMMaxObjectCount properties".format(self.classname)
                )
        else:
            #self.deferred.callback(self.parseResponse(xml))
            return xml

        try:
            code = int(error.attrib['CODE'])
        except ValueError:
            code = 0

        raise (CIMError(code, error.attrib['DESCRIPTION']))


class EnumerateInstances(HandleResponseMixin, twisted_client.EnumerateInstances):
    pass


class EnumerateInstanceNames(HandleResponseMixin, twisted_client.EnumerateInstanceNames):
    pass


class EnumerateClasses(HandleResponseMixin, twisted_client.EnumerateClasses):
    pass


class EnumerateClassNames(HandleResponseMixin, twisted_client.EnumerateClassNames):
    pass


class PullInstances(HandleResponseMixin, twisted_client.PullInstances):
    pass


class OpenEnumerateInstances(HandleResponseMixin, twisted_client.OpenEnumerateInstances):
    pass

