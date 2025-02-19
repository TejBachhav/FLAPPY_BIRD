import pygame
from pygame.locals import *
from .neural_network import NeuralNetwork  # Ensure you have this module

# Shared game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 15
GRAVITY = 1.5

class GABird(pygame.sprite.Sprite):
    def __init__(self, network=None):
        pygame.sprite.Sprite.__init__(self)
        # Load the same bluebird images as in the manual game
        self.images = [
            pygame.image.load('assets/assets/sprites/bluebird-upflap.png').convert_alpha(),
            pygame.image.load('assets/assets/sprites/bluebird-midflap.png').convert_alpha(),
            pygame.image.load('assets/assets/sprites/bluebird-downflap.png').convert_alpha()
        ]
        self.speed = SPEED
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH / 6
        self.rect.y = SCREEN_HEIGHT // 2
        # If no network provided, initialize a default one.
        self.network = NeuralNetwork() if network is None else network
        self.fitness = 0

    def update(self):
        # Animate and apply physics
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        self.rect.y += self.speed
        self.fitness += 1

    def bump(self):
        self.speed = -SPEED

    def decide(self, pipe):
        """
        Use a neural network to decide whether to jump.
        Inputs (normalized):
        1. Bird's y-position / SCREEN_HEIGHT
        2. Bird's vertical speed / 20.0 (assumed maximum speed)
        3. Horizontal distance to the pipe: (pipe.rect.x - bird.rect.x) / SCREEN_WIDTH
        4. Pipe gap center: pipe.gap_center / SCREEN_HEIGHT
        If the network's output exceeds 0.5, the bird jumps.
        """
        inputs = [
            self.rect.y / SCREEN_HEIGHT,
            self.speed / 20.0,
            (pipe.rect.x - self.rect.x) / SCREEN_WIDTH,
            pipe.gap_center / SCREEN_HEIGHT
        ]
        output = self.network.forward(inputs)
        if output[0] > 0.5:
            self.bump()

