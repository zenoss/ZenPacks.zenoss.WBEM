import importlib
import os
import site


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


def import_pywbem():
    """Return pywbem module."""
    #import_module('ply',      'lib/ply-3.11')
    #import_module('pywbem',   'lib/pywbemz-0.14.3')
    return
