# Multiscript
Gather Bible passages in multiple languages for multicultural ministry.

## Download
[Download Mac and Windows binaries (or source) from Releases](https://github.com/multiscript/multiscript/releases).

## Background
Multicultural Christian ministries often need to provide printed copies of Bible passages for their members and guests, usually with one or more Bible versions printed in parallel. Typically, the size of each passage is small, but the number of different version combinations is large. This tool simplifies the process of collating the different versions, and inserting them into a template document. The result is a series of files, each containing a different combination of Bible versions, for the same Bible passages. These files can then be printed, subject to copyright and licensing restrictions.

Multiscript is designed to be easy to use, while also being highly flexible in the output it produces. A basic plugin system allows for further customisation.

This code is in active use, but please note it's currently a very part-time project, and the code is pre-release only. If you have skills that would benefit the project, we'd love to hear from you! In particular, we'd like to extend the range of free Bible version sources available.

## Build Instructions
Multiscript has been developed and tested mostly on macOS Mojave. We've done some very basic testing on Windows 10.
1. Install Python (we've only tested with Python 3.7)
1. Install git
1. `git clone https://github.com/jamesbcd/multiscript/`
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

