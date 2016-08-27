from pygame import *

texture_atlas = image.load('img/texture_atlas.png')
sprite_size = 16

def get_sprite(pos):
    texture_atlas.set_clip(Rect(pos[0], pos[1], sprite_size, sprite_size))
    return texture_atlas.subsurface(texture_atlas.get_clip())

textures = {
            'orb'       : get_sprite((0, 0)),
            'tower1'    : get_sprite((2 * sprite_size, 0)),
            'wall'      : get_sprite((1 * sprite_size, 0)),
            'torch'     : get_sprite((4 * sprite_size, 0)),
            'monster1'  : get_sprite((0, 1 * sprite_size)),
            'monster2'  : get_sprite((1 * sprite_size, 1 * sprite_size)),
            'monster3'  : get_sprite((2 * sprite_size, 1 * sprite_size)),
            'monster4'  : get_sprite((3 * sprite_size, 1 * sprite_size)),
            'bones'  : get_sprite((4 * sprite_size, 1 * sprite_size))
          }

class Sprite:
    def __init__(self, img):
        self.img = Surface((sprite_size, sprite_size), 0, img)
        self.static_array = PixelArray(img)

#class Sprite:
#    def __init__(self, img):
#        self.img = image.load(img)
#        self.static_array = PixelArray(image.load(img))

''' Static sprites '''

#orb = Sprite('img/orb.png')

''' pygame.surfarray.pixels2d(), manipulates the pixels, for rgb changes, no copying, faster '''

"""
pixel_array = PixelArray(wall_sprite)

size = len(pixel_array)

''' Mapper for integer values, changing from tuple color to integer values '''
'''
for y in range(size):
    for x in range(size):

'''

def change_brightness(pixel, amount, tint=None):

    #amount = amount + self.emit_light

    r, g, b, a = pixel # needs alpha because of the png with alpha layer

    max_r = r
    max_g = g
    max_b = b

    min_r = r * 0.01
    min_g = g * 0.01
    min_b = b * 0.01

    r *= amount
    g *= amount
    b *= amount

    if not tint == None:
        if 'r' in tint:
            r += r * amount
        if 'g' in tint:
            g += g * amount
        if 'b' in tint:
            b += b * amount

    if r < min_r:
        r = min_r
    if g < min_g:
        g = min_g
    if b < min_b:
        b = min_b

    if r > max_r:
        r = max_r
    if g > max_g:
        g = max_g
    if b > max_b:
        b = max_b

    return (int(r), int(g), int(b), a)

for y in range(size):
    for x in range(size):
        pixel_array[x, y] = change_brightness(wall_sprite.unmap_rgb(pixel_array[x, y]), 0.3)

del pixel_array

wall_sprite = transform.scale(wall_sprite, (wall_sprite.get_width()*4, wall_sprite.get_height()*4))
w, h = 400, 400
screen_size = w, h
screen = display.set_mode(screen_size)

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
    screen.blit(wall_sprite, (200-wall_sprite.get_width()/2, 200-wall_sprite.get_height()/2))
    display.update()


quit()
"""
