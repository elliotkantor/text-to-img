import textwrap
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
from pathlib import Path
import glob
import sys


def get_fonts():
    fonts = []
    expressions = ["SF-Pro-Display*"]
    for e in expressions:
        fonts.extend(glob.glob("/library/Fonts/" + e))
    return fonts


LINE_LENGTH = 20
IMAGE_WIDTH, IMAGE_HEIGHT = (1000, 1000)
FONTS = get_fonts()


def make_image(text, filepath=None, custom_color=None, custom_font=None):

    """
    Creates a plain image based on text.
    filepath: str -> where the image is saved.
    if empty, won't save
    custom_color: tuple len 3 -> color in RGB
    if empty, random color
    custom_font: str -> path to font
    if empty, random font
    """

    def avg(t):
        return sum(t) / len(t)

    fnt_size = 500  # starting font size
    FNT_RATIO = 0.85
    text_width, text_height = tuple([x * 3 for x in [IMAGE_WIDTH, IMAGE_HEIGHT]])

    # get random colors
    bg_color = tuple(np.random.choice(range(256), size=3))
    if not custom_color:
        fg_color = "white" if avg(bg_color) < 128 else "black"
    else:
        fg_color = custom_color

    # get font family
    fnt_family = custom_font if custom_font else str(random.choice(FONTS))

    # scale text based on ratio
    while (
        text_width > FNT_RATIO * IMAGE_WIDTH or text_height > FNT_RATIO * IMAGE_HEIGHT
    ):

        img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=bg_color)
        fnt = ImageFont.truetype(fnt_family, fnt_size)
        text_canvas = ImageDraw.Draw(img)

        # calculate text size for scaling
        text_width, text_height = text_canvas.textsize(text, font=fnt)
        fnt_size -= 5

    # center text and write image
    X_POS = int((IMAGE_WIDTH - text_width) / 2)
    Y_POS = int((IMAGE_HEIGHT - text_height) / 2)
    text_canvas.text((X_POS, Y_POS), text, font=fnt, fill=fg_color)

    # save image
    saved = False
    if filepath:
        img.save(filepath)
        saved = True
    return img, saved


def demo():
    img, saved = make_image("This is some test text.")
    if not saved:
        img.save("img.png")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        demo()
    elif len(sys.argv) == 2:
        make_image(sys.argv[-1], filepath="img.png")