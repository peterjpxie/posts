from PIL import ImageFont

# Get a list of available fonts
available_fonts = ImageFont.get_fonts()

# Print the list of available fonts
for font in available_fonts:
    print(font)