# Chum File Basic Structures

import logging
import yaml


def InitializeChummerCharacter():
    """
    Initialize an empty chummer character dictionary

    Returns:
        character (dict): Character Dictionary with empty values.
    """

    # Logging
    logger = logging.getLogger('chumchar.InitializeChummerCharacter')
    logger.debug('Entering Function')

    # Generate a copy of the blank character
    with open('data/blankchar.yaml', mode='r') as fp:
        character = yaml.safe_load(fp)

    return character


def SaveCharacter(character, filename):
    """
    Save a character to a file.

    Parameters:
        character (dict): A character dict to write.
        filename (str): Path to the filename.
    """

    # Logging
    logger = logging.getLogger('chumchar.SaveCharacter')
    logger.debug('Entering Function')

    with open(filename, mode='w') as fp:
        yaml.dump(character, fp)
    logger.info(f"Saved character '{character['alias']}' to '{filename}'")


def LoadCharacter(filename):
    """
    Load a character to a file.

    Parameters:
        filename (str): Path to the filename.

    Returns
        character (dict): Character Dictionary.
    """

    # Logging
    logger = logging.getLogger('chumchar.SaveCharacter')
    logger.debug('Entering Function')

    with open(filename, mode='r') as fp:
        character = yaml.safe_load(fp)
    logger.info(f"Loaded character '{character['alias']}' from '{filename}'")

    return character
