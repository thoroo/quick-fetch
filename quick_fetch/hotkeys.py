
from keyboard import add_hotkey
from quick_fetch import constants as const
from quick_fetch import page_navigator
from quick_fetch.fetch import go_fetch
from quick_fetch import logger
from quick_fetch.exit_handler import clean_exit
    
def register_hotkeys(hotkeys):
    """Register hotkeys based on values present in the selected config"""
    def register_hotkey(key, callback):
        add_hotkey(key, callback, suppress=True, trigger_on_release=True)

    register_hotkey(hotkeys.get(const.KEY_EXIT), clean_exit)
    register_hotkey(hotkeys.get(const.KEY_DOWNLOAD_DIRECT), lambda: go_fetch('direct'))
    register_hotkey(hotkeys.get(const.KEY_DOWNLOAD_INDIRECT), lambda: go_fetch('indirect'))
    register_hotkey(hotkeys.get(const.KEY_NEXT_PAGE), page_navigator.get_next_page)
    register_hotkey(hotkeys.get(const.KEY_PREVIOUS_PAGE), page_navigator.get_previous_page)

    logger.debug('Hotkeys have been registered!')
