# Geometric Utility Functions
# Author: Boris Wezisla


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
