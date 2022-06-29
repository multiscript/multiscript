
import os
import json
import logging
import subprocess
import time
from pathlib import Path
from pprint import pprint

_logger_name = Path(__file__).stem if __name__ == '__main__' else __name__
_logger = logging.getLogger(_logger_name)

virtual_env_path = Path(os.environ['VIRTUAL_ENV'])
project_path = virtual_env_path.parent # assumes virtual env is a top-level subdir of the project
pyside_uic_path = virtual_env_path / Path('bin/pyside6-uic')
mod_times_path = Path(__file__).parent / Path('.ui_mod_times.json')

# Exclude any ui files in the virutal environment
exclusions = set(virtual_env_path.glob('**/*.ui'))

sleep_time = 2 # In seconds

def main():
    mod_times = {}
    try:
        with open(mod_times_path) as infile:
            _logger.debug("Loading cache of modification times")
            mod_times = json.load(infile)

    except FileNotFoundError:
        pass

    _logger.info("Monitoring ui files...")
    try:
        while True:
            # Search for ui files
            ui_paths = [path for path in project_path.glob('**/*.ui') if path not in exclusions]
            mod_times_changed = False

            # Check if they need reconverting
            for ui_path in ui_paths:
                # It's possible a file could be deleted between our search above and our processing now
                if not ui_path.exists():
                    continue
                ui_path_str = str(ui_path)
                ui_mod_time = ui_path.stat().st_mtime
                py_path = ui_path.with_name(ui_path.stem + "_generated.py")

                if not py_path.exists() or \
                ui_path_str not in mod_times or \
                mod_times[ui_path_str] != ui_mod_time:
                    reconvert(ui_path, py_path)
                    mod_times[ui_path_str] = ui_mod_time
                    mod_times_changed = True

            # Remove cached times of any ui files that no longer exist
            for ui_path_str in list(mod_times.keys()):
                ui_path = Path(ui_path_str)
                if not ui_path.exists():
                    _logger.info("Removing " + str(ui_path.name) + " from monitor cache")
                    del mod_times[ui_path_str]
                    mod_times_changed = True

            if mod_times_changed:
                cache_mod_times(mod_times, mod_times_path)

            time.sleep(sleep_time)
    except KeyboardInterrupt:
        # Catch keyboard interrupts, as they are the main way to stop execution of this monitor.
        pass
    finally:
        _logger.info("Monitoring ended")     

def reconvert(ui_path, py_path):
    _logger.info("Reconverting " + str(ui_path.name) + " to " + str(py_path.name))
    args = [str(pyside_uic_path), '-o', str(py_path), str(ui_path)]
    subprocess.run(args)

def cache_mod_times(mod_times, mod_times_path):
    with open(mod_times_path, "w") as outfile:
        _logger.debug("Caching modification times")
        json.dump(mod_times, outfile, indent=4)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(name)s: %(levelname)s: %(asctime)s: %(message)s', style='%')
    main()