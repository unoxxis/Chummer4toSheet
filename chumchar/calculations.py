# Recalculate Characters

import logging
import yaml
import copy
import math

from .improvement_handling import ScanImprovements


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


# Global Data Buffers, will be filled only when required
global yMetatypes
LoadDataFile('metatypes')


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
    # Racial Improvements
    for key, improvement in yMetatypes[character['metatype']]['improvements'].items():
        character['improvements'][key] = copy.copy(improvement)

    # ------------------------------------------------------------------
    # Qualities
    logger.debug('Calculating qualities...')

    # Racial Qualities
    for quality, qdata in yMetatypes[character['metatype']]['qualities'].items():
        character['qualities'][quality] = copy.copy(qdata)

    # ------------------------------------------------------------------
    # Qualities
    logger.debug('Calculating qualities...')

    # ------------------------------------------------------------------
    # Powers
    logger.debug('Calculating powers...')

    # Racial Powers
    logger.warning('Powers are not yet in!')


    # Here go Augments, Items, Lifestyle...


    # ------------------------------------------------------------------
    # Calculate Attributes
    logger.debug('Calculating attributes...')
    for attr in character['attributes'].keys():
        vrac = yMetatypes[character['metatype']]['attribute_racials'].get(attr, 0)
        character['attributes'][attr]['racial'] = vrac

        if (attr == 'MAG' and not ScanImprovements(character['improvements'], itype='special', ieffect='enable_magic')) \
            or (attr == 'RES' and not ScanImprovements(character['improvements'], itype='special', ieffect='enable_resonance')):
            character['attributes'][attr]['augment_max'] = 0
            character['attributes'][attr]['actual'] = 0
        # Max Value
        vmax = 6
        vmax += vrac
        vmax += ScanImprovements(character['improvements'], itype='attribute', iattribute=attr, iproperty='augment_max')

        vmax = int(math.floor(vmax * 1.5))
        character['attributes'][attr]['augment_max'] = vmax

        # Augmented value
        vaug = ScanImprovements(character['improvements'], itype='attribute', iattribute=attr, iproperty='augment')
        character['attributes'][attr]['augment'] = vaug

        # Actual value
        vact = character['attributes'][attr]['natural'] + character['attributes'][attr].get('racial', 0)
        vact += vaug
        if vact > vmax:
            logger.warning(f"Actual attribute value for {attr} is higher then allowed augmented max!")
            vact = vmax
        character['attributes'][attr]['actual'] = vact

    # Here goes: Skill calculation


    # ------------------------------------------------------------------
    # Calculate Derived Values
    logger.debug('Calculating derived values...')

    # Movement
    character['derived']['movement'] = copy.deepcopy(yMetatypes[character['metatype']]['movement'])

    # Reach
    character['derived']['reach'] = ScanImprovements(character['improvements'], itype='derived', iproperty='reach')

    # Armor
    character['derived']['armor'] = {
        'ballistic': ScanImprovements(character['improvements'], itype='derived', iproperty='armor_ballistic'),
        'impact': ScanImprovements(character['improvements'], itype='derived', iproperty='armor_impact')
    }

    return character
