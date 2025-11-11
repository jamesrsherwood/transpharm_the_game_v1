import pygame
from pygame.math import Vector2 as vector
from sys import exit

# Get user's screen dimensions and use 80% of it (or set manual values)
def get_adaptive_window_size():
    pygame.init()  # Need to init pygame to get display info
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    # Use 80% of screen size, or fall back to 1200x720
    width = int(screen_width * 1) if screen_width > 0 else 1200
    height = int(screen_height * 1) if screen_height > 0 else 720

    # Maintain 5:3 aspect ratio (same as 1200:720)
    aspect_ratio = 5 / 3
    if width / height > aspect_ratio:
        width = int(height * aspect_ratio)
    else:
        height = int(width / aspect_ratio)

    return width, height

WINDOW_WIDTH, WINDOW_HEIGHT = get_adaptive_window_size()
SCREEN_PADDING = 20  # Padding from screen edges for text boxes

def wrap_text(text, font, max_width):
    """
    Wraps text to fit within max_width, breaking at spaces.
    Returns a list of lines.
    """
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        # Test if adding this word exceeds max width
        test_line = ' '.join(current_line + [word])
        test_surf = font.render(test_line, False, (0, 0, 0))

        if test_surf.get_width() <= max_width:
            current_line.append(word)
        else:
            # Current line is full, start a new line
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # Single word is too long, add it anyway
                lines.append(word)

    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))

    return lines

TILE_SIZE = 12 #standard tile size is 12
WATER_TILE_SIZE = 48
ANIMATION_SPEED = 8
INDEX_ANIMATION_SPEED = 4
BATTLE_OUTLINE_WIDTH = 4

COLORS = {
	'white': '#f4fefa', 
	'pure white': '#ffffff',
	'dark': '#2b292c',
	'light': '#c8c8c8',
	'gray': '#3a373b',
	'gold': '#ffd700',
	'light-gray': '#4b484d',
	'fire':'#f8a060',
	'water':'#50b0d8',
	'plant': '#64a990', 
	'black': '#000000', 
	'red': '#f03131',
	'blue': '#66d7ee',
    'normal': '#ffffff', #white
    'dark white': '#f0f0f0'
}

WORLD_LAYERS = {
	'water': 0, #keep water under all other tiles
	'bg': 1, # redundant
	'shadow': 2,
	'main': 3, # all other tiles on this layer
	'top': 4, # in case I want player to pass under something
    'text': 5 # added for speech bubbles
}

BATTLE_POSITIONS = { #for battle sprites
	'left': {'top': (360, 260), 'center': (190, 400), 'bottom': (410, 520)},
	'right': {'top': (780, 260), 'center': (900, 390), 'bottom': (800, 490)}
}

BATTLE_LAYERS =  { #for ordering images and text boxes
	'outline': 0,
	'name': 1,
	'monster': 2,
	'effects': 3,
	'overlay': 4
}

BATTLE_CHOICES = {
	'full': {
		'fight':  {'pos' : vector(30, -60), 'icon': 'sword'},
		'defend': {'pos' : vector(40, -20), 'icon': 'shield'},
		'switch': {'pos' : vector(40, 20), 'icon': 'arrows'},
		'catch':  {'pos' : vector(30, 60), 'icon': 'hand'}},
	
	'limited': {
		'fight':  {'pos' : vector(30, -40), 'icon': 'sword'},
		'defend': {'pos' : vector(40, 0), 'icon': 'shield'},
		'switch': {'pos' : vector(30, 40), 'icon': 'arrows'}}
}