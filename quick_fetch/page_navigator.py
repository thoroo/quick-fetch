import pyperclip
import pyautogui
import chime
from urllib.parse import urlparse
from colorama import Fore

from quick_fetch import logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_navigator(image):
    """
    Clicks on page for URL redirect and checks for hostname mismatches.

    Args:
        image (Path): A image of the button to be clicked.
    """
    try:
        button = pyautogui.locateOnScreen(image, confidence=0.7)

        # selects address bar and then copies the current URL
        pyautogui.hotkey('ctrl', 'l')
        pyautogui.hotkey('ctrl', 'c')
        current_url = pyperclip.paste()

        # copies the URL from the button
        pyautogui.dragTo(button)
        pyautogui.hotkey('ctrl', 'c')
        button_url = pyperclip.paste()
        button_url = pyperclip.paste()

        current_host = urlparse(current_url)
        button_host = urlparse(button_url)

        if current_host != button_host:
            logger.error(
                'Hostname mismatch for current window and button URL. '
                'Check manually the intended button.')
            chime.error()
            return

        pyautogui.click(button)

    except pyautogui.ImageNotFoundException:
        logger.error('Could not locate button. Ensure it is present on screen.')
    
def click_on_page(xpath):
    from __main__ import DRIVER
    logger.debug(f'Clicking on the following element: {Fore.BLUE}{xpath}{Fore.WHITE}')
    WebDriverWait(DRIVER, timeout=10, poll_frequency=2).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

def get_next_page():
    """Presses the button for the next page/URL"""
    from __main__ import CONFIG

    logger.debug('Moving on to next page..')
    click_navigator(CONFIG.read_path('NextPageImage'))


def get_previous_page():
    """Presses the button for the previous page/URL"""
    from __main__ import CONFIG

    logger.debug('Moving on to the previous page..')
    click_navigator(CONFIG.read_path('PreviousPageImage'))
