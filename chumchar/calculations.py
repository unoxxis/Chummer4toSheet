# Recalculate Characters

import logging
import yaml


# Global Data Buffers, will be filled only when required
yMetatypes = None


def LoadDataFile(datacategory):
    """
    Loads a yaml datafile into the respective global variable.

    Parameters:
        datacategory (str): Which yaml file to load
    """

    # Logging
    logger = logging.getLogger('chumchar.LoadDataFile')
    logger.debug('Entering Function')

    if datacategory == 'metatypes':
        yamlfile = f'data/{datacategory}.yaml'
        with open(yamlfile, mode='r') as fp:
            global yMetatypes
            yMetatypes = yaml.safe_load(fp)
        print(f"Read Data from '{yamlfile}'")


def RecalculateCharacter(character):
    """
    Recalculate all the derived stats of a character

    Parameters:
        character (dict): Input Character

    Returns:
        character (dict): Modified and recalculated character
    """

    # Logging
    logger = logging.getLogger('chumchar.RecalculateCharacter')
    logger.debug('Entering Function')

    # ------------------------------------------------------------------
    # APPLY METATYPE
    if yMetatypes is None:
        LoadDataFile('metatypes')

    # Attributes
    for attr, vrac in yMetatypes[character['metatype']]['attribute_racials'].items():
        character['attributes'][attr]['racial'] = vrac




    return character
