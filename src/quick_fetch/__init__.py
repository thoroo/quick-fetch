import logging
from rich.logging import RichHandler
from colorama import Fore

logging.basicConfig(
    level='INFO', #TODO read log level from config
    format='%(message)s',
    datefmt='[%X]',
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger('rich')

__version__ = "0.1.0"