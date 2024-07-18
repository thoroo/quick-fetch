import os
import glob
import inquirer
import chime
from configparser import ConfigParser
from ast import literal_eval
from pathlib import Path
from quick_fetch import logger
from . import constants as c
from colorama import Fore

def value_range(min, max):
    return [str(x) for x in [*range(min, max + 1)]]

def create_default_config_file():
    config = ConfigParser()
    config.optionxform = str # enables case-sensitive keys

    if not c.CONFIG_FILE.exists():
        config["General"] = {"Mode": "Mouse",
                             "Unzip": False,
                             "Prefix": "",
                             "Suffix": "",
                             "ThemeSound": "big-sur",
                             "LogLevel": "INFO"}
        config["Hotkeys"] = {"Exit": "F4",
                             "DirectDownload": "F8",
                             "IndirectDownload": "F9",
                             "NextPage": "Right",
                             "PreviousPage": "Left"}
        config["Paths"] = {"OutputDirectory": os.path.join(os.getenv("USERPROFILE"), "Downloads"),
                           "ButtonNextPage": "",
                           "ButtonPreviousPage": ""}
        config["XPath"] = {"String1": "",
                           "String2": "",
                           "MoveIntoURL": "",
                           "FileDownload": "",
                           "Gatekeeper": ""}
        with open(c.CONFIG_FILE, "w") as configfile:
            config.write(configfile)

def pick_config():
    """Lets user pick config from those found in config files folder"""

    original_config_list = glob.glob('*.ini', root_dir=c.CONFIG_DIR)
    if c.CONFIG_FILE.name in original_config_list:
        original_config_list.remove(c.CONFIG_FILE.name)
        original_config_list.insert(0, c.CONFIG_FILE.name)
    new_config_list = list(map(lambda str: str.replace('.ini', ''), original_config_list))
    new_config_list = list(map(str.title, new_config_list))

    question = [
        inquirer.List(name='config',
                      message='Which config should be loaded?',
                      choices=new_config_list)
    ]

    chosen_value = next(iter(inquirer.prompt(question).values()))
    index = new_config_list.index(chosen_value)

    return c.CONFIG_DIR / original_config_list[index]

def load_config():
    """Attempts to load a config depending on how many there are in the config files folder"""

    if not c.CONFIG_DIR.exists():
        c.CONFIG_DIR.mkdir()        

    n_config = len(os.listdir(c.CONFIG_DIR))

    if  n_config == 0:
        create_default_config_file()
        conf = c.CONFIG_FILE
    elif n_config == 1:
        conf = c.CONFIG_DIR / os.listdir(c.CONFIG_DIR)[0]
    elif n_config > 1:
        conf = pick_config()

    logger.info(f"Using config file: {Fore.CYAN}{conf.name}{Fore.WHITE}")
    return QuickFetchConfig(conf)

class QuickFetchConfig(ConfigParser):
    """Provides global access to loaded configuration options as a ConfigParser subclass."""

    def __init__(self, config_file: Path | None = None) -> None:
        super(ConfigParser, self).__init__()

        if config_file:
            self.optionxform = str # enables case-sensitive keys
            self._read_config(config_file)
            #self._validate_config()
        else:
            from .main import CONFIG as config_file
       
    def _read_config(self, config_file: Path) -> None:
        """Attempt reading the config"""
        try:
            self.read(config_file)
            logger.debug(f"Read config file '{config_file}'", )
        except OSError as err:
            raise err("Error reading configuration file '%s': %s", config_file, err) from err
        
    def _validate_config(self):
        """
        Validates ConfigParser and returns errors.
        Compares a ConfigParser with a template dict or ConfigParser 
        and returns errors if there are invalid sections, invalid keys,
        or values of wrong type or value.
        """
        errors = []
        # config_get_map = {str: self.get,
        #                   int: self.getint,
        #                   float: self.getfloat,
        #                   bool: self.getboolean}
        
        for section in self.sections():
            if section not in c.VALID_VALUES.keys():
                errors.append(f'Invalid section in config: "{section}"')
                continue

            for conf_key, conf_val in self.items(section):
                if section == c.SECTION_HOTKEY:
                    conf_val = conf_val.lower()

                if conf_key not in c.VALID_VALUES[section].keys():
                    errors.append(f'Invalid key "{conf_key}" in section "{section}"')
                    continue

                if c.VALID_VALUES[section][conf_key]['required']:
                    if conf_val not in c.VALID_VALUES[section][conf_key]['values']:
                        errors.append(f'Invalid value "{conf_val}" for key "{conf_key}" in section "{section}"')

                # TODO add type validation
                # valid_val_type = type(c.VALUES_VALID[section][conf_key])
                # try:
                #     config_get_map[valid_val_type](section, conf_key)
                # except ValueError:
                #     errors.append(f'Invalid value type for key "{conf_key}" in section "{section}": "{conf_val}"')
        
        if len(errors) > 0:
            chime.error()

            for err in errors:
                logger.error(err)
           
            os._exit(0)
        
        logger.debug('Config validated successfully!')
        
    def read_general(self, key):
        """Get values for keys present in the General section of the config"""
        value = self.get(c.SECTION_GENERAL, key)

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
