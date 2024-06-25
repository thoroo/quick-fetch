
import pyperclip
import pyautogui
import chime
from urllib.parse import urlparse
from quick_fetch import logger
from pyscreeze import locateOnScreen
from pyscreeze import ImageNotFoundException


def _click_on_page(image):
    """
    Clicks on page for URL redirect and checks for hostname mismatches.
    
    Args:
        image (Path): A image of the button to be clicked.

    Return:
        None
    """
    try:
        button = locateOnScreen(image, confidence=0.7)

        # selects address bar and then copies the current URL
        pyautogui.hotkey('ctrl', 'l')
        pyautogui.hotkey('ctrl', 'c')
        current_url = pyperclip.paste()

        # copies the URL from the button
        pyautogui.dragTo(button)
        pyautogui.hotkey('ctrl', 'c')
        button_url = pyperclip.paste()

        current_host = urlparse(current_url)
        button_host = urlparse(button_url)

        if current_host != button_host:
            logger.error('Hostname mismatch for current window and button URL. Check manually the intended button.')
            chime.error()
            return
        
        pyautogui.click(button)

    except ImageNotFoundException:
        logger.error('Could not locate button. Ensure they are present on screen.')

def get_next_page():
    """Presses the button for the next page/URL"""
    from .main import CONFIG

    logger.debug('Moving on to next page..')
    button_image = CONFIG.read_path('NextPageImage') # TODO configparser for some reason returns the constant key as lowercase
    _click_on_page(button_image)

def get_previous_page():
    """Presses the button for the previous page/URL"""
    from .main import CONFIG

    logger.debug('Moving on to the previous page..')
    button_image = CONFIG.read_path('PreviousPageImage') # TODO configparser for some reason returns the constant key as lowercase
    _click_on_page(button_image)
    