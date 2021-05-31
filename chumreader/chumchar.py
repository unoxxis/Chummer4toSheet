# Chummer Character Object
# Author: Boris Wezisla

import logging
import untangle
import sys

# XML Reader
from .chumreader import ReadChumFile

# Block Generation Functions
from .blockassembly import AssembleBlockGeneral


# Globals
_CHUM_MIN_VERSION = 490     # Minimum Chummer Version


class ChummerCharacter:
    """
    A class that represents a Shadowrun 4 character stored in a chum file.

    Attributes
    ----------
    xmldata : untangle.Element
        XML character data of the chum file
    alias : str
        Street name of the character for identification
    blocks: dict
        Dictionary of the generated data blocks. Missing blocks will be
        generated on-the-fly if requested with GetBlock().

    Methods:
    --------
    GetBlock(block) :
        Get a dictionary containing information required to print a given block of the character sheet.
    """

    def __init__(self, character):
        """
        Construct a ChummerCharacter object from a chummer file or an existing untangle object.
        """

        self.clogger = logging.getLogger('chumreader.ChummerCharacter')
        self.clogger.info('Instantiating Class ChummerCharacter')

        self.clogger.debug(f'Type of character argument to constructor: {type(character)}')
        if isinstance(character, untangle.Element):
            self.xmldata = character
        elif isinstance(character, str):
            self.xmldata = ReadChumFile(character)
        else:
            raise TypeError(f"'character' argument should be of type untangle.Element or string. Given type: <{type(character)}>")

        try:
            self.clogger.debug(f'Chummer Version of XML data: {self.xmldata.appversion.cdata}')
            if int(self.xmldata.appversion.cdata) < _CHUM_MIN_VERSION:
                raise ValueError(f'Stored XML data is from a too old Chummer version. Please update at least to version {_CHUM_MIN_VERSION}!')
        except AttributeError:
            self.clogger.error('XML data seems not to be a chummer file!')
            raise

        # Init Alias for faster instantiation
        self.alias = self.xmldata.alias.cdata

        # Init Block Dictionary
        self.blocks = dict()

    def GetBlock(self, block):
        """
        Returns a dictionary of a given character sheet block for printing. Requests assembly of missing blocks.

        Parameters:
            block (str): Block name, currently supported:
                'general': General Character Information

        Returns:
            blockdata (dict): Dictionary of the block data.
        """

        logger = logging.getLogger('chumreader.ChummerCharacter.GetBlock')
        self.clogger.info("Requesting Block <{block}>")

        logger.debug(self.blocks.keys())
        if block not in self.blocks.keys():
            logger.debug('Block is not yet generated and needs to be assembled.')
            self.AssembleBlock(block)

        return self.blocks[block]

    def AssembleBlock(self, block):
        """
        Assemble the requested block into self.blocks.

        Parameters:
            block (str): Block name, see GetBlock for list of possible blocks.
        """

        logger = logging.getLogger('chumreader.ChummerCharacter.AssembleBlock')
        logger.debug(f"Requested assembly of block '{block}'")

        # Figure out the assembly function
        assemble_function_name = 'AssembleBlock' + block.capitalize()
        assemble_function = globals()[assemble_function_name]
        logger.debug(f'Assemble function: {assemble_function}')

        # Call the assembly function:
        assemble_function(self)
