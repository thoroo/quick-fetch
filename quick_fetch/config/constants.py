import chime
import logging

_CONFIG_FILE = 'default.ini'
_CONFIG_DIR = 'config_files'
_INTERNAL_CONFIG_FILE = "default.ini"

SECTION_GENERAL = 'General'
KEY_MODE = 'Mode'
KEY_UNZIP = 'Unzip'
KEY_PREFIX = 'Prefix'
KEY_SUFFIX = 'Suffix'
KEY_SOUND = 'ThemeSound'
KEY_LOG_LEVEL = 'LogLevel'

SECTION_HOTKEY = 'Hotkeys'
KEY_EXIT = 'Exit'
KEY_DOWNLOAD_DIRECT = 'DirectDownload'
KEY_DOWNLOAD_INDIRECT = 'IndirectDownload'
KEY_NEXT_PAGE = 'NextPage'
KEY_PREVIOUS_PAGE = 'PreviousPage'

SECTION_PATH = 'Paths'
KEY_OUTPUT_DIR = 'OutputDirectory'
KEY_NEXT_PAGE_IMG = 'ButtonNextPage'
KEY_PREVIOUS_PAGE_IMG = 'ButtonPreviousPage'

SECTION_XPATH = 'XPath'
KEY_XPATH_STRING1 = 'String1'
KEY_XPATH_STRING2 = 'String2'
KEY_XPATH_NEXT_URL = 'MoveIntoURL'
KEY_XPATH_DOWNLOAD = 'FileDownload'
KEY_XPATH_GATEKEEPER = 'Gatekeeper'

KEY_EMPTY = ''

KEYBOARD_KEYS = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "altleft",
    "altright",
    "backspace",
    "capslock",
    "ctrlleft",
    "ctrlright",
    "del",
    "delete",
    "down",
    "f1",
    "f10",
    "f11",
    "f12",
    "f13",
    "f14",
    "f15",
    "f16",
    "f17",
    "f18",
    "f19",
    "f2",
    "f20",
    "f21",
    "f22",
    "f23",
    "f24",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "home",
    "left",
    "num0",
    "num1",
    "num2",
    "num3",
    "num4",
    "num5",
    "num6",
    "num7",
    "num8",
    "num9",
    "numlock",
    "pagedown",
    "pageup",
    "pause",
    "pgdn",
    "pgup",
    "printscreen",
    "prntscrn",
    "prtsc",
    "prtscr",
    "return",
    "right",
    "shift",
    "shiftleft",
    "shiftright",
    "space",
    "up",
    "win",
    "winleft",
    "winright"
]

VALID_VALUES = {
    SECTION_GENERAL: {
        KEY_MODE: {'values': ['Mouse', 'XPath'], 'required': True},
        KEY_UNZIP: {'values': ['True', 'False'], 'required': True},
        KEY_PREFIX: {'values': [], 'required': False},
        KEY_SUFFIX: {'values': [], 'required': False},
        KEY_SOUND: {'values': chime.themes(), 'required': True},
        KEY_LOG_LEVEL: {'values': list(logging.getLevelNamesMapping().keys()), 'required': True}
    },
    SECTION_HOTKEY: {
        KEY_EXIT: {'values': KEYBOARD_KEYS, 'required': True},
        KEY_DOWNLOAD_DIRECT: {'values': KEYBOARD_KEYS, 'required': True},
        KEY_DOWNLOAD_INDIRECT: {'values': KEYBOARD_KEYS, 'required': False},
        KEY_NEXT_PAGE: {'values': KEYBOARD_KEYS, 'required': False},
        KEY_PREVIOUS_PAGE: {'values': KEYBOARD_KEYS, 'required': False}
    },
    SECTION_PATH: {
        KEY_OUTPUT_DIR: {'values': [], 'required': False},
        KEY_NEXT_PAGE_IMG: {'values': [], 'required': False},
        KEY_PREVIOUS_PAGE_IMG: {'values': [], 'required': False},
    },
    SECTION_XPATH: {
        KEY_XPATH_STRING1: {'values': [], 'required': False},
        KEY_XPATH_STRING2: {'values': [], 'required': False},
        KEY_XPATH_NEXT_URL: {'values': [], 'required': False},
        KEY_XPATH_DOWNLOAD: {'values': [], 'required': False},
        KEY_XPATH_GATEKEEPER: {'values': [], 'required': False}
    }
}