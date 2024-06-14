

from quick_fetch import logger
from os import _exit

def clean_exit():    
    from .main import DRIVER, PATH_TEMP

    DRIVER.quit()
    PATH_TEMP.cleanup()
    logger.info('QuickFetch has cleaned up after itself')
    _exit(0)