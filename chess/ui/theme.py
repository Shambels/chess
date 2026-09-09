SQUARE_SIZE = 100
FPS = 5

LIGHT_SQUARE = (232, 210, 150)
DARK_SQUARE = (156, 99, 56)

# Added onto a dark square, this yields the light square colour.
HIGHLIGHT_COLOR = tuple(l - d for l, d in zip(LIGHT_SQUARE, DARK_SQUARE))
