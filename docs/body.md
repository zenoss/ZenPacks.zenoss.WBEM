WBEM ZenPack
============

Adds a *WBEM* data source type and a *WBEMPlugin* base modeler plugin.

Support
-------

WBEM ZenPack is an Open Source ZenPack developed by Zenoss, Inc. Enterprise
support for this ZenPack is available to commercial customers with an
active subscription.

Releases
--------

Version 2.0.0- [Download](http://wiki.zenoss.org/download/zenpacks/ZenPacks.zenoss.WBEM/2.0.0/ZenPacks.zenoss.WBEM-2.0.0.egg){.external}
:   Released on 2017/12/27
:   Requires [PythonCollector ZenPack](/product/zenpacks/pythoncollector "ZenPack:PythonCollector")
:   Compatible with Zenoss Core 4.2.x, Zenoss Core 5.x.x, Zenoss
    Resource Manager 4.2.x, Zenoss Resource Manager 5.x.x, Zenoss Core 6.x.x, Zenoss Resource Manager 6.x.x


Version 1.0.3- [Download](http://wiki.zenoss.org/download/zenpacks/ZenPacks.zenoss.WBEM/1.0.3/ZenPacks.zenoss.WBEM-1.0.3.egg){.external}
:   Released on 2015/09/11
:   Requires [PythonCollector ZenPack](/product/zenpacks/pythoncollector "ZenPack:PythonCollector")
:   Compatible with Zenoss Core 4.2.x, Zenoss Core 5.x.x, Zenoss
    Resource Manager 4.2.x, Zenoss Resource Manager 5.x.x

Background
----------

This ZenPack provides a new *WBEM* data source type that makes it easy
to collect metrics from a WBEM provider using a CQL query. It also
provides a new *WBEMPlugin* modeler plugin base class that simplifies
modeling devices and applications that support WBEM.

Installed Items
---------------

Datasource Types

- WBEM

Configuration Properties

- zWBEMPort
- zWBEMUsername
- zWBEMPassword
- zWBEMUseSSL
- zWBEMRequestTimeout
- zWBEMMaxObjectCount
- zWBEMOperationTimeout

Configuration Options
---------------------

- zWBEMPort: Value of the WBEM port number. The default value is 5989.
- zWBEMUsername: WBEM username.
- zWBEMPassword: Password for user defined by *zWBEMUsername*.
- zWBEMUseSSL: True or false value to use SSL. The default value is true.
- zWBEMRequestTimeout: Time in seconds while Zenoss waits for WBEM server to return all data.
- zWBEMMaxObjectCount: Maximum number of instances the WBEM server may return for each of the requests. The user should adjust the value if device modeling never completes.
- zWBEMOperationTimeout: Time in seconds while WBEM Server keeps enumeration session opened after a previous request.

WBEM Data Source Type
---------------------

The *WBEM* data source type added by this ZenPack allows you to add a
WBEM data source with the following new data source properties.

Namespace
:   The WBEM namespace. This must be specified and there is no default
    value. A common example would be root/cimv2.

<!-- -->

CQL Query
:   The CQL query to execute that will return the desired record(s).
    It must be specified, and there is no default value.

<!-- -->

Result Component Key
:   Optional. Only used in cases where the WBEM data source is in a
    monitoring template that gets bound to components. In this case
    *Result Component Key* should be set to the attribute or column name
    that contains the component identifier in the result set of the CQL
    Query.

<!-- -->

Result Component Value
:   Optional. Only used in cases where the WBEM data source is in a
    monitoring template that gets bound to components. In this case
    *Result Component Value* is the value that gets mapped to values in
    the *Result Component Key* column of the CQL result set. Typically
    this takes the form of a TALES expression such as \${here/id} or
    \${here/wbemInstanceId} if wbemInstanceID was modeled on your
    component.

<!-- -->

Result Timestamp Key
:   Optional. Used in both device- and component-bound monitoring
    templates when the query result set has a column noting the time the
    data was originally collected. Like the *Result Component Key* this
    should be the name of an attribute or column name in the results. By
    default this will default to NOW as the collection time.

WBEMPlugin Modeler Plugin Base Class
------------------------------------

The *WBEMPlugin* modeler plugin base class allows you to create modeler
plugins that do something with data that is returned from a WBEM
EnumerateInstances call.

See the following example of a modeler plugin.


```python

from ZenPacks.zenoss.WBEM.modeler.wbem import WBEMPlugin
from ZenPacks.zenoss.WBEM.utils import result_errmsg

"""Description of what MyWBEMPlugin does."""

class MyWBEMPlugin(WBEMPlugin):
    wbemQueries = {
        # EnumerateInstances (ei) for all EMC arrays.
        'root/emc:EMC_ArrayChassis': 'ei',
        }

    def process(self, device, results, log):
        log.info('Modeler %s processing data for device %s',
            self.name(), device.id)

        for success, instances in results:
            if not success:
                log.warn("WBEM: %s %s", device.id, result_errmsg(instances))
                continue

            # Check for no instances in results.
            if len(instances) < 1:
                continue

            # classname will become EMC_ArrayChassis.
            classname = instances[0].classname

            if classname == 'EMC_ArrayProduct':
                return self.objectMap(compname='hw', data={
                    'serialNumber': instance['SerialNumber'],
                    'setProductKey': MultiArgs(instance['Model'], instance['Manufacturer']),
                    })

```


Troubleshooting
---------------

Please refer the Zenoss Service Dynamics documentation if you run into any of the following problems:

-   ZenPack will not install
-   Adding device fails
-   Don't understand how to add a device
-   Don't understand how to model a device

If you cannot find the answer in the documentation, then Resource Manager (Service Dynamics)
users should contact [Zenoss Customer Support](https://support.zenoss.com).
Core users can use the *#zenoss* IRC channel or the [Zenoss Community Forums](https://community.zenoss.com/home).

### WBEM Device Modeling or Monitoring never completes

Please check *zWBEMMaxObjectCount*, *zWBEMOperationTimeout*, and *zWBEMRequestTimeout* zProperties documentation 
and adjust the vaules

Changes
-------

2.0.0

-   Add optional pull instance operations during modeling (ZPS-2450)
-   Add optional pull instance operations during monitoring (ZPS-2533)
-   Fix memory leak in zenpython (ZPS-2742)
-   Tested with Zenoss Resource Manager 6.0.1, Zenoss Resource Manager 6.1.0, Zenoss Resource Manager 5.3.3, Zenoss Resource Manager 4.2.5 RPS 743 and Service Impact 5.2.3

