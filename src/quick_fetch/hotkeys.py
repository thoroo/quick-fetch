
from keyboard import add_hotkey
from .config import constants as c
from . import page_navigator
from .grab import grab_from_mouse
from .fetch import go_fetch
from quick_fetch import logger
from .exit_handler import clean_exit
    
def register_hotkeys():
    """Register hotkeys based on values present in the selected config"""
    from .main import CONFIG, MODE

    hotkeys = CONFIG.get_section(c.SECTION_HOTKEY)
    if MODE == 'mouse':
        download_function = grab_from_mouse
    elif MODE == 'xpath':
        download_function = go_fetch
    
    # TODO if any hotkey is empty then return null function

    add_hotkey(hotkeys.get(c.KEY_EXIT.lower()),
               clean_exit,
               suppress=True,
               trigger_on_release=True)

    add_hotkey(hotkeys.get(c.KEY_DOWNLOAD_DIRECT.lower()), 
               lambda: download_function('direct'),
               suppress=True,
               trigger_on_release=True)

    add_hotkey(hotkeys.get(c.KEY_DOWNLOAD_INDIRECT.lower()),
               lambda: download_function('indirect'),
               suppress=True,
               trigger_on_release=True)

    add_hotkey(hotkeys.get(c.KEY_NEXT_PAGE.lower()),
               page_navigator.get_next_page,
               suppress=True,
               trigger_on_release=True)

    add_hotkey(hotkeys.get(c.KEY_PREVIOUS_PAGE.lower()),
               page_navigator.get_previous_page,
               suppress=True,
               trigger_on_release=True)
    
    logger.debug('Hotkeys have been registered!')
