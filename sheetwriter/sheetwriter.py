# Main Character Sheet Writer Routine
# Author: Boris Wezisla

import logging
from fpdf import FPDF

# Blockwriters
from .blockwriters import WriteBlockGeneral


sheets_highres = {
    'Allgemeines': 'sheets/Allgemeines.png'
}

sheets_lowres = {
    'Allgemeines': 'sheets/Allgemeines_LowRes.png'
}


def WriteCharacterSheet(char, filename, lowres=False):
    """
    Writes the character sheet of a character to a PDF file.

    Parameters:
        char (ChummerCharacter): Character to use
        filename (str): file path
        lowres (bool): Whether to use thumbnail backgrounds for debugging.
    """

    # Logging
    logger = logging.getLogger('sheetwriter.WriteCharacterSheet')
    logger.debug('Entering Function')

    if lowres:
        logger.debug('Using low resolution backgrounds.')
        sheet_backgrounds = sheets_lowres
    else:
        sheet_backgrounds = sheets_highres

    currpage = 0

    # Initialize PDF Writer
    pdf = FPDF(orientation='P', unit='cm', format='A4')

    # Load Fonts
    # pdf.add_font('Shadowrun', '', fname='sheets/res/SHADRG.TTF', uni=True)
    # pdf.add_font('Shadowrun', 'B', fname='sheets/res/SHADB.TTF', uni=True)
    pdf.add_font('Agency FB', '', fname='sheets/res/AGENCYR.TTF', uni=True)
    pdf.add_font('Agency FB', 'B', fname='sheets/res/AGENCYB.TTF', uni=True)


    # PAGE ONE
    pdf.add_page()
    currpage += 1
    logger.info(f'New Page {currpage}:')

    # Background
    logger.info('Embedding Background "Allgemeines"...')
    pdf.image(sheet_backgrounds['Allgemeines'], x=0, y=0, w=21.0)

    logger.info('Writing General Block...')
    WriteBlockGeneral(pdf, char, origin=(0.96, 1.29))

    pdf.output(name=filename, dest='F')


