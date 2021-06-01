# Main Character Sheet Writer Routine
# Author: Boris Wezisla

import logging
from fpdf import FPDF

# Blockwriters
from .blockwriters import *


sheets_highres = {
    'Allgemeines': 'sheets/Allgemeines.png'
}

sheets_lowres = {
    'Allgemeines': 'sheets/Allgemeines_LowRes.png'
}


def WriteCharacterSheet(char, filename, lowres=False, borders=False):
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

    # Determine Image Path
    if lowres:
        logger.debug('Using low resolution backgrounds.')
        sheet_backgrounds = sheets_lowres
    else:
        sheet_backgrounds = sheets_highres

    # Determine Border Parameter for blockwriters
    if borders:
        border = 1
    else:
        border = 0

    currpage = 0

    # Initialize PDF Writer
    pdf = FPDF(orientation='P', unit='cm', format='A4')

    # Load Fonts
    pdf.add_font('Agency FB', '', fname='sheets/res/AGENCYR.TTF', uni=True)
    pdf.add_font('Agency FB', 'B', fname='sheets/res/AGENCYB.TTF', uni=True)

    if borders:
        # Set bordercolor to red
        pdf.set_draw_color(255, 0, 0)
        pdf.set_fill_color(255, 0, 0)

    # PAGE ONE
    pdf.add_page()
    currpage += 1
    logger.info(f'New Page {currpage}:')

    # Background
    logger.info(f"Embedding Background '{sheet_backgrounds['Allgemeines']}'...")
    pdf.image(sheet_backgrounds['Allgemeines'], x=0, y=0, w=21.0)

    logger.info('Writing General Block...')
    WriteBlockGeneral(pdf, char, origin=(0.96, 1.30), border=border)

    logger.info('Writing Attributes Block...')
    WriteBlockAttributes(pdf, char, origin=(0.96, 4.15), border=border)

    pdf.output(name=filename, dest='F')


