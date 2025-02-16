import sys
import pygame
from pygame.locals import *
from src.Game import main_game   # Ensure main_game.py defines a function named 'main'
from src.GA import ga_game       # Ensure ga_game.py defines a function named 'ga_main'

def main():
    pygame.init()
    # Set up a simple window for mode selection
    menu_screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Flappy Bird - Mode Selection")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    mode = None

    # Simple Pygame loop for mode selection
    while mode is None:
        menu_screen.fill((0, 0, 0))  # Black background

        title_text = font.render("Select Mode:", True, (255, 255, 255))
        option1_text = font.render("1: Play Flappy Bird", True, (255, 255, 255))
        option2_text = font.render("2: Run GA Training", True, (255, 255, 255))

        menu_screen.blit(title_text, (50, 150))
        menu_screen.blit(option1_text, (50, 200))
        menu_screen.blit(option2_text, (50, 250))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in (K_1, K_KP1):
                    mode = "1"
                elif event.key in (K_2, K_KP2):
                    mode = "2"

        clock.tick(30)

    # Reinitialize the display for the game mode
    game_screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Flappy Bird")

    if mode == "1":
        main_game.main()    # Launch the manual game
    elif mode == "2":
        ga_game.ga_main()   # Launch the GA simulation

if __name__ == "__main__":
    main()
