from quick_fetch import logger
from quick_fetch.download import download
from quick_fetch.driver import element_exist
from quick_fetch.page_navigator import click_on_page
from quick_fetch.util_url import get_url_from_window, get_url_from_mouse, move_to_url

def go_fetch(mode):
    from __main__ import INSTRUCTIONS
    logger.info('Input registered!')

    set = INSTRUCTIONS.get(mode)
    logger.debug(f"Instructions are:\n{set}")

    for key, value in set.items():
        if key.startswith('click'):
            click_on_page(value)
        elif key.startswith('url_from_mouse'):
            get_url_from_mouse(value)
        elif key.startswith('url_from_window'):
            get_url_from_window()
        elif key.startswith('move_to_url'):
            move_to_url()
        elif key.startswith('gatekeeper'):
            if element_exist(value):
                click_on_page(value)
        elif key.startswith('download'):
            download(value)
