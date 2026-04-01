import pygame
import random
import time
from button import Button   # Access Button class and its methods

pygame.init()
clock = pygame.time.Clock()

# ── Constants ──────────────────────────────────────────────────────────
SCREEN_WIDTH  = 500
SCREEN_HEIGHT = 500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simon Says")

GREEN_ON   = (0,   255, 0)
GREEN_OFF  = (0,   227, 0)
RED_ON     = (255, 0,   0)
RED_OFF    = (227, 0,   0)
BLUE_ON    = (0,   0,   255)
BLUE_OFF   = (0,   0,   227)
YELLOW_ON  = (255, 255, 0)
YELLOW_OFF = (227, 227, 0)

# Pass in respective sounds for each color
GREEN_SOUND  = pygame.mixer.Sound("bell1.mp3")
RED_SOUND    = pygame.mixer.Sound("bell2.mp3")
BLUE_SOUND   = pygame.mixer.Sound("bell3.mp3")
YELLOW_SOUND = pygame.mixer.Sound("bell4.mp3")

# ── Button sprite objects ──────────────────────────────────────────────
#   Layout:  [ GREEN  | RED   ]
#            [ BLUE   | YELLOW]
green  = Button(GREEN_ON,  GREEN_OFF,  GREEN_SOUND,  10,  10)
red    = Button(RED_ON,    RED_OFF,    RED_SOUND,    260, 10)
blue   = Button(BLUE_ON,   BLUE_OFF,   BLUE_SOUND,   10,  260)
yellow = Button(YELLOW_ON, YELLOW_OFF, YELLOW_SOUND, 260, 260)

# ── Game variables ─────────────────────────────────────────────────────
colors       = ["green", "red", "blue", "yellow"]
cpu_sequence = []
choice       = ""


# ── draw_board ─────────────────────────────────────────────────────────
def draw_board():
    """Draws all four button sprites onto the pygame window."""
    SCREEN.fill((30, 30, 30))   # dark background between buttons
    green.draw(SCREEN)
    red.draw(SCREEN)
    blue.draw(SCREEN)
    yellow.draw(SCREEN)
    pygame.display.update()


# ── cpu_turn ───────────────────────────────────────────────────────────
def cpu_turn():
    """Chooses a random color, appends it to cpu_sequence, and illuminates it."""
    choice = random.choice(colors)
    cpu_sequence.append(choice)

    if choice == "green":
        green.update(SCREEN)
    elif choice == "red":
        red.update(SCREEN)
    elif choice == "blue":
        blue.update(SCREEN)
    else:
        yellow.update(SCREEN)


# ── repeat_cpu_sequence ────────────────────────────────────────────────
def repeat_cpu_sequence():
    """Replays the full cpu_sequence so the player can memorise it."""
    if len(cpu_sequence) != 0:
        for color in cpu_sequence:
            if color == "green":
                green.update(SCREEN)
            elif color == "red":
                red.update(SCREEN)
            elif color == "blue":
                blue.update(SCREEN)
            else:
                yellow.update(SCREEN)
            pygame.time.wait(500)


# ── player_turn ────────────────────────────────────────────────────────
def player_turn():
    """
    Player has 3 seconds to click each color in the correct order.
    Closes the game if the wrong button is clicked or time runs out.
    """
    turn_time       = time.time()
    players_sequence = []

    while (time.time() <= turn_time + 3
           and len(players_sequence) < len(cpu_sequence)):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Grab the current mouse position
                pos = pygame.mouse.get_pos()

                if green.selected(pos):
                    green.update(SCREEN)
                    players_sequence.append("green")
                    check_sequence(players_sequence)
                    turn_time = time.time()         # reset timer

                elif red.selected(pos):
                    red.update(SCREEN)
                    players_sequence.append("red")
                    check_sequence(players_sequence)
                    turn_time = time.time()

                elif blue.selected(pos):
                    blue.update(SCREEN)
                    players_sequence.append("blue")
                    check_sequence(players_sequence)
                    turn_time = time.time()

                elif yellow.selected(pos):
                    yellow.update(SCREEN)
                    players_sequence.append("yellow")
                    check_sequence(players_sequence)
                    turn_time = time.time()

    # If the player didn't click in time, game over
    if not time.time() <= turn_time + 3:
        game_over()


# ── check_sequence ─────────────────────────────────────────────────────
def check_sequence(players_sequence):
    """Ends the game immediately if the player's move doesn't match the CPU's."""
    if players_sequence != cpu_sequence[:len(players_sequence)]:
        game_over()


# ── game_over ──────────────────────────────────────────────────────────
def game_over():
    """Quits pygame and exits."""
    pygame.quit()
    quit()


# ── Game loop ──────────────────────────────────────────────────────────
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            quit()

    pygame.display.update()
    draw_board()            # draw buttons onto the screen
    repeat_cpu_sequence()   # replay the sequence so far
    cpu_turn()              # CPU adds one new random color
    player_turn()           # player tries to match the sequence
    pygame.time.wait(1000)  # pause before next round
    clock.tick(60)
