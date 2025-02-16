import sys
import pygame
from pygame.locals import *
from src.Game import main_game   # your existing manual game module
from src.GA import ga_game       # the GA simulation module

def main():
    pygame.init()
    # Set up a simple window for mode selection
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Flappy Bird - Mode Selection")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    mode = None

    # Simple Pygame loop for mode selection
    while mode is None:
        screen.fill((0, 0, 0))  # Black background

        title_text = font.render("Select Mode:", True, (255, 255, 255))
        option1_text = font.render("1: Play Flappy Bird", True, (255, 255, 255))
        option2_text = font.render("2: Run GA Training", True, (255, 255, 255))

        screen.blit(title_text, (50, 150))
        screen.blit(option1_text, (50, 200))
        screen.blit(option2_text, (50, 250))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # Detect number key presses (both main keyboard and keypad)
                if event.key in (K_1, K_KP1):
                    mode = "1"
                elif event.key in (K_2, K_KP2):
                    mode = "2"

        clock.tick(30)

    # Once mode is chosen, quit the menu display before launching the game
    pygame.display.quit()

    # Launch the selected mode
    if mode == "1":
        main_game.main()  # Launch the manual game
    elif mode == "2":
        ga_game.ga_main()  # Launch the GA simulation

if __name__ == "__main__":
    main()
