import time
import pyautogui
import pyperclip
import validators
import chime

from colorama import Fore
from quick_fetch import logger
from quick_fetch.driver import find_chrome

def get_mapped_key(type):
    key_mapping = {
        'image': 'o',
        'link': 'e'
    }
    return key_mapping.get(type)

def is_valid_url(url):
    from __main__ import USE_SOUND
    if validators.url(url):        
        logger.info(f'Found the following URL: {Fore.BLUE}{url}{Fore.WHITE}')
        return True
    else:
        logger.error(f'Could not find a valid URL!')
        if USE_SOUND:
            chime.warning()
        return False

def get_url_from_mouse(type):
    """Grab URL from underneath mouse pointer"""
    key = get_mapped_key(type)

    pyautogui.rightClick()
    pyautogui.press(key)
    url = pyperclip.paste()

    if is_valid_url(url):
        return url

    return None

def get_url_from_window():
    pyautogui.hotkey('altleft', 'd')
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'c')
    url = pyperclip.paste()

    if is_valid_url(url):
        logger.debug('URL is valid')
        return url

    return None

def get_url_from_chrome_window():
    current_chrome = find_chrome()
    url = 'https://' + current_chrome.child_window(title='Address and search bar', control_type='Edit').get_value()
    logger.info(f'Found the following URL: {Fore.BLUE}{url}{Fore.WHITE}')

    if is_valid_url(url):
        return url

    return None

def move_to_url():
    from __main__ import DRIVER
    url = pyperclip.paste()
    logger.debug(f'Found the following URL for moving to: {Fore.BLUE}{url}{Fore.WHITE}')
    DRIVER.get(url)