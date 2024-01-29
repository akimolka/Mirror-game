import enum


white = (255, 255, 255)
blue = (0, 0, 128)


class Size(enum.Enum):  # % of available space
    small = 0.6
    medium = 0.8
    large = 1.0

    def __float__(self):
        return self.value


class Style:
    class Standard:
        textcolor = white
        background = blue
        font = "couriernew"
        bold = False
        italic = False
        size = Size.medium


