
import os
import sys
import subprocess


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

