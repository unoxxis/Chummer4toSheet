# Geometric Utility Functions

geom_box_offset_x = -0.30    # Offset for box graphics relativ to box origin
geom_box_offset_y = -0.65    #
geom_box_sizeplus_x = 0.67   # Size Plus of the box graphics to accomodate shadow etc.
geom_box_sizeplus_y = 0.00
geom_box_textoffset_x = 0.00  # Offset of Box title text
geom_box_textoffset_y = -0.45

geom_fieldlabel_textoffset_x = 0.00  # Offset of field label text
geom_fieldlabel_textoffset_y = 0.02

geom_field_offset_x = -0.05    # Offset for field graphics relativ to field origin
geom_field_offset_y = -0.05    #
geom_field_sizeplus_x = 0.15   # Size Plus of the field graphics to accomodate shadow etc.
geom_field_sizeplus_y = 0.15
geom_field_textoffset_x = 0.00  # Text offset
geom_field_textoffset_y = geom_fieldlabel_textoffset_y

# Colors
geom_box_headercolor = (33, 74, 103)    # Box Header
geom_fieldlabel_color = (33, 74, 103)   # Field Label
geom_field_color = (0, 0, 0)        # Field Text


def LoadAssets(lowres=True):
    """
    Load Sheetwriter graphical assets

    Parameters:
        lowres (bool): whether to use the lowres assets for speed
    """
    global assets, assets_field_widths, assets_box_heights

    assets_box_heights = {
        'h03': 3.0,
        'h03_logo': 3.0,
        'h04': 4.0,
    }

    assets_field_widths = {
        'b05': 0.5,
        'b065': 0.65,
        'b30': 3.0,
        'b80': 8.0,
        'b90': 9.0,
    }

    assets_highres = dict()
    assets_lowres = dict()

    for k in assets_box_heights.keys():
        assets_highres[f"box_{k}"] = f"sheets/box_{k}.png"
        assets_lowres[f"box_{k}"] = f"sheets/box_{k}_LowRes.png"

    for k in assets_field_widths.keys():
        assets_highres[f"field_{k}"] = f"sheets/feld_{k}_light.png"
        assets_highres[f"field_{k}d"] = f"sheets/feld_{k}_dark.png"
        assets_lowres[f"field_{k}"] = f"sheets/feld_{k}_light.png"
        assets_lowres[f"field_{k}d"] = f"sheets/feld_{k}_dark.png"

    if lowres:
        assets = assets_lowres
    else:
        assets = assets_highres


def LoadFonts(pdf):
    """
    Load fonts.

    Parameters:
        pdf (FPDF): PDF writer
    """

    pdf.add_font('Fira Sans', '', fname='test/font_store/FiraSans-Regular.ttf', uni=True)
    pdf.add_font('Fira Sans Semi', '', fname='test/font_store/FiraSans-SemiBold.ttf', uni=True)
    pdf.add_font('Fira Sans', 'B', fname='test/font_store/FiraSans-Bold.ttf', uni=True)
    pdf.add_font('Fira Code', '', fname='test/font_store/FiraCode-Regular.ttf', uni=True)
    pdf.add_font('Fira Code', 'B', fname='test/font_store/FiraCode-SemiBold.ttf', uni=True)


def draw_box(pdf, boxheight, x=0.0, y=0.68, text='Box', dark=False, border=0):
    """
    Draw a field onto the frame.

    Parameters:
        pdf (FPDF): PDF writer object
        fieldsize (str): height identifier of the box
        x, y (float): top left corner of inner (blue) box
        text (str): headline text

    """
    global assets, assets_box_heights

    if boxheight not in assets_box_heights.keys():
        raise ValueError(f"Requested box height '{boxheight}' is not available")

    ass = assets[f"box_{boxheight}"]

    pdf.image(ass, x=(x + geom_box_offset_x), y=(y + geom_box_offset_y), h=(assets_box_heights[boxheight] + geom_box_sizeplus_y))

    # Caption Text
    pdf.set_font('Fira Code', 'B', 8)
    pdf.set_text_color(*geom_box_headercolor)
    pdf.set_xy(x + geom_box_textoffset_x, y + geom_box_textoffset_y)
    pdf.cell(txt=text, w=10.0, h=0.5, align='L', border=border)


def draw_field_label(pdf, x=0.0, y=0.0, w=3.0, text='Label', border=0):
    """
    Draw a label for a field at given positions.

    Parameters:
        pdf (FPDF): PDF writer object
        x, y (float): top left corner of inner (blue) box
        w (float): width of the field
        text (str): headline text
    """

    pdf.set_font('Fira Sans Semi', '', 8)
    pdf.set_text_color(*geom_fieldlabel_color)
    pdf.set_xy(x + geom_fieldlabel_textoffset_x, y + geom_fieldlabel_textoffset_y)
    pdf.cell(txt=text, w=w, h=0.5, align='L', border=border)


def draw_field(pdf, fieldsize, x, y, text=None, dark=False, border=0, textemph=''):
    """
    Draw a field onto the frame.

    Parameters:
        pdf (FPDF): PDF writer object
        fieldsize (str): width identifier of the field
        x, y (float): top left corner of box
        dark (bool): Whether to use the dark (calculated) field
        text (str) or None: if present, draw text onto field
        textemph (str): FPDS emphasis string for the text

    """
    global assets, assets_field_widths

    if fieldsize not in assets_field_widths.keys():
        raise ValueError(f"Requested field size '{fieldsize}' is not available")

    if dark:
        ass = assets[f"field_{fieldsize}d"]
    else:
        ass = assets[f"field_{fieldsize}"]

    pdf.image(ass, x=(x + geom_field_offset_x), y=(y + geom_field_offset_y), w=(assets_field_widths[fieldsize] + geom_field_sizeplus_x))

    if text is not None:
        pdf.set_font('Fira Sans', textemph, 8)
        pdf.set_text_color(*geom_field_color)
        pdf.set_xy(x + geom_field_textoffset_x, y + geom_field_textoffset_y)
        pdf.cell(txt=text, w=assets_field_widths[fieldsize], h=0.5, align='L', border=border)



# Old functions:

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


def draw_cross(pdf, x, y, size):
    """Draws a cross with top left corner (x,y).

    Parameters:
        pdf (FPDF): pdf writer object
        x, y (float): top left corner position
        size (float): side length of square
    """

    pdf.set_line_width(0.04)
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x1=x, y1=y, x2=x+size, y2=y+size)
    pdf.line(x1=x+size, y1=y, x2=x, y2=y+size)
