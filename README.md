# Multiscript
Combine Bible versions for multicultural ministry.

To learn more, see the project website at [multiscript.app](https://multiscript.app).

## Download
[Download latest binaries and source from Releases](https://github.com/multiscript/multiscript/releases).

The code is currently pre-release, so you should expect bugs. If you have skills that would benefit the project, we'd
love to hear from you! In particular, we'd like to extend the range of free Bible version sources available.

## Build Instructions
Use these instructions if you’re building from the source. Multiscript has been developed and tested mostly on macOS Mojave and more recently Ventura. We've done some very basic testing on Windows 11 and Linux.
1. Install Python
   * We recommend using Python 3.10 (and things likely won't work below Python 3.8).
1. Install git
1. `git clone https://github.com/multiscript/multiscript/`
1. `cd multiscript`
1. `python3 -m venv venv` (Create a virtual environment.)
   * On Windows: `python -m venv venv`
1. `source venv/bin/activate` (Activate the virtual environment.)
   * In Windows cmd.exe: `venv\Scripts\activate.bat`
   * In Windows powershell: `.\venv\Scripts\Activate.ps1` You may first need to run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
1. `pip install -r requirements.txt` (Install our dependencies)
1. At this point, if you want to run the build from source, execute: `python -m multiscript`
1. `python build.py` (Build the executable self-contained application from source)
   * The resulting `dist` directory will contain the built application.

