import time
from tempfile import TemporaryDirectory
import os
import logging
import atexit
import keyboard
import chime
from colorama import Fore
from quick_fetch import logger
from quick_fetch import constants as c
from .configuration import load_config
from .hotkeys import register_hotkeys
from .driver import create_driver
from .exit_handler import clean_exit

def run():
    """Main function to run the application"""
    
    global MODE
    global CONFIG
    global PATH_OUTPUT
    global PATH_TEMP
    global DRIVER
    global USE_SOUND

    CONFIG = load_config()
    MODE = CONFIG.read_general(c.KEY_MODE).lower()

    if not c.RESOURCES_DIR.exists():
        c.RESOURCES_DIR.mkdir()

    register_hotkeys()

    PATH_TEMP = TemporaryDirectory()
    DRIVER = create_driver(PATH_TEMP)
    path_output = CONFIG.read_path(c.KEY_OUTPUT_DIR)

    log_level = CONFIG.read_general(c.KEY_LOG_LEVEL)
    logging.getLogger("rich").setLevel(log_level)
    logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(log_level)

    if "%USERPROFILE%" in path_output:
        PATH_OUTPUT = path_output.replace("%USERPROFILE%", os.environ["USERPROFILE"])
    else:
        PATH_OUTPUT = path_output

    logger.info(f"Output path set to: {Fore.GREEN}{PATH_OUTPUT}{Fore.WHITE}")
    logger.info(f"Using mode: {Fore.GREEN}{MODE.title()}{Fore.WHITE}")

    atexit.register(clean_exit)

    sound_theme = CONFIG.read_general(c.KEY_SOUND)

    # TODO log to file

    if sound_theme.lower() != 'none':
        USE_SOUND = True
        try:
            chime.theme(sound_theme)
        except:
            logger.warning(f'Unable to read {c.KEY_SOUND}. Defaulting to "big-sur".')
            chime.theme('big-sur')
            chime.warning()
    else:
        USE_SOUND = False
        logger.info('Sound has been disabled in config.')

    while True:
        time.sleep(0.5)
        logger.info("Awaiting input..")
        keyboard.wait()
        time.sleep(0.5)

if __name__ == "__main__":
    run()
