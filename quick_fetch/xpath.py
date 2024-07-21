import re
from colorama import Fore
from quick_fetch import logger
from quick_fetch.driver import element_exist
from quick_fetch.file import build_filename
from selenium.webdriver.common.by import By

def build_name_from_xpath(DRIVER, XPATH_STRING1, XPATH_STRING2):

    if element_exist(DRIVER, XPATH_STRING1):        
        string1 = DRIVER.find_element(By.XPATH, XPATH_STRING1).text.title()
        string1 = re.sub(r' /.*', '', string1)

    else:
        logger.warn(f'Unable to find the following element: "{XPATH_STRING1}". {Fore.YELLOW}Skipping!{Fore.WHITE}')
        return
    
    if element_exist(DRIVER, XPATH_STRING2):
        string2 = DRIVER.find_element(By.XPATH, XPATH_STRING2).text
    else:
        logger.warning('Unable to find XPath for "String2". {Fore.YELLOW}Skipping!{Fore.WHITE}')
        string2 = ''

    string_meta = f'{string1} ({string2})'
    # remove reserved characters
    reserved_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    string_meta = string_meta.translate({ord(char): '' for char in reserved_chars})

    logger.info(f'Found the following metadata: {Fore.YELLOW}"{string_meta}"{Fore.WHITE}')
        
    return build_filename(string_meta)

# a crude check to see if the xpath is potentially valid
def is_xpath(xpath):
    if xpath.startswith('//'):
        return True
    else:
        return False