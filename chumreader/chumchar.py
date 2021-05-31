# Chummer Character Object
# Author: Boris Wezisla

import logging
import untangle
import sys

from .chumreader import ReadChumFile

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
            raise ValueError('stored XML data has wrong format!')

        # Init Alias for faster instantiation
        self.alias = self.xmldata.alias.cdata

        # Init Block Dictionary
        self.blocks = dict()

    def GetBlock(block):
        """
        Returns a dictionary of a given character sheet block for printing. Generates missing blocks on-the-fly.

        Parameters:
            block (str): Block name, currently supported:
                'general': General Character Information

        Returns:
            blockdata (dict): Dictionary of the block data.
        """
        pass
