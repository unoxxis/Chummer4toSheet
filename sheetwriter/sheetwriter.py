# Main Character Sheet Writer Routine
# Author: Boris Wezisla

import logging
import pprint


def WriteCharacterSheet(char, filename):
    # Logging
    logger = logging.getLogger('sheetwriter.WriteCharacterSheet')
    logger.debug('Entering Function')

    logger.info(f'This is a test; we are trying to write a character sheet to {filename} of the following char:')
    logger.info(pprint.pformat(char))
