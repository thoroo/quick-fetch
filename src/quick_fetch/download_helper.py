import time
import os
import chime
from quick_fetch import logger
from colorama import Fore
from .exit_handler import clean_exit

def download_wait(directory, timeout=120, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
        directory : str
            The path to the folder where the files will be downloaded.
        timeout : int
            How many seconds to wait until timing out.
        nfiles : int, defaults to None
            If provided, also wait for the expected number of files.

    """
    from .main import USE_SOUND

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
        files = os.listdir(directory)

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
