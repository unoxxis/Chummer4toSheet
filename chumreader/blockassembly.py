# Functions which Assemble Character Sheet Blocks
# Author: Boris Wezisla

import logging
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
