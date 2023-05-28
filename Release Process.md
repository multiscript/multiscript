# Release Process

  1. On Mac:
     1. Create `release-vX.Y.Z` branch from `main`
     1. Make development changes on the release branch.
     1. Update version numbers in `VERSION`, `multiscript.iss` and `CHANGES.md`
     1. Commit, then squash `release-vX.Y.Z` into `main`
     1. Can delete `release-vX.Y.Z` branch at this point.
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
