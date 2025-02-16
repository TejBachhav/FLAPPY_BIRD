# import pygame, random, sys
# from pygame.locals import *
# from .ga_bird import GABird, SCREEN_WIDTH, SCREEN_HEIGHT, SPEED, GRAVITY
# from .genetic_algorithm import evolve

# # Game parameters for GA simulation
# GAME_SPEED = 15
# PIPE_WIDTH = 80
# PIPE_GAP = 150
# FPS = 30

# # Pipe class for GA simulation
# class Pipe(pygame.sprite.Sprite):
#     def __init__(self, xpos):
#         super().__init__()
#         self.x = xpos
#         self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
#         self.gap_center = self.height + PIPE_GAP / 2
#         self.passed = False
#         # Create two rectangles representing the top and bottom pipes
#         self.top_rect = pygame.Rect(xpos, 0, PIPE_WIDTH, self.height)
#         self.bottom_rect = pygame.Rect(xpos, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (self.height + PIPE_GAP))
#         # For simple tracking
#         self.rect = pygame.Rect(xpos, 0, PIPE_WIDTH, SCREEN_HEIGHT)

#     def update(self):
#         self.top_rect.x -= GAME_SPEED
#         self.bottom_rect.x -= GAME_SPEED
#         self.rect.x -= GAME_SPEED

#     def draw(self, surface):
#         pygame.draw.rect(surface, (0, 255, 0), self.top_rect)
#         pygame.draw.rect(surface, (0, 255, 0), self.bottom_rect)

# def get_random_pipe(xpos):
#     return Pipe(xpos)

# def run_generation(population, screen, clock):
#     birds = pygame.sprite.Group(population)
#     pipes = [get_random_pipe(SCREEN_WIDTH + 200)]
#     generation_running = True

#     while generation_running:
#         clock.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()

#         # Update pipes and add new ones as needed
#         for pipe in pipes:
#             pipe.update()
#         if pipes[-1].rect.x < SCREEN_WIDTH:
#             pipes.append(get_random_pipe(SCREEN_WIDTH + 200))

#         # For each bird, have it decide based on the closest pipe
#         for bird in population:
#             if bird.rect.y < 0 or bird.rect.y > SCREEN_HEIGHT:
#                 bird.kill()  # Off-screen, mark as dead
#             else:
#                 for pipe in pipes:
#                     if pipe.rect.x + PIPE_WIDTH > bird.rect.x:
#                         bird.decide(pipe)
#                         break
#                 bird.update()

#         # Check for collisions between birds and pipes
#         for bird in population:
#             for pipe in pipes:
#                 if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
#                     bird.kill()

#         # Remove dead birds from the population
#         population = [bird for bird in population if bird.alive()]

#         # Draw everything
#         screen.fill((135, 206, 235))  # Sky blue background
#         for pipe in pipes:
#             pipe.draw(screen)
#         birds = pygame.sprite.Group(population)
#         birds.draw(screen)
#         pygame.display.update()

#         if len(population) == 0:
#             generation_running = False

#     return population

# def ga_main():
#     population_size = 50
#     population = [GABird() for _ in range(population_size)]
#     clock = pygame.time.Clock()
#     generation = 0

#     while True:
#         generation += 1
#         print("Generation:", generation)
#         run_generation(population, pygame.display.get_surface(), clock)
#         best_fitness = max(bird.fitness for bird in population)
#         print("Best fitness:", best_fitness)
#         population = evolve(population)

# if __name__ == "__main__":
#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     pygame.display.set_caption("Flappy Bird GA")
#     ga_main()
"""
GA Simulation for Flappy Bird using a Genetic Algorithm.
This module runs a generation loop where a population of AI-controlled birds
(evolving via crossover and mutation) try to survive by avoiding pipes.
"""

import pygame, random, sys
from pygame.locals import *
from .ga_bird import GABird, SCREEN_WIDTH, SCREEN_HEIGHT, SPEED, GRAVITY
from .genetic_algorithm import evolve

# Simulation constants
GAME_SPEED = 15
PIPE_WIDTH = 80
PIPE_GAP = 150
FPS = 30

class Pipe(pygame.sprite.Sprite):
    def __init__(self, xpos):
        super().__init__()
        self.x = xpos
        # Random height such that there's room for the gap
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.gap_center = self.height + PIPE_GAP / 2
        self.passed = False
        # Create rectangles for top and bottom pipes
        self.top_rect = pygame.Rect(xpos, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(xpos, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (self.height + PIPE_GAP))
        # A tracking rect for overall horizontal position
        self.rect = pygame.Rect(xpos, 0, PIPE_WIDTH, SCREEN_HEIGHT)

    def update(self):
        self.top_rect.x -= GAME_SPEED
        self.bottom_rect.x -= GAME_SPEED
        self.rect.x -= GAME_SPEED

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.top_rect)
        pygame.draw.rect(surface, (0, 255, 0), self.bottom_rect)

def get_random_pipe(xpos):
    """Return a new Pipe object with its gap randomized."""
    return Pipe(xpos)

def run_generation(population, screen, clock):
    """
    Run one generation of the GA simulation.
    Returns the surviving population.
    """
    # Create a sprite group for drawing birds
    birds = pygame.sprite.Group(population)
    # Start with one pipe off the right of the screen
    pipes = [get_random_pipe(SCREEN_WIDTH + 200)]
    generation_running = True

    while generation_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Update pipes and add a new pipe if needed
        for pipe in pipes:
            pipe.update()
        if pipes[-1].rect.x < SCREEN_WIDTH:
            pipes.append(get_random_pipe(SCREEN_WIDTH + 200))

        # Process each bird: let it decide based on the nearest pipe and update
        for bird in population:
            if bird.rect.y < 0 or bird.rect.y > SCREEN_HEIGHT:
                bird.kill()  # Out-of-bounds → mark as dead
            else:
                for pipe in pipes:
                    if pipe.rect.x + PIPE_WIDTH > bird.rect.x:
                        bird.decide(pipe)
                        break
                bird.update()

        # Collision detection: if a bird hits any pipe, it dies
        for bird in population:
            for pipe in pipes:
                if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                    bird.kill()

        # Remove dead birds from the population list
        population = [bird for bird in population if bird.alive()]

        # Draw background and sprites
        screen.fill((135, 206, 235))  # Sky blue background
        for pipe in pipes:
            pipe.draw(screen)
        birds = pygame.sprite.Group(population)
        birds.draw(screen)
        pygame.display.update()

        if len(population) == 0:
            generation_running = False

    return population

def ga_main():
    """
    Main function for running the GA training simulation.
    Evolves the bird population over successive generations.
    """
    population_size = 50
    population = [GABird() for _ in range(population_size)]
    clock = pygame.time.Clock()
    generation = 0

    while True:
        generation += 1
        print("Generation:", generation)
        run_generation(population, pygame.display.get_surface(), clock)
        best_fitness = max(bird.fitness for bird in population)
        print("Best fitness:", best_fitness)
        population = evolve(population)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird GA")
    ga_main()
