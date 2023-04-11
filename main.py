import epd2in13b_v3 as epd
from PIL import Image, ImageDraw, ImageFont
import re, math, os

# Change working dir
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import rocket_data  # Now import the custom module

# Initialize display (Important: Enable SPI via raspi-config!)
display = epd.EPD()
display.init()


# Some functions used later
def truncate(string):
    return re.sub(r"\([^)]*\)", "", string)


def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


launches = rocket_data.Launches()  # Get Launches

launches.get_data()  # Request data from API
data = launches.parse_data(0)  # Get next launching rocket data
next_rocket_name = launches.parse_data(1)[
    "rocket_name"
]  # ... and the name of the rocket after that


# Loading fonts
font_12 = ImageFont.truetype("font.ttf", size=12)
font_20 = ImageFont.truetype("font.ttf", size=20)

color_image = Image.new(
    mode="1", size=(212, 104), color=255
)  # Image for drawing with color
color = ImageDraw.Draw(color_image)

black_image = Image.new(
    mode="1", size=(212, 104), color=255
)  # And the one where we draw the black image
black = ImageDraw.Draw(black_image)

color.text((0, 0), data["rocket_name"], 0, font_20)  # Name of rocket
black.text((0, 20), truncate(data["mission_name"]), 0, font_12)  # Mission name
black.text((0, 35), data["agency"], 0, font_12)  # Agency name
color.text(
    (0, 48), "T-" + seconds_to_hms(data["countdown"]), 0, font_20
)  # Create countdown (T-H:M:S)
black.text(
    (0, 69), f"Next: {next_rocket_name}", 0, font_12
)  # And here the next rocket name

# Add launch status in top left corner
abbrev_width, abbrev_height = black.textsize(data["abbrev"], font_20)
abbrev_x = 212 - abbrev_width
abbrev_y = 0
color.text((abbrev_x, abbrev_y), data["abbrev"], 0, font_20)

# Percentage Rectangle
height = 20
black_width = 4
black_rectangle_top = 104 - (math.ceil(height / 2) - math.ceil(black_width / 2))
black_rectangle_left = 0
black_rectangle_bottom = 104 - (math.floor(height / 2) + math.floor(black_width / 2))
black_rectangle_right = 212
black.rectangle(
    (
        black_rectangle_left,
        black_rectangle_top,
        black_rectangle_right,
        black_rectangle_bottom,
    ),
    fill="black",
)  # The black, thin line

color_rectangle_top = 104 - height
color_rectangle_left = 0
color_rectangle_bottom = 104
color_rectangle_right = round(212 * data["launch_percent"])
color.rectangle(
    (
        color_rectangle_left,
        color_rectangle_top,
        color_rectangle_right,
        color_rectangle_bottom,
    ),
    fill="black",
)  # and the colored one

# Rotate images
color_image = color_image.rotate(angle=180)
black_image = black_image.rotate(angle=180)

# Display images
display.Clear()
display.display(
    display.getbuffer(image=black_image), display.getbuffer(image=color_image)
)
