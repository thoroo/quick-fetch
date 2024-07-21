from quick_fetch import logger
from quick_fetch import constants as const
import chime

def setup_sound():
    from __main__ import CONFIG

    sound_theme = CONFIG.read_general(const.KEY_SOUND).lower()

    if sound_theme != 'none':
        try:
            chime.theme(sound_theme)
        except Exception:
            logger.warning(f'{const.KEY_SOUND} is not a valid theme. Defaulting to "big-sur".')
            chime.theme('big-sur')
            chime.warning()
        
        return True
    else:
        logger.info('Sound has been disabled in config.')
        return False