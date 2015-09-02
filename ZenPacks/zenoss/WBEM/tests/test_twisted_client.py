##############################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from mock import Mock, sentinel

from Products.ZenTestCase.BaseTestCase import BaseTestCase

from ZenPacks.zenoss.WBEM.utils import addLocalLibPath
addLocalLibPath()

from pywbem.twisted_client import EnumerateInstances

class TestParseResponse(BaseTestCase):

    def test_catalog_is_empty(self):
        self.assertEqual(len(EnumerateInstances.parseResponse(2)), 0)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestParseResponse))
    return suite

