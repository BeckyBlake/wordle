import pygame
pygame.init()

# Set up the Pygame window
width = 600
height = 800
window_size = (width, height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Wordle")

guessed_words = []

# define colors
white = (255, 255, 255)
black = (0, 0, 0)

# set up boxes
def set_up_boxes():
    for i in range(0, 5):
        for j in range(0, 6):
            box = pygame.Rect(600/4 + i * 60, 800/4 + j * 70, 50, 60)
            pygame.draw.rect(screen, black, box, 2)
    # box = pygame.Rect(10, 10, 50, 60)
    # pygame.draw.rect(screen, black, box, 2)

def check_valid_word():
    return 1

current_word = 0

def display_user_input():
    y = current_word*70 + 800/4 + 10
    font = pygame.font.Font(None, 50)
    text = font.render(user_input, True, black)
    # text_rect = text.get_rect(width/2, y)
    screen.blit(text, (width/2, y))

def display_guessed_words():
    for i in range(0, len(guessed_words)):
        font = pygame.font.Font(None, 50)
        text = font.render(guessed_words[i], True, black)
        screen.blit(text, (width/2, i*70 + 800/4 + 10))


user_input = ""

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if check_valid_word() == 1:
                    current_word += 1
                    guessed_words.append(user_input)
                    user_input = ""
            elif event.key == pygame.K_BACKSPACE:
                if len(user_input) != 0:
                    user_input = user_input[:-1]
            else:
                if len(user_input) != 5:
                    user_input += event.unicode
                    # print(user_input)

    # Clear the screen
    screen.fill(white)
    
    set_up_boxes()

    display_guessed_words()

    display_user_input()

    # display "Wordle"
    font = pygame.font.Font(None, 50)
    text = font.render("Wordle", True, black)
    text_rect = text.get_rect(center=(width/2, 50))
    screen.blit(text, text_rect)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()