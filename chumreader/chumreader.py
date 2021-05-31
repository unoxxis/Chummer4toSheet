# Main Character Sheet Writer Routine
# Author: Boris Wezisla

import logging

# XML Reader Module
import untangle


def ReadChumFile(filename):
    # Logging
    logger = logging.getLogger('chumreader.ReadChumFile')
    logger.debug('Entering Function')

    logger.info(f"Reading character from '{filename}'")
    chumf = untangle.parse(filename)
    char = chumf.character
    logger.info(f"Loaded character with street name '{char.alias.cdata}'.")

    return char
