#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2017 all rights reserved.
#
# You should have received a copy of the GNU General Public License
# along with this ZenPack. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import pprint

import Globals
from Products.ZenUtils.Utils import unused

from ZenPacks.zenoss.WBEM.utils import addLocalLibPath
addLocalLibPath()

from pywbem.cim_operations import WBEMConnection
from WBEMParser import WBEMParser

from optparse import OptionParser
unused(Globals)


HOST = ''
USERNAME = ''
PASSWORD = ''


class WBEMCommand(object):
    '''Collect WBEM data samples'''
    def __init__(self):
        self.buildOptions()
        baseurl = 'http'
        if self.options.ssl:
            baseurl = 'https'
        url = '{}://{}:{}'.format(baseurl, self.options.host, self.options.tcpport)
        print 'Using', url
        self.credentials = (self.options.username, self.options.password)
        self.client = WBEMConnection(url, self.credentials, self.options.namespace)
        self.parse = WBEMParser

    def buildOptions(self):
        ''''''
        self.parser = OptionParser(usage="usage: %prog [options] filename",
                                    version="%prog 1.0")
        self.parser.add_option('--host',
                        dest='host',
                        default=HOST,
                        help='WBEM Host/IP')
        self.parser.add_option('--tcpport',
                         dest='tcpport',
                         default='5989',
                         help='WBEM TCP Port')
        self.parser.add_option('--username',
                         dest='username',
                         default=USERNAME,
                         help='WBEM User')
        self.parser.add_option('--password',
                         dest='password',
                         default=PASSWORD,
                         help='WBEM Password')
        self.parser.add_option('--ssl',
                         dest='ssl',
                         default=True,
                         action='store_true',
                         help='WBEM uses SSL')
        self.parser.add_option('--namespace',
                         dest='namespace',
                         default='root/cimv2',
                         help='WBEM Namespace')
        (self.options, self.args) = self.parser.parse_args()

    def run(self):
        results = {}
        for cls_name in self.client.EnumerateClassNames(namespace=self.options.namespace, DeepInheritance=True):
            print cls_name
            print '-' * 80
            output = self.client.EnumerateInstanceNames(cls_name)
            results[cls_name] = self.parse.parse_results(output)
        self.write_data(results, 'output.txt')

    def write_data(self, data, filename):
        '''write out data to the provided filename'''
        print 'Writing results to {}'.format(filename)
        with open(filename, 'w') as f:
            if self.options.raw:
                f.write(str(data))
            else:
                pprint.pprint(data, stream=f)
        f.close()


if __name__ == '__main__':
    u = WBEMCommand()
    u.run()
