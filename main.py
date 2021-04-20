import textwrap
from PIL import Image, ImageDraw, ImageFont
import numpy as np

LINE_LENGTH = 20
IMAGE_WIDTH, IMAGE_HEIGHT = (1000, 1000)


def get_quote():
    # TODO: get random quote
    quote = "This is a quote in a picture"
    formatted = "\n".join(textwrap.wrap(quote, LINE_LENGTH))
    return formatted


def make_image(text, filepath=None, custom_color=None):

    """
    Creates a plain image based on text.
    filepath: str -> where the image is saved.
    if empty, won't save
    custom_color: tuple len 3 -> color in RGB
    if empty, random color
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

    # scale text based on ratio
    while (
        text_width > FNT_RATIO * IMAGE_WIDTH or text_height > FNT_RATIO * IMAGE_HEIGHT
    ):

        img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=bg_color)
        fnt = ImageFont.truetype("/Library/Fonts/Arial.ttf", fnt_size)
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


def main():
    text = get_quote()
    img, saved = make_image(text)
    if not saved:
        img.save("img.png")


if __name__ == "__main__":
    main()