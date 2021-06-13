# Import original Chummer *.chum files

import untangle
import logging

from .charfiles import InitializeChummerCharacter
from .calculations import RecalculateCharacter

_CHUM_MIN_VERSION = 490     # Minimum Chummer Version


def ImportChummerCharacter(filename):
    """
    Import a character from the original Chummer program.

    Parameters:
        filename (str): Path to chummer file.

    Returns:
        character (dict): A character dictionary
    """

    # Logging
    logger = logging.getLogger('chumchar.ImportChummerCharacter')
    logger.debug('Entering Function')

    logger.info(f"Reading original Chummer character from '{filename}'")
    chumf = untangle.parse(filename)
    xmldata = chumf.character
    logger.info(f"Loaded character with street name '{xmldata.alias.cdata}'.")

    try:
        logger.debug('Chummer Version of XML data: '
                     f'{xmldata.appversion.cdata}')
        if int(xmldata.appversion.cdata) < _CHUM_MIN_VERSION:
            raise ValueError(
                'Stored XML data is from a too old Chummer version. '
                f'Please update at least to version {_CHUM_MIN_VERSION}!'
            )
    except AttributeError:
        logger.error('XML data seems not to be a chummer file!')
        raise

    # Initialize Basic Character, the rest will then be overwritten
    character = InitializeChummerCharacter()

    # General Information
    character['alias'] = xmldata.alias.cdata

    if xmldata.metavariant.cdata == '':
        # Pure Variant
        metatypestring = xmldata.metatype.cdata
    else:
        # Metavariant
        metatypestring = xmldata.metavariant.cdata
    character['metatype'] = metatypestring

    # Personal
    character['personal']['realname'] = xmldata.name.cdata
    character['personal']['age'] = xmldata.age.cdata
    character['personal']['sex'] = xmldata.sex.cdata
    character['personal']['height'] = xmldata.height.cdata
    character['personal']['weight'] = xmldata.weight.cdata
    character['personal']['eyes'] = xmldata.eyes.cdata
    character['personal']['hair'] = xmldata.hair.cdata
    character['personal']['skin'] = xmldata.skin.cdata

    # Attributes
    # Only the natural attribute is transferred, the rest is recalculated later
    for a in xmldata.attributes.attribute:
        attributename = a.name.cdata
        if attributename == 'AGI':
            attributename = 'GES'
        elif attributename == 'BOD':
            attributename = 'KON'

        if attributename in ['KON', 'GES', 'REA', 'STR', 'CHA',
                             'INT', 'LOG', 'WIL', 'EDG']:
            # Racial
            # Guessed from metatype min and max if they are not 1 / 6
            vrac = 0
            if int(a.metatypemin.cdata) > 1:
                vrac = int(a.metatypemin.cdata) - 1
            elif int(a.metatypemax.cdata) < 6:
                vrac = int(a.metatypemax.cdata) - 6

            # Natural
            # Not saved in XML, deduced from racial and natural value.)
            vnat = int(a.value.cdata) - vrac
            character['attributes'][attributename]['natural'] = vnat

    # Essence
    character['essence']['reference'] = (
        float(xmldata.essenceatspecialstart.cdata))

    # Recalculate Character and return
    return RecalculateCharacter(character)
