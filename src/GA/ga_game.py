import pygame, random, sys
from pygame.locals import *
from .ga_bird import GABird, SCREEN_WIDTH, SCREEN_HEIGHT, SPEED, GRAVITY
from .genetic_algorithm import evolve
import matplotlib.pyplot as plt

# Simulation constants
GAME_SPEED = 15
PIPE_WIDTH = 80
PIPE_HEIGHT = 500   # same as in the manual game
PIPE_GAP = 150
FPS = 30

# Load shared assets (using same asset paths as the manual game)
BACKGROUND = pygame.image.load('assets/assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
wing = 'assets/assets/audio/wing.wav'
hit = 'assets/assets/audio/hit.wav'
pygame.mixer.init()

# Global list to track the best fitness per generation
fitness_history = []

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.inverted = inverted
        # Load and scale the pipe image as in the manual game
        self.image = pygame.image.load('assets/assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.y = - (self.rect.height - ysize)
        else:
            self.rect.y = SCREEN_HEIGHT - ysize
            self.passed = False  # for score tracking if needed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= GAME_SPEED

def get_random_pipes(xpos):
    """
    Return a tuple of (normal_pipe, inverted_pipe) with a randomized gap.
    Also computes the gap center (vertical center of the gap) and assigns it
    to the normal pipe so that the decision function in GABird can use it.
    """
    size = random.randint(100, 300)
    normal_pipe = Pipe(False, xpos, size)
    inverted_pipe = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    normal_pipe.gap_center = size + PIPE_GAP / 2
    return normal_pipe, inverted_pipe

def plot_fitness():
    """Update the live plot of best fitness per generation."""
    plt.clf()
    plt.plot(fitness_history, marker='o', linestyle='-', color='b')
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.title("Flappy Bird GA - Fitness Over Generations")
    plt.grid(True)
    plt.pause(0.001)

def run_generation(population, screen, clock):
    """
    Run one generation of the GA simulation.
    Uses the same background as the manual game.
    Returns the surviving population.
    """
    # Start with 2 pairs, spaced roughly by SCREEN_WIDTH.
    initial_x = 800
    pipes = []
    for i in range(2):
        pair = get_random_pipes(initial_x + i * SCREEN_WIDTH)
        pipes.extend(pair)
    
    generation_running = True

    while generation_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Allow quitting with the Q key
            if event.type == KEYDOWN and event.key == K_q:
                pygame.quit()
                sys.exit()

        # Update pipes
        for pipe in pipes:
            pipe.update()

        # Remove off-screen pipes
        for pipe in list(pipes):
            if pipe.rect.x < -pipe.rect.width:
                pipes.remove(pipe)

        # Add new pipes if needed
        if len(pipes) < 4:
            new_x = pipes[-1].rect.x + SCREEN_WIDTH
            new_pair = get_random_pipes(new_x)
            pipes.extend(new_pair)

        # Process each bird: decide, update, and check bounds.
        for bird in population:
            if bird.rect.y < 0 or bird.rect.y > SCREEN_HEIGHT:
                bird.kill()  # Out-of-bounds → mark as dead.
            else:
                # Find the nearest pipe to the right
                for pipe in pipes:
                    if pipe.rect.x + PIPE_WIDTH > bird.rect.x:
                        bird.decide(pipe)  # The decision function uses pipe.gap_center.
                        break
                bird.update()

        # Collision detection using mask-based collision.
        birds_group = pygame.sprite.Group(population)
        pipes_group = pygame.sprite.Group(pipes)
        collisions = pygame.sprite.groupcollide(birds_group, pipes_group, False, False, pygame.sprite.collide_mask)
        if collisions:
            pygame.mixer.music.load(hit)
            pygame.mixer.music.play()
            for bird in collisions:
                bird.kill()

        # Remove dead birds from the population list.
        population = [bird for bird in population if bird.alive()]

        # Draw the background and all sprites.
        screen.blit(BACKGROUND, (0, 0))
        for pipe in pipes:
            screen.blit(pipe.image, pipe.rect)
        birds_group = pygame.sprite.Group(population)
        birds_group.draw(screen)
        pygame.display.update()

        # End generation if all birds are dead.
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

    # Enable interactive mode for live graph updates.
    plt.ion()
    plt.figure(figsize=(8, 4))

    while True:
        generation += 1
        print("Generation:", generation)
        run_generation(population, pygame.display.get_surface(), clock)
        best_fitness = max(bird.fitness for bird in population)
        print("Best fitness:", best_fitness)
        
        # Update fitness history and plot the learning curve.
        fitness_history.append(best_fitness)
        plot_fitness()
        
        # Evolve the population.
        population = evolve(population)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird GA")
    ga_main()





# """
# GA Simulation for Flappy Bird using a Genetic Algorithm.
# This module runs a generation loop where a population of AI-controlled birds
# (evolving via crossover and mutation) try to survive by avoiding pipes.
# It uses the same assets and appearance logic (for birds and pipes) as the manual game.
# """

# import pygame, random, sys
# from pygame.locals import *
# from .ga_bird import GABird, SCREEN_WIDTH, SCREEN_HEIGHT, SPEED, GRAVITY
# from .genetic_algorithm import evolve

# # Simulation constants
# GAME_SPEED = 15
# PIPE_WIDTH = 80
# PIPE_HEIGHT = 500   # same as in the manual game
# PIPE_GAP = 150
# FPS = 30

# # Load shared assets (using same asset paths as the manual game)
# BACKGROUND = pygame.image.load('assets/assets/sprites/background-day.png')
# BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
# wing = 'assets/assets/audio/wing.wav'
# hit = 'assets/assets/audio/hit.wav'
# pygame.mixer.init()

# class Pipe(pygame.sprite.Sprite):
#     def __init__(self, inverted, xpos, ysize):
#         pygame.sprite.Sprite.__init__(self)
#         self.inverted = inverted
#         # Load and scale the pipe image as in the manual game
#         self.image = pygame.image.load('assets/assets/sprites/pipe-green.png').convert_alpha()
#         self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
#         self.rect = self.image.get_rect()
#         self.rect.x = xpos
#         if inverted:
#             self.image = pygame.transform.flip(self.image, False, True)
#             self.rect.y = - (self.rect.height - ysize)
#         else:
#             self.rect.y = SCREEN_HEIGHT - ysize
#             self.passed = False  # for score tracking if needed
#         self.mask = pygame.mask.from_surface(self.image)

#     def update(self):
#         self.rect.x -= GAME_SPEED

# def get_random_pipes(xpos):
#     """
#     Return a tuple of (normal_pipe, inverted_pipe) with a randomized gap.
#     Also computes the gap center (vertical center of the gap) and assigns it
#     to the normal pipe so that the decision function in GABird can use it.
#     """
#     size = random.randint(100, 300)
#     # Create normal and inverted pipes using the same y–value for consistency.
#     normal_pipe = Pipe(False, xpos, size)
#     inverted_pipe = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
#     normal_pipe.gap_center = size + PIPE_GAP / 2
#     return normal_pipe, inverted_pipe

# def run_generation(population, screen, clock):
#     """
#     Run one generation of the GA simulation.
#     Uses the same background as the manual game.
#     Returns the surviving population.
#     """
#     # Initialize pipes similar to the manual game:
#     # Start with 2 pairs, spaced roughly by SCREEN_WIDTH.
#     initial_x = 800
#     pipes = []
#     for i in range(2):
#         pair = get_random_pipes(initial_x + i * SCREEN_WIDTH)
#         pipes.extend(pair)
    
#     generation_running = True

#     while generation_running:
#         clock.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()

#         # Update pipes
#         for pipe in pipes:
#             pipe.update()

#         # Remove off-screen pipes
#         for pipe in list(pipes):
#             if pipe.rect.x < -pipe.rect.width:
#                 pipes.remove(pipe)

#         # If there are fewer than 4 pipes, add a new pair.
#         if len(pipes) < 4:
#             new_x = pipes[-1].rect.x + SCREEN_WIDTH
#             new_pair = get_random_pipes(new_x)
#             pipes.extend(new_pair)

#         # Process each bird: let it decide based on the nearest pipe and update its state.
#         for bird in population:
#             if bird.rect.y < 0 or bird.rect.y > SCREEN_HEIGHT:
#                 bird.kill()  # Out-of-bounds → mark as dead.
#             else:
#                 # Find the nearest pipe that is still to the right of the bird.
#                 for pipe in pipes:
#                     if pipe.rect.x + PIPE_WIDTH > bird.rect.x:
#                         bird.decide(pipe)  # The decision function uses pipe.gap_center.
#                         break
#                 bird.update()

#         # Collision detection using mask-based collision.
#         birds_group = pygame.sprite.Group(population)
#         pipes_group = pygame.sprite.Group(pipes)
#         collisions = pygame.sprite.groupcollide(birds_group, pipes_group, False, False, pygame.sprite.collide_mask)
#         if collisions:
#             pygame.mixer.music.load(hit)
#             pygame.mixer.music.play()
#             for bird in collisions:
#                 bird.kill()

#         # Remove dead birds from the population list.
#         population = [bird for bird in population if bird.alive()]

#         # Draw the background and all sprites.
#         screen.blit(BACKGROUND, (0, 0))
#         for pipe in pipes:
#             screen.blit(pipe.image, pipe.rect)
#         birds_group = pygame.sprite.Group(population)
#         birds_group.draw(screen)
#         pygame.display.update()

#         if len(population) == 0:
#             generation_running = False

#     return population

# def ga_main():
#     """
#     Main function for running the GA training simulation.
#     Evolves the bird population over successive generations.
#     """
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
