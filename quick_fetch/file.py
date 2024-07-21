import os
from pathlib import Path
import shutil
from zipfile import ZipFile

from colorama import Fore
from quick_fetch import constants as const
from quick_fetch import logger
import chime

def file_exists(file_path):
    from __main__ import USE_SOUND    

    if os.path.exists(file_path):
        logger.warning('File already exists! Skipping..')
        if USE_SOUND:
            chime.warning()
        return True
    else:
        return False

def build_filename(str):
    from __main__ import CONFIG

    prefix = CONFIG.read_general(const.KEY_PREFIX)
    suffix = CONFIG.read_general(const.KEY_SUFFIX)

    filename = prefix + str + suffix
    return filename

def is_downloaded():
    from __main__ import TEMP_DIR, USE_SOUND

    if len(os.listdir(TEMP_DIR.name)) == 0:
        logger.error(f'Download was not able to start! Most likely a {Fore.RED}"404 Not Found"{Fore.WHITE}. {Fore.YELLOW}Skipping!{Fore.WHITE}')
        if USE_SOUND:
            chime.error()
        return False
    else:
        return True
    
def get_downloaded_file():
    from __main__ import TEMP_DIR
    return Path(TEMP_DIR.name, os.listdir(TEMP_DIR.name)[0])
    
def unzip_downloaded():
    from __main__ import TEMP_DIR, OUTPUT_DIR

    file = get_downloaded_file()
    source_dir = Path(TEMP_DIR.name, file.stem)
    dest_dir = Path(OUTPUT_DIR, file.stem)

    os.mkdir(file.parent)

    with ZipFile(file, 'r') as zObject:
        zObject.extractall(source_dir)
            
    shutil.copytree(source_dir, dest_dir)

    # remove all files in temp folder
    for root, dirs, files in os.walk(TEMP_DIR.name):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))

def move_downloaded():
    from __main__ import TEMP_DIR, OUTPUT_DIR
    shutil.move(src=TEMP_DIR, dst=OUTPUT_DIR)