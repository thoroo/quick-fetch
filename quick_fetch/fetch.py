
import shutil
from zipfile import ZipFile
from .driver import find_chrome
from .driver import element_exist
import os
import chime
from colorama import Fore
from pathlib import Path
from quick_fetch import logger
from .config import constants as c
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .download_helper import download_wait
from .file_helper import build_filename
from glob import glob
import re

def go_fetch(mode):
    logger.info('Input registered!')

    if mode == 'direct':
        fetch_directly()
    elif mode == 'indirect':
        fetch_indirectly()

def fetch_directly():
    from .main import USE_SOUND

    logger.debug('Fetching file indirectly..')
    logger.error(f'{Fore.YELLOW}Fetching file indirectly is currently not implemented!{Fore.WHITE}')

    if USE_SOUND:
        chime.error()

def fetch_indirectly():    
    from .main import DRIVER, CONFIG, PATH_OUTPUT, PATH_TEMP, USE_SOUND
    
    logger.debug('Fetching file directly..')

    UNZIP = CONFIG.read_general(c.KEY_UNZIP)

    XPATH_STRING1 = CONFIG.read_xpath(c.KEY_XPATH_STRING1)
    XPATH_STRING2 = CONFIG.read_xpath(c.KEY_XPATH_STRING2)
    XPATH_DOWNLOAD = CONFIG.read_xpath(c.KEY_XPATH_DOWNLOAD)
    XPATH_NEXT_URL = CONFIG.read_xpath(c.KEY_XPATH_NEXT_URL)
    
    current_chrome = find_chrome()
    url = 'https://' + current_chrome.child_window(title='Address and search bar', control_type='Edit').get_value()
    logger.info(f'Found the following URL: {Fore.BLUE}{url}{Fore.WHITE}')

    DRIVER.get(url)
    WebDriverWait(DRIVER, timeout=10, poll_frequency=2).until(EC.presence_of_element_located((By.XPATH, XPATH_NEXT_URL)))

    if element_exist(DRIVER, XPATH_STRING1):        
        string1 = DRIVER.find_element(By.XPATH, XPATH_STRING1).text.title()
        string1 = re.sub(r' /.*', '', string1)

        if element_exist(DRIVER, XPATH_STRING2):
            string2 = DRIVER.find_element(By.XPATH, XPATH_STRING2).text
        else:
            logger.warning('Unable to find XPath for "String2". {Fore.YELLOW}Skipping!{Fore.WHITE}')
            string2 = ''

    else:
        logger.warn(f'Unable to find the following element: "{XPATH_STRING1}". {Fore.YELLOW}Skipping!{Fore.WHITE}')
        return
    
    string_meta = f'{string1} ({string2})'
    reserved_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    string_meta = string_meta.translate({ord(char): '' for char in reserved_chars})

    logger.info(f'Found the following metadata: {Fore.YELLOW}"{string_meta}"{Fore.WHITE}')
            
    file_name = build_filename(string_meta)

    if UNZIP:
        ext = ''
    else:
        ext = '.*'
        
    if len(glob(os.path.join(PATH_OUTPUT, file_name + ext))) > 0:
        logger.warning(f'Target file already exists in output folder! {Fore.RED}Skipping!{Fore.WHITE}')
        if USE_SOUND:
            chime.warning()
        return

    url_next = DRIVER.find_element(By.XPATH, XPATH_NEXT_URL).get_attribute('href')

    DRIVER.get(url_next)
                    
    WebDriverWait(DRIVER, 20).until(EC.element_to_be_clickable((By.XPATH, XPATH_DOWNLOAD))).click()
    download_wait(PATH_TEMP.name)

    if len(os.listdir(PATH_TEMP.name)) == 0:
        logger.error(f'Download was not able to start! Most likely a {Fore.RED}"404 Not Found"{Fore.WHITE}. {Fore.YELLOW}Skipping!{Fore.WHITE}')
        if USE_SOUND:
            chime.error()
        return

    file_in = Path(PATH_TEMP.name, os.listdir(PATH_TEMP.name)[0])
    file_out = file_in.parent/(file_name + file_in.suffix)
    file_in.rename(file_out)

    path_source_dir = os.path.join(PATH_TEMP.name, file_out.stem)
    path_destination_dir = os.path.join(PATH_OUTPUT, file_out.stem)

    logger.info(f'{Fore.GREEN}File was successfully downloaded!{Fore.WHITE}')

    if UNZIP:
        os.mkdir(path_source_dir)

        with ZipFile(file_out, 'r') as zObject:
            zObject.extractall(path_source_dir)
                
        shutil.copytree(path_source_dir, path_destination_dir)
            
    else: 
        shutil.move(file_out, PATH_OUTPUT)

    for object_name in os.listdir(PATH_TEMP.name):
        object = os.path.join(PATH_TEMP.name, object_name)

        if os.path.isfile(object):
            os.remove(object)
        else:
            try:
                shutil.rmtree(object, ignore_errors=True)
            except:
                logger.error(f'Unable to delete folder: "{object}"')

    logger.info(f'{Fore.GREEN}And file has been unzipped!{Fore.WHITE}')

    if USE_SOUND:
        chime.success()
