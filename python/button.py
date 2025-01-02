from render import dynamic_resize

class Button:
    def __init__(self, image, x, y, width=None, height=None):
        self.image = dynamic_resize(image, new_width=width, new_height=height)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    

