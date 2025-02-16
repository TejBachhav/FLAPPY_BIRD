import pygame
from pygame.locals import *
from .neural_network import NeuralNetwork  # Import your neural network class

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
        # If no network is provided, instantiate a default neural network
        self.network = NeuralNetwork() if network is None else network
        self.fitness = 0

    def update(self):
        # Animate the bird like in the manual game
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        self.rect.y += self.speed
        self.fitness += 1

    def bump(self):
        self.speed = -SPEED

    def decide(self, pipe):
        """
        Decision logic for the GA-controlled bird.
        Normally, you'd pass inputs (bird's y, speed, pipe distance, gap center) to the neural network.
        For simplicity, here we simulate a decision: if the pipe is near, then jump.
        """
        if pipe.rect.x < self.rect.x + 100:
            self.bump()
