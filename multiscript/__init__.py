
from pathlib import Path
import platform

import semver

from multiscript.application import MultiscriptApplication


# Flag to turn pyinstaller argv-emulation on macOS on (True) or off (False)
#
# Argv-emulation doesn't seem to work on macOS Ventura, so we disable it for
# now. See https://github.com/pyinstaller/pyinstaller/issues/7355
ARGV_EMULATION = False


_app = None

def app():
    global _app
    if _app is None:
        _app = MultiscriptApplication()
    return _app


_platform_system = None

def get_platform_system():
    global _platform_system
    if _platform_system is None:
        _platform_system = platform.system()
    
    return _platform_system

def on_mac():
    return get_platform_system() == "Darwin"

def on_windows():
    return get_platform_system() == "Windows"


_app_version = None

def get_app_version():
    '''This function to return the app version is implemented as a module-level function
    (rather than a method on the app) so that it can easily be called by build scripts.
    '''
    global _app_version
    if _app_version is not None:
        return _app_version

    version_path = Path(__file__).parent.parent / Path("VERSION")
    try:
        with open(version_path) as file:
            _app_version = semver.VersionInfo.parse(file.readline())
    except:
        _app_version = semver.VersionInfo.parse("0.0.0")

    return _app_version
