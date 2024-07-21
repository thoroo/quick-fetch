
from quick_fetch import constants as const
import json5

def load_instructions():
    with open(const.INSTRUCTIONS_FILE, 'r') as file:
        data = json5.load(file)
    
    return data
