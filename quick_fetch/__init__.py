import logging
import os
import platform
from rich.logging import RichHandler

logging.basicConfig(
    level='INFO',
    format='%(message)s',
    datefmt='[%X]',
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger('rich')

__version__ = "0.3.0"

if __name__ == '__main__':
    if platform.system() != 'Windows':
        logger.error('This application is currently built to run on Windows only')
        os._exit(0)