import logging
import os
from colorama import Fore
import quick_fetch
from quick_fetch.hotkeys import register_hotkeys
from quick_fetch.main import run
from quick_fetch import logger
from quick_fetch.configuration import load_config
from quick_fetch.driver import create_driver
from quick_fetch.exit_handler import clean_exit
from tempfile import TemporaryDirectory
from quick_fetch import constants as const
from colorama import init
import chime

if __name__ == '__main__':
    """Entry point of the application. All setup is done here first."""

    logger.info(f"{Fore.CYAN}QuickFetch{Fore.WHITE} {quick_fetch.__version__}")

    global CONFIG
    global TEMP_DIR
    global DRIVER
    global USE_SOUND

    CONFIG = load_config()
    TEMP_DIR = TemporaryDirectory()
    DRIVER = create_driver(TEMP_DIR)

    # update output path if using OS path variables, specifically %USERPROFILE%
    output_dir = CONFIG.read_path(const.KEY_OUTPUT_DIR)
    output_dir = output_dir.replace("%USERPROFILE%", os.environ.get("USERPROFILE", ""))
    CONFIG.set(section=const.SECTION_PATH, option=const.KEY_OUTPUT_DIR, value=output_dir)    

    const.RESOURCES_DIR.mkdir(parents=True, exist_ok=True)

    # helps rich logger to properly output colors
    init(convert=True)

    log_level = CONFIG.read_general(const.KEY_LOG_LEVEL)
    logging.getLogger("rich").setLevel(log_level)
    logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(log_level)

    sound_theme = CONFIG.read_general(const.KEY_SOUND).lower()

    if sound_theme != 'none':
        try:
            chime.theme(sound_theme)
        except Exception:
            logger.warning(f'{const.KEY_SOUND} is not a valid theme. Defaulting to "big-sur".')
            chime.theme('big-sur')
            chime.warning()
        
        USE_SOUND = True
    else:
        USE_SOUND = False
        logger.info('Sound has been disabled in config.')

    mode = CONFIG.read_general(const.KEY_MODE).lower()
    hotkeys = CONFIG.get_section(const.SECTION_HOTKEY)
    register_hotkeys(hotkeys, mode)    

    logger.info(f"Output path set to: {Fore.GREEN}{output_dir}{Fore.WHITE}")
    logger.info(f"Using mode: {Fore.GREEN}{mode.title()}{Fore.WHITE}")

    try:
        run()
    finally:
        clean_exit()
