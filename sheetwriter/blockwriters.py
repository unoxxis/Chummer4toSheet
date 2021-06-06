# Block Writer Routines

import logging
from fpdf import FPDF

from .geom_util import move_point, draw_cross
from .geom_util import draw_field, draw_box, draw_field_label

import chumdata

# Globals
box_offset = (-0.15, -0.15)  # Offset of Box for Shadow Reasons


def WriteBlockHead(pdf, char, ox=0.0, oy=0.68, border=0):
    """
    Places the general block into the current PDF page.

    Parameters:
        pdf (FPDF): PDF writer object
        char (ChummerCharacter): Character to use
        ox, oy (float): Reference Position of the Block, top left corner.
        border (float): Border width
    """

    # Logging
    logger = logging.getLogger('sheetwriter.WriteBlockGeneral')
    logger.debug('Entering Function')

    # Box
    draw_box(pdf, 'h03_logo', ox, oy, 'Allgemeines', border=border)

    # Geometric Data
    rowspc = 0.62
    xmargin = 0.1
    ymargin = 0.1
    descw = 1.8

    # Left Colum
    draw_field_label(pdf, x=(ox + xmargin), y=(oy + ymargin + 0.0 * rowspc), w=descw, text='Alias', border=border)
    draw_field(pdf, 'b90', x=(ox + xmargin + descw), y=(oy + ymargin + 0.0 * rowspc), text=char['alias'], textemph='B', border=border)

    draw_field_label(pdf, x=(ox + xmargin), y=(oy + ymargin + 1.0 * rowspc), w=descw, text='realer Name', border=border)
    draw_field(pdf, 'b90', x=(ox + xmargin + descw), y=(oy + ymargin + 1.0 * rowspc), text=char['personal']['realname'], border=border)

    draw_field_label(pdf, x=(ox + xmargin), y=(oy + ymargin + 2.0 * rowspc), w=descw, text='Rolle', border=border)
    draw_field(pdf, 'b90', x=(ox + xmargin + descw), y=(oy + ymargin + 2.0 * rowspc), text=char['background']['role'], border=border)

    # Right Colum
    draw_field_label(pdf, x=(ox + 2.0 * xmargin + descw + 9.0), y=(oy + ymargin + 0.0 * rowspc), w=(19.0 - 3.0 * xmargin - descw - 12.0), text='Metatyp', border=border)
    # draw_field(pdf, 'b30', x=(ox + 2.0 * xmargin + descw + 9.0 + descw), y=(oy + ymargin + 0.0 * rowspc), text=chumdata.Metatypes[char['metatype']]['text'], border=border)

    draw_field_label(pdf, x=(ox + 2.0 * xmargin + descw + 9.0), y=(oy + ymargin + 1.0 * rowspc), w=descw, text='Alter', border=border)
    # draw_field(pdf, 'b30', x=(ox + 2.0 * xmargin + descw + 9.0 + descw), y=(oy + ymargin + 1.0 * rowspc), text=char['personal']['age'], border=border)

    # draw_field_label(pdf, x=(ox + 2.0 * xmargin + descw + 9.0), y=(oy + ymargin + 2.0 * rowspc), w=descw, text='Geschlecht', border=border)
    draw_field(pdf, 'b30', x=(ox + 2.0 * xmargin + 2.0 * descw + 9.0), y=(oy + ymargin + 2.0 * rowspc), text=char['personal']['sex'], border=border)

    return



    # Geometric Block Data
    margin = 0.05
    baselineadjust = 0.05
    leftcoloffset = (2.14 + margin, 0.14 + baselineadjust)
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

    currpoint = move_point(origin, *leftcoloffset)
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


def WriteBlockAttributes(pdf, char, origin=(0.0, 0.0), border=0):
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

    data = char.GetBlock('attributes')

    # Geometric Block Data
    margin = 0.05
    baselineadjust = 0.05
    leftcoloffset = (2.46 + margin, 0.27 + baselineadjust)
    columnoffset1 = 6.32
    columnoffset2 = 7.235
    rowoffset = 0.57
    valcellwidth = 0.65 - 2 * margin
    valcelloffset = 0.743
    crosscellsize = 0.32
    cellheight = 0.49

    pdf.set_font('Agency FB', '', 10)  # Back to Normal

    if border > 0:
        # Draw Origin
        currpoint = move_point(origin, -0.05, -0.05)
        pdf.ellipse(*currpoint, 0.1, 0.1, style='F')

    # Physical Attribute Block
    currpoint = move_point(origin, *leftcoloffset)
    pdf.set_xy(*currpoint)
    for a in ['KON', 'GES', 'REA', 'STR']:
        for i in range(5):
            localpoint = move_point(currpoint, valcelloffset * i, 0.0)
            pdf.set_xy(*localpoint)
            pdf.cell(txt=data[a][i], w=valcellwidth, h=cellheight, align='C', border=border)
        currpoint = move_point(currpoint, 0.0, rowoffset)

    # Mental Attribute Block
    currpoint = move_point(currpoint, columnoffset1, -4.0 * rowoffset)
    pdf.set_xy(*currpoint)
    for a in ['CHA', 'INT', 'LOG', 'WIL']:
        for i in range(5):
            localpoint = move_point(currpoint, valcelloffset * i, 0.0)
            pdf.set_xy(*localpoint)
            pdf.cell(txt=data[a][i], w=valcellwidth, h=cellheight, align='C', border=border)
        currpoint = move_point(currpoint, 0.0, rowoffset)

    # Special Attribute Block
    currpoint = move_point(currpoint, columnoffset2, -4.0 * rowoffset)
    pdf.set_xy(*currpoint)
    for a in ['MAGRES', 'EDG']:
        for i in range(4):
            localpoint = move_point(currpoint, (valcelloffset - 0.0075) * i, 0.0)
            pdf.set_xy(*localpoint)
            pdf.cell(txt=data[a][i], w=valcellwidth, h=cellheight, align='C', border=border)
        currpoint = move_point(currpoint, 0.0, rowoffset)

    #Edgepool
    for i in range(8):
        localpoint = move_point(currpoint, i * 0.56 - 1.51, 0.5 * margin)
        if i >= int(data['EDG'][2]):
            draw_cross(pdf, *localpoint, crosscellsize)
    if border > 0:
        pdf.set_line_width(0.02)
        pdf.set_draw_color(255, 0, 0)

    currpoint = move_point(currpoint, -0.29, rowoffset)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['ESS'][0], w=valcellwidth, h=cellheight, align='C', border=border)

    currpoint = move_point(currpoint, 1.195, 0.0)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['ESS'][1], w=valcellwidth, h=cellheight, align='C', border=border)

    currpoint = move_point(currpoint, 1.305, 0.0)
    pdf.set_xy(*currpoint)
    pdf.cell(txt=data['ESS'][2], w=valcellwidth, h=cellheight, align='C', border=border)
