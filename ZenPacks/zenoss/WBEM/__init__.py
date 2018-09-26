##############################################################################
#
# Copyright (C) Zenoss, Inc. 2012, 2017, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import logging
LOG = logging.getLogger('zen.WBEM')

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenRelations.zPropertyCategory import setzPropertyCategory
import ZenPacks.zenoss.WBEM.patches


# Categorize our zProperties.
ZPROPERTY_CATEGORY = 'WBEM'

setzPropertyCategory('zWBEMPort', ZPROPERTY_CATEGORY)
setzPropertyCategory('zWBEMUsername', ZPROPERTY_CATEGORY)
setzPropertyCategory('zWBEMPassword', ZPROPERTY_CATEGORY)
setzPropertyCategory('zWBEMUseSSL', ZPROPERTY_CATEGORY)
setzPropertyCategory('zWBEMRequestTimeout', ZPROPERTY_CATEGORY)
setzPropertyCategory('zWBEMMaxObjectCount', ZPROPERTY_CATEGORY)
setzPropertyCategory('zWBEMOperationTimeout', ZPROPERTY_CATEGORY)


class ZenPack(ZenPackBase):
    """WBEM ZenPack."""

    packZProperties = [
        ('zWBEMPort', 5989, 'int'),
        ('zWBEMUsername', '', 'string'),
        ('zWBEMPassword', '', 'password'),
        ('zWBEMUseSSL', True, 'boolean'),
        ('zWBEMRequestTimeout', 290, 'int'),
        ('zWBEMMaxObjectCount', 0, 'int'),
        ('zWBEMOperationTimeout', 0, 'int'),
    ]

    packZProperties_data = {
        'zWBEMPort': {
            'category': ZPROPERTY_CATEGORY,
            'label': 'WBEM Port',
            'description': 'TCP port of remote WBEM service',
            'type': 'int',
        },
        'zWBEMUsername': {
            'category': ZPROPERTY_CATEGORY,
            'label': 'WBEM Username',
            'description': 'Username for remote WBEM service.',
            'type': 'string',
        },
        'zWBEMPassword': {
            'category': ZPROPERTY_CATEGORY,
            'label': 'WBEM Password',
            'description': 'Password for remote WBEM service.',
            'type': 'password',
        },
        'zWBEMUseSSL': {
            'category': ZPROPERTY_CATEGORY,
            'label': 'WBEM SSL',
            'description': 'Use SSL for remote WBEM service.',
            'type': 'boolean',
        },
        'zWBEMRequestTimeout': {
            'category': ZPROPERTY_CATEGORY,
            'label': 'WBEM Request Timeout',
            'description': 'Timeout (in seconds) for WBEM requests.',
            'type': 'int',
        },
        'zWBEMMaxObjectCount': {
            'category': ZPROPERTY_CATEGORY,
            'label': 'WBEM Max Objects',
            'description': 'Maximum objects allowed to be returned per WBEM request.',
            'type': 'int',
        },
        'zWBEMOperationTimeout': {
            'category': ZPROPERTY_CATEGORY,
            'label': 'WBEM Operation Timeout',
            'description': 'Timeout (in seconds) for WBEM operations.',
            'type': 'int',
        },
    }
