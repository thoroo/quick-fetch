import os
from pathlib import Path
import shutil
import time
from urllib.parse import parse_qs, urlparse

import chime
import pyperclip
import requests

from colorama import Fore

from quick_fetch import logger
from quick_fetch.file import file_exists, unzip_downloaded
from quick_fetch.page_navigator import click_on_page
from quick_fetch.exit_handler import clean_exit

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from quick_fetch.xpath import is_xpath

def download_wait(dir, timeout=120, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    Args:
        dir (str):
            The path to the folder where the files will be downloaded.
        timeout (int):
            How many seconds to wait until timing out.
        nfiles (int): defaults to None
            If provided, also wait for the expected number of files.

    """
    from __main__ import USE_SOUND

    seconds = 0
    waiting = True
    messaged = False
    
    while waiting and seconds < timeout:
        time.sleep(1)        
        seconds += 1        

        if seconds == timeout:
            logger.error(f'Checking for downloaded file has timed out after {timeout} seconds..')

            if USE_SOUND:
                chime.error()
                
            clean_exit()

        waiting = False
        files = os.listdir(dir)

        if nfiles and len(files) != nfiles:
            waiting = True

        for filename in files:
            if filename.endswith('.crdownload'):
                waiting = True

        if not messaged and len(files) > 0:
            logger.info(f'{Fore.WHITE}{Fore.BLUE}Download has started!{Fore.WHITE}')
            messaged = True

    if len(files) == 0:
        return
    else:
        logger.debug(f'{Fore.GREEN}Received downloaded file!{Fore.WHITE}')        

def download_image(url):
    from __main__ import OUTPUT_DIR
    
    file_name = os.path.basename(urlparse(url).path)
    file_path = os.path.join(OUTPUT_DIR, file_name)

    if file_exists(file_path):
        return False
    
    with requests.get(url, stream=True, timeout=10) as response:
        if response.ok:
            with open(file_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        del response

    return True

def download_file(xpath):
    from __main__ import TEMP_DIR, OUTPUT_DIR, DRIVER

    logger.debug('Attempting to download the file...')

    # attempt to get filename from URL and check if it exists
    url = WebDriverWait(DRIVER, timeout=10, poll_frequency=2).until(EC.element_to_be_clickable((By.XPATH, xpath))).get_attribute('href')

    # requires a bit more work if a file is renamed using a query
    parsed_url = urlparse(url)
    query_dict = parse_qs(parsed_url.query)
    
    if 'download' in query_dict:
        name = query_dict['download'][0]
    else:
        name = parsed_url.path

    logger.debug(f'Found the following filename from URL: {name}')

    filename = os.path.join(OUTPUT_DIR, name)
    filepath = os.path.join(OUTPUT_DIR, filename)

    if file_exists(filepath):
        return False

    click_on_page(xpath)
    download_wait(TEMP_DIR.name)

    return True

def download(type):
    from __main__ import DRIVER, TEMP_DIR, OUTPUT_DIR, USE_SOUND
    
    if type == 'image':
        url = pyperclip.paste()
        download_image(url)

    elif isinstance(type, dict):
        logger.debug('Download has sub instructions..')
        for key, value in type.items():
            if key == 'method':
                method = value
            if key == 'xpath':
                xpath = value
            if key == 'attr':
                attr = value
            if key == 'rename_file':
                for key, value in value.items():
                    if key.startswith('add_prefix'):
                        logger.warning('"add_prefix" is not implemented yet') # TODO
                        #build_filename(key, value)
                    elif key.startswith('add_suffix'):
                        logger.warning('"add_suffix" is not implemented yet') # TODO
                        #build_filename(key, value)
            

        if method == 'image' and attr:
            url = DRIVER.find_element(By.XPATH, xpath).get_attribute(attr)
            logger.debug(f'Found the following URL for download: {Fore.BLUE}{url}{Fore.WHITE}')

            if not download_image(url):
                return

        if method == 'unzip':
            click_on_page(xpath)
            download_wait(TEMP_DIR.name)
            unzip_downloaded()
    
    elif is_xpath(type):
        logger.debug(f'Download has an XPath: {type}')

        if download_file(xpath=type):
            file_path = Path(TEMP_DIR.name, os.listdir(TEMP_DIR.name)[0])
            shutil.move(src=file_path, dst=OUTPUT_DIR)
        else:
            return
    
    logger.info(f'{Fore.GREEN}File was successfully downloaded!{Fore.WHITE}')

    if USE_SOUND:
        chime.success()
