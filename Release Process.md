# Release Process

  1. On Mac:
     1. Update version numbers in `VERSION`, `multiscript.iss` and `CHANGES.md`
     1. Update version numbers in test plans (by searching for previous version number).
     1. Confirm all tests pass.
     1. Commit.
     1. Remove old `dist/` directory
     1. `python build.py`
  1. On Windows:
     1. Ensure repository sync is up to date.
     1. Remove old `dist/` directory
     1. `python build.py`
     1. For convenience, move `multiscript_installer.exe` into Mac `dist/` directory
  1. Create a new release tag on `main`, named `vX.Y.Z`. Include as assets:
     - `Multiscript.dmg`
     - `multiscript_installer.exe`
  1. Update current version number on website.
