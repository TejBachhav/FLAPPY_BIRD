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
It uses the same assets and appearance logic (for birds and pipes) as the manual game.
"""

import pygame, random, sys
from pygame.locals import *
from .ga_bird import GABird, SCREEN_WIDTH, SCREEN_HEIGHT, SPEED, GRAVITY
from .genetic_algorithm import evolve

# Simulation constants
GAME_SPEED = 15
PIPE_WIDTH = 80
PIPE_HEIGHT = 500   # same as in the manual game
PIPE_GAP = 150
FPS = 30

# Load shared assets
BACKGROUND = pygame.image.load('assets/assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
wing = 'assets/assets/audio/wing.wav'
hit = 'assets/assets/audio/hit.wav'
pygame.mixer.init()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.inverted = inverted
        # Load the pipe image and scale it as in the manual game
        self.image = pygame.image.load('assets/assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.y = - (self.rect.height - ysize)
        else:
            self.rect.y = SCREEN_HEIGHT - ysize
            self.passed = False  # for score tracking (if needed)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= GAME_SPEED

def get_random_pipes(xpos):
    """Return a tuple of (normal_pipe, inverted_pipe) with a randomized gap."""
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted

def run_generation(population, screen, clock):
    """
    Run one generation of the GA simulation.
    Uses the same background as the manual game.
    Returns the surviving population.
    """
    # Start with a pair of pipes off the right of the screen
    pipes = []
    pipes_pair = get_random_pipes(SCREEN_WIDTH + 200)
    pipes.extend(pipes_pair)
    generation_running = True

    while generation_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Update pipes; add new pipe pair if the last pipe is within the screen
        for pipe in pipes:
            pipe.update()
        if pipes[-1].rect.x < SCREEN_WIDTH:
            new_pair = get_random_pipes(SCREEN_WIDTH + 200)
            pipes.extend(new_pair)

        # Process each bird: let it decide based on the nearest pipe and update its state
        for bird in population:
            if bird.rect.y < 0 or bird.rect.y > SCREEN_HEIGHT:
                bird.kill()  # Out-of-bounds → mark as dead
            else:
                for pipe in pipes:
                    if pipe.rect.x + PIPE_WIDTH > bird.rect.x:
                        bird.decide(pipe)
                        break
                bird.update()

        # Collision detection: if a bird collides with any pipe, it dies
        for bird in population:
            for pipe in pipes:
                if bird.rect.colliderect(pipe.rect):
                    pygame.mixer.music.load(hit)
                    pygame.mixer.music.play()
                    bird.kill()

        # Remove dead birds from the population list
        population = [bird for bird in population if bird.alive()]

        # Draw the background and all sprites using shared assets
        screen.blit(BACKGROUND, (0, 0))
        for pipe in pipes:
            screen.blit(pipe.image, pipe.rect)
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
