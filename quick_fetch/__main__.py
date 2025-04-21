import logging
from colorama import Fore
from colorama import init
import inquirer
import os
from quick_fetch import constants as const
from quick_fetch import logger
import quick_fetch
from quick_fetch.driver import create_driver
from quick_fetch.exit_handler import clean_exit
from quick_fetch.hotkeys import register_hotkeys
from quick_fetch.instructions import load_instructions
from quick_fetch import config
from tempfile import TemporaryDirectory

from quick_fetch.main import run
from quick_fetch.sound import setup_sound

if __name__ == '__main__':
    """Entry point of the application. All setup is done here first."""

    logger.info(f"{Fore.CYAN}QuickFetch{Fore.WHITE} {quick_fetch.__version__}")

    global CONFIG
    global TEMP_DIR
    global OUTPUT_DIR
    global DRIVER
    global USE_SOUND
    global INSTRUCTIONS

    CONFIG = config.QuickFetchConfig()
    TEMP_DIR = TemporaryDirectory()
    DRIVER = create_driver(TEMP_DIR.name)

    # helps rich logger to properly output colors
    init(convert=True)

    log_level = CONFIG.read_general(const.KEY_LOG_LEVEL)
    logging.getLogger("rich").setLevel(log_level)
    logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(log_level)

    USE_SOUND = setup_sound()

    instructions = load_instructions()

    question = [
        inquirer.List(name='section',
                       message='Which instruction should be used?',
                       choices=list(instructions.keys()))
    ]

    chosen_section = next(iter(inquirer.prompt(question).values()))

    INSTRUCTIONS = instructions.get(chosen_section)

    OUTPUT_DIR = INSTRUCTIONS.get('output')

    if '%USERPROFILE%' in OUTPUT_DIR:
        OUTPUT_DIR = OUTPUT_DIR.replace('%USERPROFILE%', os.environ['USERPROFILE'])

    logger.info(f'Output path set to: "{OUTPUT_DIR}"')

    hotkeys = CONFIG.get_section(const.SECTION_HOTKEY)
    register_hotkeys(hotkeys)

    try:
        run()
    finally:
        clean_exit()
