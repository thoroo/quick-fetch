from quick_fetch import logger
from os import _exit

def clean_exit():
    from __main__ import DRIVER, TEMP_DIR

    DRIVER.quit()
    TEMP_DIR.cleanup()
    logger.info('QuickFetch has cleaned up after itself')
    _exit(0)
    