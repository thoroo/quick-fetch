import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pywinauto import Application

from quick_fetch import logger
from quick_fetch import constants as const
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException

def find_chrome():
    """Finds the top most Chrome application that is currently open"""
    logger.debug('Attempting to find current Chrome window')
    app = Application(backend='uia')
    app = app.connect(title_re='.*Chrome.*', class_name='Chrome_WidgetWin_1', visible_only=True, found_index=0)
    logger.debug('Found top most Chrome window!')
    return app.top_window()

def element_exist(xpath):
    """Checks whether a certain element using XPath exists on the page or note."""
    from __main__ import DRIVER

    try:
        time.sleep(0.5)
        DRIVER.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def create_driver(dir: str):
    """
    Creates a headless Chrome driver that grabs or fetches files/images in the background
    
    Args:
        dir (str): Directory to use as download location
    """
    from __main__ import CONFIG

    log_level = CONFIG.read_general(const.KEY_LOG_LEVEL)

    options = Options()
    if  log_level != 'DEBUG':
        options.add_argument('--headless=new')       
    options.add_argument(f'--log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.set_capability('browserVersion', '117')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('prefs', {
        'profile.default_content_settings.popups': 0,
        'download.default_directory': r'%s' %dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True
        })
    
    logger.debug('Created a headless Chrome driver!')
    
    return webdriver.Chrome(options=options)