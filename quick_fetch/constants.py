from pathlib import Path

SETTINGS_DIR = Path.cwd() / 'settings'
CONFIG_FILE = SETTINGS_DIR / 'config.ini'
INSTRUCTIONS_FILE = SETTINGS_DIR / 'instructions.json5'

SECTION_GENERAL = 'General'
KEY_MODE = 'Mode'
KEY_SOUND = 'ThemeSound'
KEY_LOG_LEVEL = 'LogLevel'

SECTION_HOTKEY = 'Hotkeys'
KEY_EXIT = 'Exit'
KEY_DOWNLOAD_DIRECT = 'DirectDownload'
KEY_DOWNLOAD_INDIRECT = 'IndirectDownload'
KEY_NEXT_PAGE = 'NextPage'
KEY_PREVIOUS_PAGE = 'PreviousPage'

MODES = [
    'direct',
    'indirect'
]

ACTIONS = [
    'click',
    'gatekeeper',
    'url_from_mouse',
    'url_from_window',
    'move_to_url',
    'download'
]

FORMATS = [    
    'format',
    'add-prefix',
    'add-suffix'
]

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