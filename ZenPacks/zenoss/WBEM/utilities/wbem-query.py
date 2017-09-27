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
from optparse import OptionParser
from WBEMCommand import WBEMCommand


class WBEMQuery(WBEMCommand):
    '''Collect JSON data samples while iterating over endpoints'''

    def buildOptions(self):
        ''''''
        self.parser = OptionParser(usage="usage: %prog [options] filename",
                                    version="%prog 1.0")
        self.parser.add_option('--host',
                        dest='host',
                        help='WBEM Host/IP')
        self.parser.add_option('--tcpport',
                         dest='tcpport',
                         default='5989',
                         help='WBEM TCP Port')
        self.parser.add_option('--username',
                         dest='username',
                         help='WBEM User')
        self.parser.add_option('--password',
                         dest='password',
                         help='WBEM Password')
        self.parser.add_option('--ssl',
                         dest='ssl',
                         default=True,
                         action='store_true',
                         help='WBEM uses SSL')
        self.parser.add_option('--operation',
                         dest='operation',
                         default='ei',
                         help='WBEM Operation')
        self.parser.add_option('--namespace',
                         dest='namespace',
                         default='root/cimv2',
                         help='WBEM Namespace')
        self.parser.add_option('--classname',
                         dest='classname',
                         default='CIM_ComputerSystem',
                         help='WBEM Classname')
        self.parser.add_option('--raw',
                         dest='raw',
                         default=False,
                         action='store_true',
                         help='Return raw data')
        self.parser.add_option('--dump',
                         dest='dump',
                         default=False,
                         action='store_true',
                         help='Perform WBEM walk')
        (self.options, self.args) = self.parser.parse_args()

    def run(self):
        if self.options.operation == 'ei':
            print 'Enumerating instances for class: {}'.format(self.options.classname)
            results = self.client.EnumerateInstances(self.options.classname)

        elif self.options.operation == 'ein':
            print 'Enumerating instance names for class: {}'.format(self.options.classname)
            results = self.client.EnumerateInstanceNames(self.options.classname)

        elif self.options.operation == 'ec':
            print 'Enumerating classes in namespace: {}'.format(self.options.namespace)
            results = self.client.EnumerateClasses(namespace=self.options.namespace, DeepInheritance=True)

        elif self.options.operation == 'ecn':
            print 'Enumerating class names in namespace: {}'.format(self.options.namespace)
            results = self.client.EnumerateClassNames(namespace=self.options.namespace, DeepInheritance=True)

        if self.options.raw or 'n' in self.options.operation:
            print '-' * 80
            print 'results ', results
        else:
            results = self.parse.parse_results(results)
            print '-' * 80
            pprint.pprint(results)

        filename = 'wbem-{}-{}-{}.txt'.format(self.options.operation,
                                              self.options.namespace.replace('/', '_'),
                                              self.options.classname)
        if self.options.raw:
            filename = filename.replace('.txt', '-raw.txt')
        self.write_data(results, filename)


if __name__ == '__main__':
    u = WBEMQuery()
    u.run()
