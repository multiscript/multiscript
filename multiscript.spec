# -*- mode: python ; coding: utf-8 -*-

import importlib
import platform
import sys
from stdlibs import stdlib_module_names
from PyInstaller.utils.hooks import collect_submodules

sys.path.append('.')    # Needed to allow multiscript module to be found in current directory
import multiscript

#
# Set various parameters
#
app_version = str(multiscript.get_app_version())
onefile = False
block_cipher = None

#
# Collect majority of std library, so it's available for plugins
#
exclusions = set(['antigravity','turtle','turtledemo','cmd','this','tkinter','idlelib','lib2to3',
                  'unittest','test','doctest','ensurepip',
                  'aifc','asynchat','asyncore','audioop','cgi','cgitb','chunk','crypt','imghdr','imp',
                  'mailcap','msilib','nis','nntplib','optparse','ossaudiodev','pipes','smtpd',
                  'sndhdr','spwd','sunau','telnetlib','uu','xdrlib'])
std_lib_hidden_imports = []
for mod_name in sorted(stdlib_module_names()):
    try:
        if mod_name not in exclusions and mod_name[0] != "_": # Exclude all private modules
            # We used to try actually importing the module, and only collecting it
            # if the import succeeded. However, this doesn't seem to be strictly necessary.
            #
            # importlib.import_module(mod_name)
            #
            std_lib_hidden_imports.append(mod_name)
            submod_names = collect_submodules(mod_name)
            std_lib_hidden_imports.extend(submod_names)
            # print("Including", mod_name, submod_names)
    except (ModuleNotFoundError, ImportError) as e:
        # print("Skipping", mod_name)
        pass

#
# Main spec file elements
#
a = Analysis(['multiscript/__main__.py'],
        binaries=[],
        datas=[ ('VERSION', '.'),
                ('Attribution.html', '.'),
                ('multiscript/templates', 'multiscript/templates'),
                ('multiscript/icons', 'multiscript/icons'),
                ('multiscript/icons/*.icns', '.')],
        hiddenimports=std_lib_hidden_imports,
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher,
        noarchive=False
    )

pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)

exe = EXE(pyz,
        a.scripts,
        a.binaries if onefile else [],
        a.zipfiles if onefile else [],
        a.datas if onefile else [],
        exclude_binaries=not onefile,
        name='Multiscript_', # Can't be named 'multiscript' due to clash with directory of that name
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        icon='multiscript/icons/multiscript.ico',
        disable_windowed_traceback=False,
        argv_emulation=multiscript.ARGV_EMULATION,
        target_arch='x86_64',
        codesign_identity=None,
        entitlements_file=None,
    )
bundle_obj = exe

if not onefile:
    coll = COLLECT(
            exe,
            a.binaries,
            a.zipfiles,
            a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name='multiscript',
        )
    bundle_obj = coll

app = BUNDLE(bundle_obj,
        name='Multiscript.app',
        icon='multiscript/icons/multiscript.icns',
        bundle_identifier="app.multiscript",
        info_plist={
            'CFBundleShortVersionString': app_version,
            'UTExportedTypeDeclarations':
                [{
                    'UTTypeIdentifier': 'app.multiscript.mplan',
                    'UTTypeConformsTo': ['public.json'],
                    'UTTypeTagSpecification':
                        {
                            'public.filename-extension': ['mplan']
                        },
                    'UTTypeDescription': 'Multiscript Plan',
                    'UTTypeIconFile': 'multiscript_mplan.icns'
                },
                {
                    'UTTypeIdentifier': 'app.multiscript.mplugin',
                    'UTTypeConformsTo': ['public.zip-archive'],
                    'UTTypeTagSpecification':
                        {
                            'public.filename-extension': ['mplugin']
                        },
                    'UTTypeDescription': 'Multiscript Plugin',
                    'UTTypeIconFile': 'multiscript_mplugin.icns'
                }],
            'CFBundleDocumentTypes':
                [{
                    'CFBundleTypeName': 'Multiscript Plan File',
                    'CFBundleTypeRole': 'Editor',
                    'CFBundleTypeIconFile': 'multiscript_mplan.icns',
                    'LSHandlerRank': 'Owner',
                    'LSItemContentTypes': ['app.multiscript.mplan']
                },
                {
                    'CFBundleTypeName': 'Multiscript Plugin',
                    'CFBundleTypeRole': 'Editor',
                    'CFBundleTypeIconFile': 'multiscript_mplugin.icns',
                    'LSHandlerRank': 'Owner',
                    'LSItemContentTypes': ['app.multiscript.mplugin']
                }]
        }
    )
