"""Project-wide settings for the Pygame starter."""

class ScreenSettings:
    """Class to hold all the settings related to the screen."""
    WIDTH = 800
    HEIGHT = 600
    RESOLUTION = (WIDTH,HEIGHT)
    TITLE = "Game of the Amazons"
    FPS = 60
    CRT_ALPHA_RANGE = (75, 90)
    CRT_SCANLINE_HEIGHT = 3

class ColorSettings:

    # Base color names
    WHITE = 'white'
    BLACK = 'black'
    YELLOW = 'yellow'
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    CYAN = 'cyan'
    PURPLE = 'purple'
    GOLD = 'gold'
    DODGER_BLUE = 'dodgerblue'
    TAN = 'tan'
    FIREBRICK = 'firebrick'
    LIME_GREEN = 'limegreen'
    ORCHID = 'orchid'
    MEDIUM_ORCHID = 'mediumorchid'
    PLUM = 'plum'
    DARK_GRAY = 'darkgray'
    DIM_GRAY = 'dimgray'
    SADDLE_BROWN = 'saddlebrown'
    SLATE_GRAY = 'slategray'

    SCREEN_BACKGROUND = BLACK
    GRID_OUTLINE = BLACK

    WORD_COLORS = []
    DEFAULT_TEXT_COLOR = WHITE

class GridSettings:
    pass

class UISettings:
    pass

class PlayerSettings:
    pass

class FontSettings:
    FONT = 'font/Pixeled.ttf'

class AudioSettings:
    MUTE = False
    MUTE_MUSIC = False  # Keep music disabled while retaining sound effects.
    MUSIC_VOLUME = 0.5  # Background music volume in the range [0.0, 1.0].

class AssetPaths:
    GRAPHICS_DIR = 'graphics/'
    SOUND_DIR = 'sound/'
    MUSIC_DIR = 'music/'
    FONT_DIR = 'font/'

    MUSIC_TRACKS = []

class DebugSettings:
    MUTE = False