
from quick_fetch import logger
import pyautogui
from .config import constants as c
from pyscreeze import locateOnScreen
from pyscreeze import ImageNotFoundException


def _click_on_page(key):   
    try:
        button = locateOnScreen(key, confidence=0.7)
        pyautogui.click(button)
    except ImageNotFoundException:
        logger.error('Could not locate button. Ensure they are present on screen.')

def get_next_page():
    from .main import CONFIG

    logger.debug('Moving on to next page..')
    button_image = CONFIG.read_path('NextPageImage') # TODO configparser for some reason returns the constant key as lowercase
    _click_on_page(button_image)

def get_previous_page():
    from .main import CONFIG

    logger.debug('Moving on to the previous page..')
    button_image = CONFIG.read_path('PreviousPageImage') # TODO configparser for some reason returns the constant key as lowercase
    _click_on_page(button_image)
    