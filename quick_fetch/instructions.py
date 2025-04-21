
import string
from shutil import copy
from quick_fetch import constants as const
from quick_fetch.exit_handler import clean_exit
import json5
from quick_fetch import logger

def load_instructions():
    if not const.INSTRUCTIONS_FILE.exists():
        example_file = const.INSTRUCTIONS_FILE.with_suffix('.example')

        if example_file.exists():
            copy(example_file, const.INSTRUCTIONS_FILE)
        else:
            logger.error("Example instructions file does not exist. May need to do a update / git pull")
            clean_exit()

    with open(const.INSTRUCTIONS_FILE, 'r') as file:
        data = json5.load(file)
    try:
        validate_instructions(data)
    except ValueError as e:
        logger.error(f"An error occurred during instruction validation: {str(e)}")
        clean_exit()
    
    return data

def validate_instructions(data):
    for _, value in data.items():
        for param_key, param_val in value.items():
            if not param_key in const.PARAMETERS:
                raise ValueError(f'"{param_key}" must be a key from {const.PARAMETERS}')
            if param_key == 'direct' or param_key == 'indirect':
                for action_key, action_val in param_val.items():
                    clean_action_key = action_key.rstrip(string.digits)
                    if clean_action_key != 'download':
                        if not clean_action_key in const.ACTIONS:
                            raise ValueError(f'"{clean_action_key}" must be a key from {const.ACTIONS}')
                    elif clean_action_key == 'download':
                        if isinstance(action_val, dict):
                            for download_key, download_val in param_val['download'].items():
                                if not download_key in const.DOWNLOAD_PARAM:
                                    raise ValueError(f'"{download_key}" must be a key from {const.DOWNLOAD_PARAM}')
                                if 'rename_file' in download_val:
                                    for format_key in download_val['rename_file']:
                                        if format_key not in const.FORMATS:
                                            raise ValueError(f'"{format_key}" is not a valid format key')
                    elif action_val and not action_val.startswith('//'):
                        raise ValueError(f'"{action_val}" must be XPath and start with //')