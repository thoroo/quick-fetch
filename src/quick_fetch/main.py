import time
from tempfile import TemporaryDirectory
import os
import logging
import atexit
import keyboard
import chime
from quick_fetch import logger
from .config import constants as c
from .configuration import load_config
from .mode import pick_mode
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

    # TODO read mode from config instead
    MODE = pick_mode()
    CONFIG = load_config()
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

    logger.info(f"Output path set to: '{PATH_OUTPUT}'")

    atexit.register(clean_exit)

    sound_theme = CONFIG.read_general(c.KEY_SOUND)

    # TODO add disable sound to config
    # TODO log to file

    if sound_theme in chime.themes():
        chime.theme(sound_theme)
    else:
        chime.theme("big-sur")
        logger.warning('Unable to read "ThemeSound". Defaulting to "big-sur".')
        chime.warning()

    while True:
        time.sleep(0.5)
        logger.info("Awaiting input..")
        keyboard.wait()
        time.sleep(0.5)


if __name__ == "__main__":
    run()
