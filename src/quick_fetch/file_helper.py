 
import os
import fnmatch
from .config import constants as c

def file_exists(dir, str):
    pattern = f'{str}*'

    for file in os.listdir(dir):
        if fnmatch.fnmatch(file, pattern):
            return True
        else:
            return False


def build_filename(string1, string2):
    from .main import CONFIG

    prefix = CONFIG.read_general(c.KEY_PREFIX)
    suffix = CONFIG.read_general(c.KEY_SUFFIX)

    filename = prefix + string1 + ' (' + string2 + ')' + suffix
    return filename