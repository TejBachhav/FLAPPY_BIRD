import pygame
from .neural_network import NeuralNetwork

# Constants for GA simulation (should match game settings)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 15
GRAVITY = 1.5

class GABird(pygame.sprite.Sprite):
    def __init__(self, network=None):
        super().__init__()
        # Create a simple circular bird representation
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (15, 15), 15)  # Yellow bird
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed = SPEED
        self.network = NeuralNetwork() if network is None else network
        self.fitness = 0  # Higher fitness means longer survival

    def update(self):
        self.speed += GRAVITY
        self.rect.y += self.speed
        self.fitness += 1  # Increase fitness for every frame survived

    def jump(self):
        self.speed = -SPEED

    def decide(self, pipe):
        # Inputs: normalized bird y, normalized speed, normalized horizontal distance to pipe, normalized pipe gap center
        gap_center = pipe.gap_center
        inputs = [
            self.rect.y / SCREEN_HEIGHT,
            self.speed / 20.0,  # Approximate normalization
            (pipe.rect.x - self.rect.x) / SCREEN_WIDTH,
            gap_center / SCREEN_HEIGHT
        ]
        output = self.network.forward(inputs)
        if output[0] > 0.5:
            self.jump()
