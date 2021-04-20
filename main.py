import textwrap
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def avg(t):
    return sum(t) / len(t)

LINE_LENGTH = 20
# TODO: get random quote
quote = "the only thing that matters in this life"
formatted = "\n".join(textwrap.wrap(quote, LINE_LENGTH))

# make image
image_width, image_height = (1000, 1000)
fnt_size = 500
text_width, text_height = 5000, 5000
ratio = 0.85
bg_color = tuple(np.random.choice(range(256), size=3))
fg_color = 'white' if avg(bg_color) < 128 else 'black'

while text_width > ratio * image_width or text_height > ratio * image_height:

    img = Image.new('RGB', (image_width, image_height), color=bg_color)
    fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', fnt_size)
    d = ImageDraw.Draw(img)

    text_width, text_height = d.textsize(formatted, font=fnt)
    fnt_size -= 5

# center text
x_pos = int((image_width - text_width) / 2)
y_pos = int((image_height - text_height) / 2)
d.text((x_pos, y_pos), formatted, font=fnt, fill=fg_color)
img.save('img.png')