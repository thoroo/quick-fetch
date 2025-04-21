from configparser import ConfigParser
from ast import literal_eval
from shutil import copy

from quick_fetch import logger
from quick_fetch import constants as const
from quick_fetch.exit_handler import clean_exit

class QuickFetchConfig(ConfigParser):
    """Provides global access to loaded configuration options as a ConfigParser subclass."""

    def __init__(self) -> None:
        super(ConfigParser, self).__init__()

        if not const.CONFIG_FILE.exists():
            example_file = const.CONFIG_FILE.with_suffix('.example')

            if example_file.exists():
                copy(example_file, const.CONFIG_FILE)
            else:
                logger.error("Example config file does not exist. May need to do a update / git pull")
                clean_exit()

        self.optionxform = str # enables case-sensitive keys
        self._read_config()
        #self._validate_config()
       
    def _read_config(self):
        """Attempt reading the config"""
        try:
            self.read(const.CONFIG_FILE)
        except OSError as err:
            raise Exception("Error reading configuration file.. ") from err
        
    def read_general(self, key):
        """Get values for keys present in the General section of the config"""
        value = self.get(const.SECTION_GENERAL, key)

        # ensures that booleans are read as such and not as strings
        list = ['False', 'True']
        if any(element in value for element in list):
            value = literal_eval(value)    
        return value

    def read_hotkey(self, key):
        """Get values for keys present in the Hotkey section of the config"""
        return self.get(const.SECTION_HOTKEY, key)
    
    def get_section(self, section):
        """Get all items present in a section of the config"""
        return dict(self.items(section))
