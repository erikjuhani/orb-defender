from pygame import *

texture_atlas = image.load('img/texture_atlas.png')
font_atlas = image.load('img/txtatlas.png')
sprite_size = 16
font_size = 8
ascii_font = []

''' Get's a surface/sprite from a parent surface/sprite_sheet '''
def get_sprite(pos):
    texture_atlas.set_clip(Rect(pos[0], pos[1], sprite_size, sprite_size))
    return texture_atlas.subsurface(texture_atlas.get_clip())

''' Get's a surface/sprite from a parent surface/sprite_sheet '''
def get_character(pos):
    font_atlas.set_clip(Rect(pos[0], pos[1], font_size, font_size))
    return font_atlas.subsurface(font_atlas.get_clip())

''' Creates the ascii list '''
for y in range(16):
    for x in range(16):
        ascii_font.append(get_character((x * font_size, y * font_size)))

''' Finds a corresponding sprite for the ascii character '''
def find_character(char):
    return ascii_font[ord(char)]

''' Converts a regular string to a image '''
def convert_string(string):
    width = len(string) * font_size
    surf = Surface((width, font_size))

    for c in range(len(string)):
        surf.blit(find_character(string[c]), (c * font_size, 0))

    return surf

''' Changes the menu states color between white and blue '''
def change_color(surface, state):
    pxarray = PixelArray(surface)
    size = len(pxarray)
    blue = (101, 216, 249)
    white = (255, 255, 255)

    if state:
        pxarray[:] = pxarray[:].replace(white, blue)
    else:
        pxarray[:] = pxarray[:].replace(blue, white)

    del pxarray

''' Static textures '''
textures = {
            'orb'       : get_sprite((0, 0)),
            'wall'      : get_sprite((1 * sprite_size, 0)),
            'tower1'    : get_sprite((2 * sprite_size, 0)),
            'tower2'    : get_sprite((3 * sprite_size, 0)),
            'torch'     : get_sprite((4 * sprite_size, 0)),
            'farm'      : get_sprite((5 * sprite_size, 0)),
            'coin'      : get_sprite((6 * sprite_size, 0)),
            'monster1'  : get_sprite((0, 1 * sprite_size)),
            'monster2'  : get_sprite((1 * sprite_size, 1 * sprite_size)),
            'monster3'  : get_sprite((2 * sprite_size, 1 * sprite_size)),
            'monster4'  : get_sprite((3 * sprite_size, 1 * sprite_size)),
            'bones'     : get_sprite((4 * sprite_size, 1 * sprite_size))
          }

''' Creates a new sprite for an object and keeps track of the static array '''
class Sprite:
    def __init__(self, img):
        self.img = Surface((sprite_size, sprite_size), 0, img)
        self.static_array = PixelArray(img)
        self.unmapped_rgb = []
        for y in range(len(self.static_array)):
            for x in range(len(self.static_array)):
                self.unmapped_rgb.append(self.img.unmap_rgb(self.static_array[x, y]))
