
import ctypes
import ctypes.util
import os
import pathlib
import sys
import subprocess

def is_absolute_any_platform(path):
    if isinstance(path, str):
        # If a string path is from an unknown platform, it's most reliable to convert it to a Windows path,
        # as backslashes are less common on POSIX paths (and are never path separators), but are regularly
        # path separators on Windows.
        path = pathlib.PureWindowsPath(path)
    
    # Converting between path flavours is only reliable when going via POSIX path strings. Otherwise, the
    # absolute nature of absolute paths is lost.
    return pathlib.PurePosixPath(path.as_posix()).is_absolute() or \
           pathlib.PureWindowsPath(path.as_posix()).is_absolute()

def launch_file(path):
    if sys.platform == "win32":
        # windows
        os.startfile(path)
    elif sys.platform == "darwin":
        # mac OS
        subprocess.call(["open", path])
    else:
        # Other Unix
        subprocess.call(["xdg-open", path])

def set_file_hidden_windows(path):
    '''Returns True if file successfully hidden.'''
    if sys.platform == "win32":
        from ctypes import wintypes
        kernel32 = Kernel32Library()
        file_attrs = kernel32.GetFileAttributesW(str(path))
        if file_attrs == kernel32.INVALID_FILE_ATTRIBUTES.value:
            # We can't get the file attributes, so can't hide the file
            return False
        file_attrs = wintypes.DWORD(file_attrs | kernel32.FILE_ATTRIBUTE_HIDDEN.value)
        if not kernel32.SetFileAttributesW(str(path), file_attrs):
            # Failed to set the attributes
            return False
        return True
    else:
        return False

def set_file_unhidden_windows(path):
    '''Returns True if file successfully unhidden.'''
    if sys.platform == "win32":
        from ctypes import wintypes
        kernel32 = Kernel32Library()
        file_attrs = kernel32.GetFileAttributesW(str(path))
        if file_attrs == kernel32.INVALID_FILE_ATTRIBUTES.value:
            # We can't get the file attributes, so can't unhide the file
            return False
        file_attrs = wintypes.DWORD(file_attrs & ~kernel32.FILE_ATTRIBUTE_HIDDEN.value)
        if not kernel32.SetFileAttributesW(str(path), file_attrs):
            # Failed to set the attributes
            return False
        return True
    else:
        return False


class CTypesLibrary:
    # Adapted from fontfinder library
    IN:  int    = 1
    OUT: int    = 2
    IN0: int    = 4

    def __init__(self, library_loader, library_name: str, find_library: bool = False, alt_pathname: str = None):
        '''`alt_pathname` is an alternative pathname to try if a library named `library_name` cannot be found.
        '''
        if find_library:
            library_name = ctypes.util.find_library(library_name)
            if library_name is None:
                library_name = alt_pathname
        self.lib = library_loader.LoadLibrary(library_name)

    # Inspired by https://www.cs.unc.edu/~gb/blog/2007/02/11/ctypes-tricks/
    def prototype(self, functype, result_type, func_name, *arg_items, **kwargs):
        '''
        Each arg_item should be
        (in_or_out_const, arg_type[, param_name_str[, default_value]])
        '''
        arg_types = []
        param_flags = []
        for arg_item in arg_items:
            arg_types.append(arg_item[1])
            param_flag = [arg_item[0]]
            if len(arg_item) > 2:
                param_flag.append(arg_item[2])
            if len(arg_item) > 3:
                param_flag.append(arg_item[3])
            param_flags.append(tuple(param_flag))
        return functype(result_type, *arg_types, **kwargs)((func_name, self.lib), tuple(param_flags))

    def c_prototype(self, result_type, func_name, *arg_items, **kwargs):
        '''
        Each arg_item should be
        (in_or_out_const, arg_type[, param_name_str[, default_value]])
        '''
        from ctypes import CFUNCTYPE
        return self.prototype(CFUNCTYPE, result_type, func_name, *arg_items)

    def w_prototype(self, result_type, func_name, *arg_items, **kwargs):
        '''
        Each arg_item should be
        (in_or_out_const, arg_type[, param_name_str[, default_value]])
        '''
        from ctypes import WINFUNCTYPE
        return self.prototype(WINFUNCTYPE, result_type, func_name, *arg_items)


class Kernel32Library(CTypesLibrary):
    def __init__(self):
        super().__init__(ctypes.LibraryLoader(ctypes.WinDLL), "Kernel32")

        from ctypes import wintypes
        self.INVALID_FILE_ATTRIBUTES = wintypes.DWORD(-1)
        self.FILE_ATTRIBUTE_HIDDEN = wintypes.DWORD(0x02)

        self.GetFileAttributesW = self.w_prototype(
            wintypes.DWORD, "GetFileAttributesW", (self.IN, wintypes.LPCWSTR, "lpFileName"),
            use_last_error=True
        )

        self.SetFileAttributesW = self.w_prototype(
            wintypes.BOOL, "SetFileAttributesW", (self.IN, wintypes.LPCWSTR, "lpFileName"),
                                                 (self.IN, wintypes.DWORD, "dwFileAttributes"),
            use_last_error=True
        )
