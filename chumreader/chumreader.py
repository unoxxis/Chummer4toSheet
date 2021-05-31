# Chum File XML Reader
# Author: Boris Wezisla

import logging

# XML Reader Module
import untangle


def ReadChumFile(filename):
    """
    Read a Chummer chum file and return an untangle object containing th character node.

    Parameters:
        filename (str): path to the cummer file.

    Returns:
        char (untangle.Element): character node of the Chummer character
            (that is currently the only node in a chum file beneath the root node)
    """

    # Logging
    logger = logging.getLogger('chumreader.ReadChumFile')
    logger.debug('Entering Function')

    logger.info(f"Reading character from '{filename}'")
    chumf = untangle.parse(filename)
    char = chumf.character
    logger.info(f"Loaded character with street name '{char.alias.cdata}'.")

    return char
