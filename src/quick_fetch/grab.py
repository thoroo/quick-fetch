import shutil
from urllib.parse import urlparse
import os
import pyautogui
from colorama import Fore
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import chime
from quick_fetch import logger
from .config import constants as c
from .driver import element_exist

def grab_from_mouse(mode):
    """
    Choosing mode for mouse, either directly or indirectly.
    
    Parameters:
        mode (str): String of either 'direct' or 'indirect'

    Returns:
        None    
    """
    logger.info('Input registered!')

    if mode == 'direct':
        grab_directly()
    elif mode == 'indirect':
        grab_indirectly()

def grab_url_from_mouse(button):
    """Grab URL from underneath mouse pointer"""
    pyautogui.rightClick()
    pyautogui.press(button)
    url = pyperclip.paste()
    logger.info(f'Found the following URL: {Fore.BLUE}{url}{Fore.WHITE}')
    return url

def save_file_from_url(url):
    from .main import PATH_OUTPUT, USE_SOUND

    file_name = os.path.basename(urlparse(url).path)
    file_path = f'{PATH_OUTPUT}\\{file_name}'
    
    if os.path.exists(file_path):
        logger.warning(f'{file_name} already exists at {PATH_OUTPUT}. {Fore.YELLOW}Skipping!{Fore.WHITE}')
        if USE_SOUND:
            chime.warning()
        return

    with requests.get(url, stream=True, timeout=10) as response:
        if response.ok:
            with open(file_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        del response

    logger.info(f'{Fore.GREEN}File was successfully downloaded!{Fore.WHITE}')
    if USE_SOUND:
        chime.success()

def grab_directly():
    """Interacts directly over the Chrome window and uses simple mouse and keyboard presses to grab the file/image"""
    file_url = grab_url_from_mouse('o')
    save_file_from_url(file_url)

    return

def grab_indirectly():    
    """Interacts with Chrome window and downloads file/image using an indirect way"""
    from .main import DRIVER, CONFIG

    XPATH_DOWNLOAD = CONFIG.read_xpath(c.KEY_XPATH_DOWNLOAD)
    XPATH_GATEKEEPER = CONFIG.read_xpath(c.KEY_XPATH_GATEKEEPER)

    url = grab_url_from_mouse('e')

    DRIVER.get(url)

    if element_exist(DRIVER, XPATH_GATEKEEPER):
        if XPATH_GATEKEEPER != c.KEY_EMPTY:
            WebDriverWait(DRIVER, timeout=10, poll_frequency=2).until(EC.visibility_of_element_located((By.XPATH, XPATH_GATEKEEPER))).click()
    else:
        logger.warning(f'Unable to find the following element: "{XPATH_GATEKEEPER}". {Fore.YELLOW}Skipping!{Fore.WHITE}')
        return

    WebDriverWait(DRIVER, timeout=10, poll_frequency=2).until(EC.visibility_of_element_located((By.XPATH, XPATH_DOWNLOAD)))

    file_url = DRIVER.find_element(By.XPATH, XPATH_DOWNLOAD).get_attribute('src')
    save_file_from_url(file_url)

    return