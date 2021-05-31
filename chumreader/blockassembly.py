# Functions which Assemble Character Sheet Blocks
# Author: Boris Wezisla

import logging
import math

# Local Imports
from .translations_DE import chum_translate


def AssembleBlockGeneral(self):
    """Assemble the data that goes into the general block of the character sheet and store it in the object."""

    # Logging
    logger = logging.getLogger('chumreader.AssembleBlockGeneral')
    logger.debug('Entering Function')

    block = dict()
    block['alias'] = self.xmldata.alias.cdata
    block['realname'] = self.xmldata.name.cdata
    block['role'] = self.xmldata.concept.cdata

    if self.xmldata.metatype.cdata.endswith('Shapeshifter'):
        # Shapeshifter (they abuse the metavariant)
        metatypestring = (
            chum_translate('metatype', 'Shapeshifter') + " ("
            + chum_translate('metatype', self.xmldata.metatype.cdata[:-13]) + ", "
            + chum_translate('metatype', self.xmldata.metavariant.cdata) + ")"
        )
    elif self.xmldata.metavariant.cdata == '':
        # Pure Variant
        metatypestring = chum_translate('metatype', self.xmldata.metatype.cdata)
    else:
        # Metavariant
        metatypestring = chum_translate('metatype', self.xmldata.metavariant.cdata)
    block['metatype'] = metatypestring

    block['age'] = self.xmldata.age.cdata
    block['sex'] = self.xmldata.sex.cdata

    logger.debug(f"Assembled block: {block}")
    self.blocks['general'] = block


def AssembleBlockAttributes(self):
    """Assemble the data that goes into the attributes block of the character sheet and store it in the object."""

    # Logging
    logger = logging.getLogger('chumreader.AssembleBlockAttributes')
    logger.debug('Entering Function')

    block = dict()

    for a in self.xmldata.attributes.attribute:
        attributename = a.name.cdata
        if attributename == 'AGI':
            attributename = 'GES'
        elif attributename == 'BOD':
            attributename = 'KON'

        if attributename in ['KON', 'GES', 'REA', 'STR', 'CHA', 'INT', 'LOG', 'WIL', 'EDG']:
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

            # Act
            vact = int(a.totalvalue.cdata)

            # Aug
            # Most improvements are not in the saved value, so calculated
            # as difference between act and nat+rac
            vaug = vact - (vnat + vrac)
            # vaug = int(a.augmodifier.cdata)

            # Max
            vmax = int(a.metatypeaugmax.cdata)

            if attributename == 'EDG':
                for q in self.xmldata.qualities.quality:
                    # This is not reflected anywhere, so we need to check for it manually...
                    if q.name.cdata == 'Lucky':
                        vmax += 1

                preblock = [f'{vnat:d}', f'{vrac:+d}', f'{vact:d}', f'{vmax:d}']
            else:
                preblock = [f'{vnat:d}', f'{vrac:+d}', f'{vaug:+d}', f'{vact:d}', f'{vmax:d}']

            block[attributename] = [i if i != "+0" else "-" for i in preblock]

        elif attributename == 'MAG' and self.xmldata.magenabled.cdata == 'True':
            logger.debug('Character Awakened (MAG)')

            # Natural
            vnat = int(a.value.cdata)

            # Initiation
            vinit = int(self.xmldata.initiategrade.cdata)

            # Act
            vact = int(a.totalvalue.cdata)

            # Max
            vmax = math.floor(float(self.xmldata.totaless.cdata.replace(',', '.'))) + vinit

            preblock = [f'{vnat:d}', f'{vinit:d}', f'{vact:d}', f'{vmax:d}']
            block['MAGRES'] = [i if i != "0" else "-" for i in preblock]

        elif attributename == 'RES' and self.xmldata.resenabled.cdata == 'True':
            logger.debug('Character Awakened (RES)')

            # Natural
            vnat = int(a.value.cdata)

            # Submersion
            vsub = int(self.xmldata.submersiongrade.cdata)

            # Act
            vact = int(a.totalvalue.cdata)

            # Max
            vmax = math.floor(float(self.xmldata.totaless.cdata.replace(',', '.'))) + vinit

            preblock = [f'{vnat:d}', f'{vsub:d}', f'{vact:d}', f'{vmax:d}']
            block['MAGRES'] = [i if i != "0" else "-" for i in preblock]

        elif attributename == 'ESS':
            # Act
            vact = float(self.xmldata.totaless.cdata.replace(',', '.'))

            # Essence Holes
            # Not stored, loop over cyberwares and biowares to find them
            ve = 0.00
            for cw in self.xmldata.cyberwares.cyberware:
                if cw.name.cdata == 'Essence Hole':
                    ve += int(cw.rating.cdata) * 0.01
            logger.debug(f'Calculated Essence Loss: {ve}')

            # VA
            # Implied, because faster
            va = 6.00 - ve - vact

            block['ESS'] = [f'{va:04.2f}', f'{ve:04.2f}', f'{vact:04.2f}']


    if 'MAGRES' not in block.keys():
        logger.debug('Character Not Awakened')
        block['MAGRES'] = ["-", "-", "-", "-"]

    logger.debug(f"Assembled block: {block}")
    self.blocks['attributes'] = block


def AssembleBlockTemplate(self):
    """Assemble the data that goes into the <template> block of the character sheet and store it in the object."""

    # Logging
    logger = logging.getLogger('chumreader.AssembleBlockGeneral')
    logger.debug('Entering Function')

    block = dict()

    # Here goes the Block filling

    logger.debug(f"Assembled block: {block}")
    self.blocks['general'] = block
