# # import pygame
# # import random

# # # Initialize pygame
# # pygame.init()

# # # Game Constants
# # WIDTH, HEIGHT = 400, 600
# # BIRD_X = 50
# # GRAVITY = 0.6
# # JUMP_STRENGTH = -7
# # PIPE_WIDTH = 70
# # PIPE_GAP = 180
# # PIPE_SPEED = 4
# # FPS = 30

# # # Colors
# # WHITE = (255, 255, 255)
# # GREEN = (0, 255, 0)
# # BLUE = (0, 0, 255)
# # RED = (255, 0, 0)

# # # Set up display
# # screen = pygame.display.set_mode((WIDTH, HEIGHT))
# # pygame.display.set_caption("Flappy Bird Enhanced")

# # # Bird class
# # class Bird:
# #     def __init__(self):
# #         self.y = HEIGHT // 2
# #         self.velocity = 0

# #     def jump(self):
# #         self.velocity = JUMP_STRENGTH

# #     def move(self):
# #         self.velocity += GRAVITY
# #         self.y += self.velocity
# #         if self.y < 0:
# #             self.y = 0
# #         if self.y > HEIGHT:
# #             self.y = HEIGHT

# # # Pipe class
# # class Pipe:
# #     def __init__(self, x):
# #         self.x = x
# #         self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
# #         self.passed = False

# #     def move(self):
# #         self.x -= PIPE_SPEED

# #     def draw(self):
# #         pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
# #         pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT))

# # # Main function
# # def main():
# #     clock = pygame.time.Clock()
# #     bird = Bird()
# #     pipes = [Pipe(WIDTH + i * 200) for i in range(3)]
# #     running = True
# #     score = 0
# #     game_over = False

# #     while running:
# #         screen.fill(WHITE)
# #         for event in pygame.event.get():
# #             if event.type == pygame.QUIT:
# #                 running = False
# #             if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:
# #                 bird.jump()
        
# #         if not game_over:
# #             # Move bird
# #             bird.move()
# #             pygame.draw.circle(screen, BLUE, (BIRD_X, int(bird.y)), 15)
            
# #             # Move and draw pipes
# #             for pipe in pipes:
# #                 pipe.move()
# #                 pipe.draw()
                
# #                 # Check collision
# #                 if BIRD_X + 15 > pipe.x and BIRD_X - 15 < pipe.x + PIPE_WIDTH:
# #                     if bird.y - 15 < pipe.height or bird.y + 15 > pipe.height + PIPE_GAP:
# #                         game_over = True
                
# #                 # Update score
# #                 if not pipe.passed and pipe.x + PIPE_WIDTH < BIRD_X:
# #                     pipe.passed = True
# #                     score += 1
            
# #             # Add new pipes
# #             if pipes[0].x < -PIPE_WIDTH:
# #                 pipes.pop(0)
# #                 pipes.append(Pipe(WIDTH))
# #         else:
# #             font = pygame.font.Font(None, 50)
# #             text = font.render("Game Over! Press R to Restart", True, RED)
# #             screen.blit(text, (WIDTH // 8, HEIGHT // 2))
# #             keys = pygame.key.get_pressed()
# #             if keys[pygame.K_r]:
# #                 main()
# #                 return
        
# #         # Display score
# #         font = pygame.font.Font(None, 36)
# #         text = font.render(f"Score: {score}", True, (0, 0, 0))
# #         screen.blit(text, (10, 10))
        
# #         pygame.display.flip()
# #         clock.tick(FPS)
    
# #     pygame.quit()

# # if __name__ == "__main__":
# #     main()

# import pygame, random, time
# from pygame.locals import *
 
# #VARIABLES
# SCREEN_WIDHT = 400
# SCREEN_HEIGHT = 600
# SPEED = 20
# GRAVITY = 2.5
# GAME_SPEED = 15
 
# GROUND_WIDHT = 2 * SCREEN_WIDHT
# GROUND_HEIGHT= 100
 
# PIPE_WIDHT = 80
# PIPE_HEIGHT = 500
 
# PIPE_GAP = 150
 
# wing = 'assets/assets/audio/wing.wav'
# hit = 'assets/assets/audio/hit.wav'
 
# pygame.mixer.init()
 
 
# class Bird(pygame.sprite.Sprite):
 
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
 
#         self.images =  [pygame.image.load('assets/assets/sprites/bluebird-upflap.png').convert_alpha(),
#                         pygame.image.load('assets/assets/sprites/bluebird-midflap.png').convert_alpha(),
#                         pygame.image.load('assets/assets/sprites/bluebird-downflap.png').convert_alpha()]
 
#         self.speed = SPEED
 
#         self.current_image = 0
#         self.image = pygame.image.load('assets/assets/sprites/bluebird-upflap.png').convert_alpha()
#         self.mask = pygame.mask.from_surface(self.image)
 
#         self.rect = self.image.get_rect()
#         self.rect[0] = SCREEN_WIDHT / 6
#         self.rect[1] = SCREEN_HEIGHT / 2
 
#     def update(self):
#         self.current_image = (self.current_image + 1) % 3
#         self.image = self.images[self.current_image]
#         self.speed += GRAVITY
 
#         #UPDATE HEIGHT
#         self.rect[1] += self.speed
 
#     def bump(self):
#         self.speed = -SPEED
 
#     def begin(self):
#         self.current_image = (self.current_image + 1) % 3
#         self.image = self.images[self.current_image]
 
 
 
# class Pipe(pygame.sprite.Sprite):
 
#     def __init__(self, inverted, xpos, ysize):
#         pygame.sprite.Sprite.__init__(self)
 
#         self. image = pygame.image.load('assets/assets/sprites/pipe-green.png').convert_alpha()
#         self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))
 
 
#         self.rect = self.image.get_rect()
#         self.rect[0] = xpos
 
#         if inverted:
#             self.image = pygame.transform.flip(self.image, False, True)
#             self.rect[1] = - (self.rect[3] - ysize)
#         else:
#             self.rect[1] = SCREEN_HEIGHT - ysize
 
 
#         self.mask = pygame.mask.from_surface(self.image)
 
 
#     def update(self):
#         self.rect[0] -= GAME_SPEED
 
        
 
# class Ground(pygame.sprite.Sprite):
#     def __init__(self, xpos):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load('assets/assets/sprites/base.png').convert_alpha()
#         self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))
 
#         self.mask = pygame.mask.from_surface(self.image)
 
#         self.rect = self.image.get_rect()
#         self.rect[0] = xpos
#         self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
#     def update(self):
#         self.rect[0] -= GAME_SPEED
 
# def is_off_screen(sprite):
#     return sprite.rect[0] < -(sprite.rect[2])
 
# def get_random_pipes(xpos):
#     size = random.randint(100, 300)
#     pipe = Pipe(False, xpos, size)
#     pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
#     return pipe, pipe_inverted
 
 
# pygame.init()
# screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
# pygame.display.set_caption('Flappy Bird')
 
# BACKGROUND = pygame.image.load('assets/assets/sprites/background-day.png')
# BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
# BEGIN_IMAGE = pygame.image.load('assets/assets/sprites/message.png').convert_alpha()
 
# bird_group = pygame.sprite.Group()
# bird = Bird()
# bird_group.add(bird)
 
# ground_group = pygame.sprite.Group()
 
# for i in range (2):
#     ground = Ground(GROUND_WIDHT * i)
#     ground_group.add(ground)
 
# pipe_group = pygame.sprite.Group()
# for i in range (2):
#     pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
#     pipe_group.add(pipes[0])
#     pipe_group.add(pipes[1])
 
 
# clock = pygame.time.Clock()
 
# begin = True
 
# while begin:
 
#     clock.tick(15)
 
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#         if event.type == KEYDOWN:
#             if event.key == K_SPACE or event.key == K_UP:
#                 bird.bump()
#                 pygame.mixer.music.load(wing)
#                 pygame.mixer.music.play()
#                 begin = False
 
#     screen.blit(BACKGROUND, (0, 0))
#     screen.blit(BEGIN_IMAGE, (120, 150))
 
#     if is_off_screen(ground_group.sprites()[0]):
#         ground_group.remove(ground_group.sprites()[0])
 
#         new_ground = Ground(GROUND_WIDHT - 20)
#         ground_group.add(new_ground)
 
#     bird.begin()
#     ground_group.update()
 
#     bird_group.draw(screen)
#     ground_group.draw(screen)
 
#     pygame.display.update()
 
 
# while True:
 
#     clock.tick(15)
 
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#         if event.type == KEYDOWN:
#             if event.key == K_SPACE or event.key == K_UP:
#                 bird.bump()
#                 pygame.mixer.music.load(wing)
#                 pygame.mixer.music.play()
 
#     screen.blit(BACKGROUND, (0, 0))
 
#     if is_off_screen(ground_group.sprites()[0]):
#         ground_group.remove(ground_group.sprites()[0])
 
#         new_ground = Ground(GROUND_WIDHT - 20)
#         ground_group.add(new_ground)
 
#     if is_off_screen(pipe_group.sprites()[0]):
#         pipe_group.remove(pipe_group.sprites()[0])
#         pipe_group.remove(pipe_group.sprites()[0])
 
#         pipes = get_random_pipes(SCREEN_WIDHT * 2)
 
#         pipe_group.add(pipes[0])
#         pipe_group.add(pipes[1])
 
#     bird_group.update()
#     ground_group.update()
#     pipe_group.update()
 
#     bird_group.draw(screen)
#     pipe_group.draw(screen)
#     ground_group.draw(screen)
 
#     pygame.display.update()
 
#     if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
#             pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
#         pygame.mixer.music.load(hit)
#         pygame.mixer.music.play()
#         time.sleep(1)
#         break


import pygame, random, time, sys
from pygame.locals import *

# VARIABLES
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 15
GRAVITY = 1.5
GAME_SPEED = 15

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

wing = 'assets/assets/audio/wing.wav'
hit = 'assets/assets/audio/hit.wav'

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

BACKGROUND = pygame.image.load('assets/assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('assets/assets/sprites/message.png').convert_alpha()

# Classes
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
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
        self.rect[0] = SCREEN_WIDTH / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY

        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def animate(self):
        # Used in the start state to animate the wings without affecting physics
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.inverted = inverted
        self.image = pygame.image.load('assets/assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize
            self.passed = False  # flag to check for score increment
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -sprite.rect[2]

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted

def reset_game():
    global bird, bird_group, ground_group, pipe_group, score
    bird = Bird()
    bird_group = pygame.sprite.Group(bird)
    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground = Ground(GROUND_WIDTH * i)
        ground_group.add(ground)
    pipe_group = pygame.sprite.Group()
    for i in range(2):
        pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
    score = 0

# Initialize game objects
reset_game()
clock = pygame.time.Clock()
state = 'start'  # states: 'start', 'playing', 'game_over'
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 50)

# Main game loop
while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if state == 'start':
                if event.key in [K_SPACE, K_UP]:
                    state = 'playing'
                    bird.bump()
                    pygame.mixer.music.load(wing)
                    pygame.mixer.music.play()
            elif state == 'playing':
                if event.key in [K_SPACE, K_UP]:
                    bird.bump()
                    pygame.mixer.music.load(wing)
                    pygame.mixer.music.play()
            elif state == 'game_over':
                if event.key == K_r:
                    reset_game()
                    state = 'start'
    
    # Draw background
    screen.blit(BACKGROUND, (0, 0))
    
    if state == 'start':
        # Animate the bird on the start screen
        bird.animate()
        # Update ground movement
        ground_group.update()
        for ground in list(ground_group):
            if is_off_screen(ground):
                ground_group.remove(ground)
                new_ground = Ground(GROUND_WIDTH - 20)
                ground_group.add(new_ground)
        bird_group.draw(screen)
        ground_group.draw(screen)
        # Draw the begin message (centered)
        screen.blit(BEGIN_IMAGE, (SCREEN_WIDTH//2 - BEGIN_IMAGE.get_width()//2, 
                                  SCREEN_HEIGHT//2 - BEGIN_IMAGE.get_height()//2))
        # Display score (0 at this point)
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10, 10))
    
    elif state == 'playing':
        # Update sprites
        bird_group.update()
        ground_group.update()
        pipe_group.update()
        
        # Loop the ground sprites
        for ground in list(ground_group):
            if is_off_screen(ground):
                ground_group.remove(ground)
                new_ground = Ground(GROUND_WIDTH - 20)
                ground_group.add(new_ground)
        
        # Remove off-screen pipes and add new ones as needed
        for pipe in list(pipe_group):
            if is_off_screen(pipe):
                pipe_group.remove(pipe)
        if len(pipe_group) < 4:
            new_pipes = get_random_pipes(SCREEN_WIDTH * 2)
            pipe_group.add(new_pipes[0])
            pipe_group.add(new_pipes[1])
        
        # Update score using the non-inverted pipe (only once per pair)
        for pipe in pipe_group:
            if not pipe.inverted and not pipe.passed and pipe.rect.right < bird.rect.left:
                pipe.passed = True
                score += 1
        
        # Draw sprites
        pipe_group.draw(screen)
        ground_group.draw(screen)
        bird_group.draw(screen)
        
        # Check for collisions
        if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
            pygame.mixer.music.load(hit)
            pygame.mixer.music.play()
            state = 'game_over'
        
        # Display score
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10, 10))
    
    elif state == 'game_over':
        # Draw sprites in their last state
        pipe_group.draw(screen)
        ground_group.draw(screen)
        bird_group.draw(screen)
        # Display game over messages (centered)
        game_over_text = big_font.render("Game Over!", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart", True, (255, 0, 0))
        final_score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2))
        screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//2 + 30))
    
    pygame.display.update()
