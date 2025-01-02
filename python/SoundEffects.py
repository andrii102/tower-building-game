import pygame

class SoundEffects:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        pygame.mixer.music.load('assets/sounds/background.ogg')
        self.sounds['drop'] = pygame.mixer.Sound('assets/sounds/drop.ogg')
        self.sounds['drop-perfect'] = pygame.mixer.Sound('assets/sounds/drop-perfect.ogg')
        self.sounds['game-over'] = pygame.mixer.Sound('assets/sounds/game-over.ogg')
        self.sounds['rotate'] = pygame.mixer.Sound('assets/sounds/rotate.ogg')

    def play(self, sound_name):
        self.sounds[sound_name].play()

    def play_background(self):
        pygame.mixer.music.play(-1, 0.0)

    def stop_background(self):
        pygame.mixer.music.stop()
