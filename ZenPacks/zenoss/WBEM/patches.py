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

from . import dependencies
dependencies.import_wbem_libs()
from pywbem import CIMError
import pywbem.twisted_agent

try:
    from elementtree.ElementTree import fromstring
except ImportError, arg:
    from xml.etree.ElementTree import fromstring


class HandleResponseMixin():
    """Override base parseErrorAndResponse from pywbem.twisted_agent module
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
            return xml

        try:
            code = int(error.attrib['CODE'])
        except ValueError:
            code = 0

        raise (CIMError(code, error.attrib['DESCRIPTION']))


class EnumerateInstances(HandleResponseMixin, pywbem.twisted_agent.EnumerateInstances):
    pass


class EnumerateInstanceNames(HandleResponseMixin, pywbem.twisted_agent.EnumerateInstanceNames):
    pass


class EnumerateClasses(HandleResponseMixin, pywbem.twisted_agent.EnumerateClasses):
    pass


class EnumerateClassNames(HandleResponseMixin, pywbem.twisted_agent.EnumerateClassNames):
    pass


class PullInstances(HandleResponseMixin, pywbem.twisted_agent.PullInstances):
    pass


class OpenEnumerateInstances(HandleResponseMixin, pywbem.twisted_agent.OpenEnumerateInstances):
    pass
