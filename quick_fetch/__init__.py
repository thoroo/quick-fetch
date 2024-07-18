import logging
from rich.logging import RichHandler

logging.basicConfig(
    level='INFO',
    format='%(message)s',
    datefmt='[%X]',
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger('rich')

__version__ = "0.2.0"