# Block Writer Routines
# Author: Boris Wezisla

import logging
from fpdf import FPDF

from .geom_util import move_point, draw_cross


def WriteBlockGeneral(pdf, char, origin=(0.0, 0.0), border=0):
    """
    Places the general block into the current PDF page.

    Parameters:
        pdf (FPDF): PDF writer object
        char (ChummerCharacter): Character to use
        origin (tuple): Reference Position of the Block.
    """

    # Logging
    logger = logging.getLogger('sheetwriter.WriteBlockGeneral')
    logger.debug('Entering Function')

    data = char.GetBlock('general')

    # Geometric Block Data
    margin = 0.05
    baselineadjust = 0.05
    leftrowoffset = (2.14 + margin, 0.14 + baselineadjust)
    columnoffset = 11.6
    rowoffset = 0.575
    leftcellwidth = 9.525 - 2 * margin
    rightcellwidth = 2.575 - 2 * margin
    cellheight = 0.49

    # Alias
    pdf.set_font('Agency FB', 'B', 10)  # Separate Font

    if border > 0:
        # Draw Origin
        currpoint = move_point(origin, -0.05, -0.05)
        pdf.ellipse(*currpoint, 0.1, 0.1, style='F')

    currpoint = move_point(origin, *leftrowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['alias'], w=leftcellwidth, h=cellheight, align='C', border=border)

    # Real Name
    pdf.set_font('Agency FB', '', 10)  # Back to Normal

    currpoint = move_point(currpoint, 0.0, rowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['realname'], w=leftcellwidth, h=cellheight, align='L', border=border)

    # Role
    currpoint = move_point(currpoint, 0.0, rowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['role'], w=leftcellwidth, h=cellheight, align='L', border=border)

    # Metatype
    currpoint = move_point(currpoint, columnoffset, -2.0 * rowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['metatype'], w=rightcellwidth, h=cellheight, align='C', border=border)

    # Age
    currpoint = move_point(currpoint, 0.0, rowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['age'], w=rightcellwidth, h=cellheight, align='C', border=border)

    # Sex
    currpoint = move_point(currpoint, 0.0, rowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['sex'], w=rightcellwidth, h=cellheight, align='C', border=border)

