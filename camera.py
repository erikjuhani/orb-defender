import math

''' Creates the map offsets and rendered boundaries. '''

class Camera:
    def __init__(self, screen_rect, size, follx, folly):
        self.screen_rect = screen_rect
        self.size = size
        self.x = int(screen_rect.centerx/size) - int(follx)
        self.y = int(screen_rect.centery/size) - int(folly)

    def update(self, follx, folly, level):

        if follx >= int((self.screen_rect.width/self.size)/2) and follx <= level.map_size - math.ceil((self.screen_rect.width/self.size)/2): # - 10, screen real estate takes 20 tiles
            self.x = int(self.screen_rect.centerx/self.size) - int(follx)
        if folly >= int((self.screen_rect.height/self.size)/2) - 1 and folly <= level.map_size - math.ceil((self.screen_rect.height/self.size)/2): # - 8, screen real estate takes 15 tiles
            self.y = int(self.screen_rect.centery/self.size) - int(folly)
