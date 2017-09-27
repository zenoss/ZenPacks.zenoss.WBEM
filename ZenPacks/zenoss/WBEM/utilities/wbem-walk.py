#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2017 all rights reserved.
#
# You should have received a copy of the GNU General Public License
# along with this ZenPack. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from WBEMCommand import WBEMCommand


class WBEMWalk(WBEMCommand):
    '''Collect WBEM data samples'''

    def run(self):
        results = {}
        for cls_name in self.client.EnumerateClassNames(namespace=self.options.namespace, DeepInheritance=True):
            print cls_name
            print '-' * 80
            output = self.client.EnumerateInstanceNames(cls_name)
            results[cls_name] = self.parse.parse_results(output)
        filename = 'wbem-dump-names-{}.txt'.format(self.options.host.replace('.', '_'))
        self.write_data(results, filename)

if __name__ == '__main__':
    u = WBEMWalk()
    u.run()
