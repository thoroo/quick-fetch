import time
import keyboard
from quick_fetch import logger

def run():
    """Main function to run the application"""
    try:
        while True:
            time.sleep(0.5)
            logger.info("Awaiting input..")
            keyboard.wait()

    except KeyboardInterrupt:
        logger.info("Quitting due to keyboard interrupt..")
        return
