#!/usr/bin/env python3
"""Zeigt eine Geburtstags-Widmung auf dem E-Ink-Display an.

Vorher den SlowMovie-Service stoppen:
    sudo systemctl stop slowmovie
Dann:
    cd ~/SlowMovie && .venv/bin/python birthday_message.py
Danach laeuft der Film weiter mit:
    sudo systemctl start slowmovie
"""

from PIL import Image, ImageDraw, ImageFont
from omni_epd import displayfactory

# >>> HIER DEN TEXT ANPASSEN <<<
LINES = [
    "Alles Liebe zum Geburtstag!",
    "",
    "Dieser Rahmen spielt unseren Film",
    "in Zeitlupe - jeden Tag ein neues Bild,",
    "vier Monate lang.",
    "",
    "18.07.2026",
]

EPD_NAME = "waveshare_epd.epd7in5_V2"

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def load_font(size):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    epd = displayfactory.load_display_driver(EPD_NAME)
    width, height = epd.width, epd.height

    image = Image.new("1", (width, height), 255)  # weisser Hintergrund
    draw = ImageDraw.Draw(image)

    font = load_font(34)
    line_height = 48
    total_height = line_height * len(LINES)
    y = (height - total_height) // 2

    for line in LINES:
        if line:
            text_width = draw.textlength(line, font=font)
            draw.text(((width - text_width) // 2, y), line, font=font, fill=0)
        y += line_height

    # Zierrahmen
    draw.rectangle([10, 10, width - 11, height - 11], outline=0, width=3)
    draw.rectangle([18, 18, width - 19, height - 19], outline=0, width=1)

    epd.prepare()
    epd.display(image)
    epd.sleep()
    print("Botschaft angezeigt. Film wieder starten mit: sudo systemctl start slowmovie")


if __name__ == "__main__":
    main()
