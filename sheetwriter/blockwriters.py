# Block Writer Routines

import logging

from .geom_util import draw_field, draw_box, draw_field_label, draw_annotation

from chumchar import ScanImprovements
import chumdata

# Globals
box_offset = (-0.15, -0.15)  # Offset of Box for Shadow Reasons


def WriteBlockHead(pdf, char, ox=0.96, oy=0.00, border=0):
    """
    Places the general block into the current PDF page.

    Parameters:
        pdf (FPDF): PDF writer object
        char (ChummerCharacter): Character to use
        ox, oy (float): Reference Position of the Block, top left corner.
        border (float): Border width
    """

    # Logging
    logger = logging.getLogger('sheetwriter.WriteBlockHead')
    logger.debug('Entering Function')

    # Box
    draw_box(pdf, 'h03_logo', ox, oy, 'Allgemeines', border=border)

    # Geometric Data
    rowspc = 0.62
    xmargin = 0.1
    ymargin = 0.1
    descw = 2.34

    # Left Colum
    draw_field_label(pdf, x=(ox + xmargin), y=(oy + ymargin + 0.0 * rowspc),
                     w=descw, text='Straßenname', border=border)
    draw_field(pdf, 'b80', x=(ox + xmargin + descw),
               y=(oy + ymargin + 0.0 * rowspc), text=" ".join(char['alias']),
               textemph='BBB', border=border)

    draw_field_label(pdf, x=(ox + xmargin), y=(oy + ymargin + 1.0 * rowspc),
                     w=descw, text='realer Name', border=border)
    draw_field(pdf, 'b80', x=(ox + xmargin + descw),
               y=(oy + ymargin + 1.0 * rowspc),
               text=char['personal']['realname'], border=border)

    draw_field_label(pdf, x=(ox + xmargin), y=(oy + ymargin + 2.0 * rowspc),
                     w=descw, text='Rolle', border=border)
    draw_field(pdf, 'b80', x=(ox + xmargin + descw),
               y=(oy + ymargin + 2.0 * rowspc),
               text=char['background']['role'], border=border)

    # Right Colum
    draw_field_label(pdf, x=(ox + 2.0 * xmargin + descw + 8.0),
                     y=(oy + ymargin + 0.0 * rowspc), w=descw, text='Metatyp',
                     border=border)
    draw_field(pdf, 'b30', x=(ox + 2.0 * xmargin + descw + 8.0 + descw),
               y=(oy + ymargin + 0.0 * rowspc),
               text=chumdata.Metatypes[char['metatype']]['text'],
               textalign='C', border=border)

    draw_field_label(pdf, x=(ox + 2.0 * xmargin + descw + 8.0),
                     y=(oy + ymargin + 1.0 * rowspc), w=descw, text='Alter',
                     border=border)
    draw_field(pdf, 'b30', x=(ox + 2.0 * xmargin + descw + 8.0 + descw),
               y=(oy + ymargin + 1.0 * rowspc), text=char['personal']['age'],
               textalign='C', border=border)

    draw_field_label(pdf, x=(ox + 2.0 * xmargin + descw + 8.0),
                     y=(oy + ymargin + 2.0 * rowspc), w=descw,
                     text='Geschlecht', border=border)
    draw_field(pdf, 'b30', x=(ox + 2.0 * xmargin + 2.0 * descw + 8.0),
               y=(oy + ymargin + 2.0 * rowspc), text=char['personal']['sex'],
               textalign='C', border=border)


def WriteBlockAttributes(pdf, char, ox=0.96, oy=0.00, border=0):
    """
    Places the attributes block into the current PDF page.

    Parameters:
        pdf (FPDF): PDF writer object
        char (ChummerCharacter): Character to use
        ox, oy (float): Reference Position of the Block, top left corner.
        border (float): Border width
    """

    # Logging
    logger = logging.getLogger('sheetwriter.WriteBlockAttributes')
    logger.debug('Entering Function')

    # Box
    draw_box(pdf, 'h04', ox, oy, 'Attribute', border=border)

    # Geometric Data
    rowspc = 0.57
    xmargin = 0.1
    ymargin = 0.1
    descw = 2.4
    lblskip = 0.07
    colsepextra = 0.45
    descskip = 0.3

    # An attribute block
    def Attributebox(x, y, descr, attribvals,
                     darklist=[False, False, False, True, False]):
        draw_field_label(pdf, x=x, y=y, w=descw, text=descr, border=border)
        for i in range(5):
            emph = ''
            if darklist[i]:
                emph = 'B'
            draw_field(pdf, 'b065', x=(x + descw + (0.65 + lblskip) * i),
                       y=y, text=attribvals[i], border=border, textalign='C',
                       textemph=emph, dark=darklist[i])

    def AwkAttributebox(x, y, descr, attribvals,
                        darklist=[True, False, False, False, True, False]):
        draw_field_label(pdf, x=x, y=y, w=(descw - 0.65 - lblskip),
                         text=descr, border=border)
        for i in range(6):
            if i == 2:
                continue
            emph = ''
            if darklist[i]:
                emph = 'B'
            draw_field(pdf, 'b065', x=(x + descw + (0.65 + lblskip) * (i - 1)),
                       y=y, text=attribvals[i], border=border, textalign='C',
                       textemph=emph, dark=darklist[i])

    # Put the 5 attribute values into a list
    def GetAttrVals(charattr, whichattr):
        vallist = [
            charattr[whichattr][key] for key
            in ['natural', 'racial', 'augment', 'actual', 'augment_max']
        ]
        for i in [0, 3, 4]:
            vallist[i] = f"{vallist[i]:d}"
        for i in [1, 2]:
            if vallist[i] == 0:
                vallist[i] = "–"
            else:
                vallist[i] = f"{vallist[i]:+d}"
        return vallist

    coloffs2 = descw + lblskip * 4.0 + 0.65 * 5 + colsepextra

    # Field Header
    fheaders = ['NAT', 'RAC', 'AUG', 'ACT', 'MAX']
    for i in range(5):
        draw_annotation(pdf, x=(ox + xmargin + descw + (0.65 + lblskip) * i),
                        y=(oy + ymargin), w=0.65, text=fheaders[i],
                        textalign='C', border=border)
        draw_annotation(
            pdf,
            x=(ox + xmargin + descw + (0.65 + lblskip) * i + coloffs2),
            y=(oy + ymargin), w=0.65, text=fheaders[i],
            textalign='C', border=border
        )

    tphys = ['Stärke', 'Geschicklichkeit', 'Reaktion', 'Konstitution']
    kphys = ['STR', 'GES', 'REA', 'KON']
    for i in range(4):
        Attributebox(
            ox + xmargin,
            oy + ymargin + descskip + rowspc * i,
            tphys[i],
            GetAttrVals(char['attributes'], kphys[i])
        )

    tment = ['Logik', 'Charisma', 'Intuition', 'Willenskraft']
    kment = ['LOG', 'CHA', 'INT', 'WIL']
    for i in range(4):
        Attributebox(
            ox + xmargin + coloffs2,
            oy + ymargin + descskip + rowspc * i,
            tment[i],
            GetAttrVals(char['attributes'], kment[i])
        )

    # Awakened Attribute
    test = True  # DEBUG
    if ScanImprovements(char['improvements'], itype='special',
                        ieffect='enable_magic'):
        tawk = "Magie"
        kawk = 'MAG'
        gawk = ' / GRAD = Initiationsgrad'
        awkgrade = char['initiation']['grade']
        mundane = False
    elif ScanImprovements(char['improvements'], itype='special',
                          ieffect='enable_resonance') or test:
        tawk = "Resonanz"
        kawk = 'RES'
        gawk = ' / GRAD = Wandlungsgrad'
        awkgrade = char['submersion']['grade']
        mundane = False
    else:
        # tawk = "Mundan"
        gawk = ''
        mundane = True

    if not mundane:
        if awkgrade == 0:
            gr = "–"
        else:
            gr = f"{awkgrade:d}"
        agr = [gr] + (GetAttrVals(char['attributes'], kawk))

        fheaders = ['GRAD'] + fheaders
        xtra = [0, 0, rowspc, 0, 0, 0]

        AwkAttributebox(
            ox + xmargin + coloffs2 * 2,
            oy + ymargin + descskip,
            tawk,
            agr
        )
    else:
        # draw_field_label(pdf, x=(ox + xmargin + coloffs2 * 2),
        #                  y=(oy + ymargin + descskip),
        #                  w=(descw - 0.65 - lblskip), text=tawk,
        #                  border=border)
        xtra = [rowspc for i in range(5)]

    for i in range(len(fheaders)):
        draw_annotation(
            pdf,
            x=(ox + xmargin + descw +
               (0.65 + lblskip) * (i + 5 - len(fheaders)) +
               coloffs2 * 2),
            y=(oy + ymargin + xtra[i]), w=0.65, text=fheaders[i],
            textalign='C', border=border
        )

    Attributebox(
        ox + xmargin + coloffs2 * 2,
        oy + ymargin + descskip + rowspc * 1,
        'Edge',
        GetAttrVals(char['attributes'], 'EDG')
    )

    # Footer
    foottext = (
        "NAT = natürlicher Wert / RAC = Rassenbonus / "
        "AUG = Vertärkungen / ACT = aktueller Wert / "
        f"MAX = verstärktes Maximum{gawk}"
    )
    draw_annotation(pdf, x=(ox + xmargin),
                    y=(oy + ymargin + descskip + rowspc * 4), w=16.0,
                    text=foottext, textalign='L', border=border)
