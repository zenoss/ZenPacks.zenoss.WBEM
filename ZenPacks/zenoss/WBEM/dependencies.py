import importlib
import os
import site
from Products.ZenUtils.Utils import monkeypatch

modules_imported = False
callback_patched = False
#datetime_patched = False

def import_module(module_name, module_dir):
    """Import and return module_name.

    Uses the platform's default module if it exists, otherwises uses the
    ZenPack's bundled version.

    """
    try:
        return importlib.import_module(module_name)
    except ImportError:
        mpath = os.path.join(
            os.path.dirname(__file__),
            module_dir)
        site.addsitedir(mpath)
        return importlib.import_module(module_name)

def import_wbem_libs():
    """Return pywbem module."""
    global modules_imported
    if not modules_imported:
        import_module('ply',      'dependencies/ply-3.11')
        import_module('typing',   'dependencies/typing-3.6.6')
        import_module('M2Crypto', 'dependencies/m2crypto-0.32.0')
        import_module('pywbem',   'dependencies/pywbemz-0.14.3')
        set_monkeypatches()
        #link_CIMDateTime()
        modules_imported = True
    return

def set_monkeypatches():
    global callback_patched
    if not callback_patched:
        callback_patched = True
        @monkeypatch('pywbem.cim_operations.WBEMConnection')
        def __init__(self, url, creds=None, default_namespace=None,
                     x509=None, verify_callback=None, ca_certs=None,
                     no_verification=False, timeout=None, use_pull_operations=False,
                     stats_enabled=False):
            # Monkeypatch to intercept calls to WBEMConnection and set the SSL Cert verify-callback
            return original(self, url=url, creds=creds, default_namespace=default_namespace, x509=x509,
                            verify_callback=SSLCertCheck,
                            ca_certs=ca_certs, no_verification=no_verification, timeout=timeout,
                            use_pull_operations=use_pull_operations, stats_enabled=stats_enabled)

def SSLCertCheck(connection, x509, errnum, errdepth, return_code):
    # ignore check, just accept cert - bad
    # (future: add a zProperty to check cert name)
    return True

'''
Due to EMC.base zenpacks' immediate dependency on pywbem (due to __init__.py) this WBEM zenpack must
have the dynamic libraries loaded at launch.  Thus the runtime-dynamic link is not needed.
Instead we will import the dependencies on launch

def link_CIMDateTime():
    global datetime_patched
    if not datetime_patched:
        datetime_patched = True
        @monkeypatch('ZenPacks.zenoss.WBEM.datasources.WBEMDataSource')
        class CIMDateTime(pywbem.CIMDateTime):
            # WBEMDataSources.CIMDateTime should derive from pywbem.CIMDateTime via dynamic dependencies
            pass
'''
