"""
Manages the games settings.
Make sure to load the settings from file before trying to access then.
Retrieve/Edit them via the \"usersettings\" dict after loading.
"""

import json

from simplejson import JSONDecodeError
from itblib.Log import log

SETTINGS_PATH = "itb_settings.json"

usersettings:"dict[str|any]|None" = None

def load_settings():
    """Load settings from file."""
    global usersettings
    try:
        with open(SETTINGS_PATH, "r", encoding='utf8') as settings_file:
            usersettings = json.load(settings_file)
    except FileNotFoundError as fnf_excpetion:
        log(fnf_excpetion, 0)
    except JSONDecodeError as json_exception:
        log(json_exception, 2)
    finally:
        usersettings = {}

def save_settings():
    """Write settings to file."""
    try:
        with open(SETTINGS_PATH, "w", encoding='utf8') as settings_file:
            json.dump(usersettings, settings_file)
    except FileNotFoundError as fnf_excpetion:
        log(fnf_excpetion, 2)
    except JSONDecodeError as json_exception:
        log(json_exception, 2)

def get_settings(*keys) -> "None|set[str]|any|tuple[any]":
    """
    Returns settings based on the setting key.
    This method can be used as a helper to retrieve setting information.
    @params
    keys: They key[s] to search for.\n
    If left empty, returns every existing key.\n
    If a single key is used, retuns a single value.\n
    If multiple keys are used, returns a tuple of values ordered according to the keys.\n
    If None is returned, there is no corresponding key.
    """

    if not usersettings:
        log("Settings not loaded. Use settings.load_settings() first.", 2)
        exit(1)

    if len(keys) == 0:
        return usersettings.keys()

    settings_values = (usersettings.get(key, None) for key in keys)
    return settings_values
