from colorama import Fore
import quick_fetch
from quick_fetch.main import run
from quick_fetch import logger

if __name__ == '__main__':
    logger.info(f"{Fore.CYAN}QuickFetch{Fore.WHITE} {quick_fetch.__version__}")
    run()
