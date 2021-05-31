# Block Writer Routines
# Author: Boris Wezisla

import logging
from fpdf import FPDF


def move_point(point, dx, dy):
    """Moves a point tuple relatively.

    Parameters:
        point (2-tuple of float): Origin
        dx (float): Relative Movement of x
        dy (float): Relative Movement of y

    Returns:
        point (2-tuple of floar): New Point
    """
    return tuple(p + q for p, q in zip(point, (dx, dy)))


def WriteBlockGeneral(pdf, char, origin=(0.0, 0.0)):
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
    leftcellwidth = 9.50 - 2 * margin
    rightcellwidth = 2.55 - 2 * margin
    cellheight = 0.49

    # Alias
    pdf.set_font('Agency FB', 'B', 10)

    currpoint = move_point(origin, *leftrowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['alias'], w=leftcellwidth, h=cellheight, align='C')

    # Real Name
    pdf.set_font('Agency FB', '', 10)

    currpoint = move_point(currpoint, 0.0, rowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['realname'], w=leftcellwidth, h=cellheight, align='L')

    # Role
    currpoint = move_point(currpoint, 0.0, rowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['role'], w=leftcellwidth, h=cellheight, align='L')

    # Metatype
    currpoint = move_point(currpoint, columnoffset, -2.0 * rowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['metatype'], w=rightcellwidth, h=cellheight, align='C')

    # Age
    currpoint = move_point(currpoint, 0.0, rowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['age'], w=rightcellwidth, h=cellheight, align='C')

    # Sex
    currpoint = move_point(currpoint, 0.0, rowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['sex'], w=rightcellwidth, h=cellheight, align='C')

