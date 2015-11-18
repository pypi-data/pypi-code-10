from PIL import Image, ImageEnhance

def blankTile(width=256, height=256):
    return Image.new("RGBA", (width, height), (0, 0, 0, 0))


def redTile(width=256, height=256):
    return Image.new("RGBA", (width, height), (256, 0, 0, 256))


def blackTile(width=256, height=256):
    return Image.new("RGBA", (width, height), (0, 0, 0, 256))


def solidTile(width, height, r=0, g=0, b=0, a=256):
    return Image.new("RGBA", (width, height), (r, g, b, a))
