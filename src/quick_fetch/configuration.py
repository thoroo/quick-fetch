import os
import shutil
import glob
import inquirer
import chime
import logging
import configchecker as checker
import keyboard
from pyautogui import KEYBOARD_KEYS
from configparser import ConfigParser
from colorama import Fore
from ast import literal_eval
from pathlib import Path
from quick_fetch import logger
from .config import constants as c

CONFIG_DIR_PATH = os.path.join(Path(__file__).parent.parent.parent, c._CONFIG_DIR)

def value_range(min, max):
    return [str(x) for x in [*range(min, max + 1)]]

def pick_config():
    """Lets user pick config from those found in config files folder"""

    original_config_list = glob.glob('*.ini', root_dir=CONFIG_DIR_PATH)
    index_default = original_config_list.index(c._CONFIG_FILE)
    original_config_list.insert(0, original_config_list.pop(index_default))
    new_config_list = list(map(lambda str: str.replace('.ini', ''), original_config_list))
    new_config_list = list(map(str.title, new_config_list))

    question = [
        inquirer.List(name='config',
                      message='Which config should be loaded?',
                      choices=new_config_list)
    ]

    chosen_value = next(iter(inquirer.prompt(question).values()))
    index = new_config_list.index(chosen_value)

    return os.path.join(CONFIG_DIR_PATH, original_config_list[index])

def load_config():
    """Attempts to load a config depending on how many there are in the config files folder"""
    n_config = len(os.listdir(CONFIG_DIR_PATH))

    if n_config > 1:
        conf = pick_config()

    elif  n_config < 0:
        logger.error('Missing config files! Recreating default config..')
        QuickFetchConfig()._recreate_default_file()
        n_config = 1

    elif n_config == 1:
        conf = os.listdir(c._CONFIG_DIR)[0]

    return QuickFetchConfig(conf)

class QuickFetchConfig(ConfigParser):
    """Provides global access to loaded configuration options as a ConfigParser subclass."""

    def __init__(self, config_file: Path | None = None) -> None:
        super(ConfigParser, self).__init__()

        if config_file:
            self._read_config(config_file)
            #self._validate_config()
        else:
            from .main import CONFIG as config_file

    def _recreate_default_file(self) -> None:
        """If no config file is found, default to internal config and recreate."""
        try:
            shutil.copyfile('./src/quick_fetch/config/default.ini', './config_files/default.ini') #TODO fix paths
            logger.log("Recreated default config.ini in './config_files/'")
        except OSError as err:
            raise err("Error in recreating internal default to './config_files/") from err
        
    def _read_config(self, config_file: Path) -> None:
        """Attempt reading the config"""
        try:
            self.read(config_file)
            logger.debug(f"Read config file '{config_file}'", )
        except OSError as err:
            raise err("Error reading configuration file '%s': %s", config_file, err) from err
        
    def _validate_config(self) -> None:
        """Validate the values present in the config file"""

        log_levels = '(' + '|'.join(logging.getLevelNamesMapping().keys()) + ')'
        keyboard_keys = '(' + '|'.join(KEYBOARD_KEYS) + ')'
        sound_themes = '(' + '|'.join(chime.themes()) + ')'
        schema = checker.ConfigSchema()
            
        try:
            with schema.section(c.SECTION_GENERAL) as section:
                section.value(key_val=c.KEY_MODE, value_val=checker.ItemRegexValidator('(Mouse|XPath)'))
                section.value(key_val=c.KEY_UNZIP, value_val=checker.ItemRegexValidator('(True|False)'))
                section.value(key_val=checker.ItemRegexValidator(r'.*.fix'), required=False)
                section.value(key_val=c.KEY_SOUND, value_val=checker.ItemRegexValidator(sound_themes))
                section.value(key_val=c.KEY_LOG_LEVEL, value_val=checker.ItemRegexValidator(log_levels)).no_other()

            with schema.section(c.SECTION_HOTKEY) as section:
                section.value(key_val=checker.ItemRegexValidator(r'.*(Exit|Download)'), 
                            value_val=checker.ItemRegexValidator(keyboard_keys), required=True)
                section.value(key_val=checker.ItemRegexValidator(r'.*(Scroller|Page)'), 
                            value_val=checker.ItemRegexValidator(keyboard_keys), required=False).no_other()

            with schema.section(c.SECTION_PATH) as section:
                pass

            with schema.section(c.SECTION_XPATH) as section:
                pass

            schema.no_other()
            checker.ConfigSchemaValidator(schema).validate(self)

        except:
            # TODO make it more informative
            logger.error(f'Config has invalid keys, values or structure. {Fore.RED}Exiting!{Fore.WHITE}')
            os._exit(0)
        
    def read_general(self, key):
        """Get values for keys present in the General section of the config"""
        value = self[c.SECTION_GENERAL][key]

        # ensures that booleans are read as such and not as strings
        list = ['False', 'True']
        if any(element in value for element in list):
            value = literal_eval(value)    
        return value

    def read_hotkey(self, key):
        """Get values for keys present in the Hotkey section of the config"""
        return self.get(c.SECTION_HOTKEY, key)

    def read_path(self, key):
        """Get values for keys present in the Path section of the config"""
        return self.get(c.SECTION_PATH, key)

    def read_xpath(self, key):
        """Get values for keys present in the XPath section of the config"""
        return self.get(c.SECTION_XPATH, key)
    
    def get_section(self, section):
        """Get all items present in a section of the config"""
        return dict(self.items(section))
