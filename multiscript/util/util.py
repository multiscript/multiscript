
import ctypes.util
import os
import sys
import subprocess


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
    def prototype(self, functype, result_type, func_name, *arg_items):
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
        return functype(result_type, *arg_types)((func_name, self.lib), tuple(param_flags))

    def c_prototype(self, result_type, func_name, *arg_items):
        '''
        Each arg_item should be
        (in_or_out_const, arg_type[, param_name_str[, default_value]])
        '''
        from ctypes import CFUNCTYPE
        return self.prototype(CFUNCTYPE, result_type, func_name, *arg_items)

    def w_prototype(self, result_type, func_name, *arg_items):
        '''
        Each arg_item should be
        (in_or_out_const, arg_type[, param_name_str[, default_value]])
        '''
        from ctypes import WINFUNCTYPE
        return self.prototype(WINFUNCTYPE, result_type, func_name, *arg_items)


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

