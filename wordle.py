import pygame
import random
pygame.init()

clock = pygame.time.Clock()


# Set up the Pygame window
width = 600
height = 700
window_size = (width, height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Wordle")

guessed_words = []

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
green = (50, 168, 82)
yellow = (207, 209, 105)

answer = "xxxxx"

wins = 0
win_type = [0, 0, 0, 0, 0, 0]
played = 0
max_streak = 0
current_streak = 0


def set_answer():
    # print("hello")
    global answer
    # file = open('words.txt')
    # content = file.readlines()
    # line_number = random.randint(0, len(content))
    # answer = content[line_number].strip()
    answer = "later"


# set up boxes
def set_up_boxes():
    for i in range(0, 5):
        for j in range(0, 6):
            box = pygame.Rect(600/4 + i * 60, 800/4 + j * 70, 50, 60)
            pygame.draw.rect(screen, black, box, 2)

def check_word():
    if len(user_input) < 5:
        too_few_letters = pygame.font.Font(None, 30).render("Not enough letters", True, black)
        too_few_letters_rect = too_few_letters.get_rect(center=(width/2, 180))
        screen.blit(too_few_letters, too_few_letters_rect)
        pygame.display.flip()
        clock.tick(1)
        return 0
    elif user_input == answer:
        return 2
    else:
        # check it's in the words.txt file
        with open("words.txt", "r") as f:
            for line in f:
                if line.strip() == user_input:
                    return 1
        not_a_word = pygame.font.Font(None, 30).render("Not in word list", True, black)
        # not_a_word.get_rect().center = (width/2, 180)
        not_a_word_rect = not_a_word.get_rect(center=(width/2, 180))
        screen.blit(not_a_word, not_a_word_rect)
        pygame.display.flip()
        clock.tick(1)
        return 0


current_word = 0

def set_up_colored_boxes():
    global answer
    for i in range(0, len(guessed_words)):
        list = [0, 0, 0, 0, 0]
        for j in range(0, len(guessed_words[i])):
            if (guessed_words[i][j] == answer[j]):
                list[j] = 1
                box = pygame.Rect(600/4 + j * 60, 800/4 + i * 70, 50, 60)
                pygame.draw.rect(screen, green, box)
            elif (guessed_words[i][j] != answer[j]):
                for k in range(0, len(answer)):
                    if (guessed_words[i][j] == answer[k] and list[k] == 0):
                        list[k] = 1
                        box = pygame.Rect(600/4 + j * 60, 800/4 + i * 70, 50, 60)
                        pygame.draw.rect(screen, yellow, box)
                        break
                else:
                    box = pygame.Rect(600/4 + j * 60, 800/4 + i * 70, 50, 60)
                    pygame.draw.rect(screen, gray, box)


def display_user_input():
    y = current_word*70 + 800/4 + 10
    font = pygame.font.Font(None, 50)
    for i in range(0, len(user_input)):
        text = font.render(user_input[i], True, black)
        screen.blit(text, (600/4 + i * 60 + 15, y))

def display_guessed_words():
    for i in range(0, len(guessed_words)):
        for j in range(0, len(guessed_words[i])):
            font = pygame.font.Font(None, 50)
            text = font.render(guessed_words[i][j], True, white)
            screen.blit(text, (600/4 + j * 60 + 15, i*70 + 800/4 + 10))


user_input = ""

exited_from_play_again = 0

def play_again_request():
    global user_input, current_word, played, exited_from_play_again
    played += 1
    rectangle = pygame.Rect(width/2, height/2, 350, 400)
    rectangle.center = (width/2, height/2)
    inner_rectangle = pygame.Rect(width/2, height/2, 280, 100)
    inner_rectangle.center = (width/2, height/2 + 120)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if inner_rectangle.collidepoint(mouse_pos):
                    user_input = ""
                    current_word = 0
                    guessed_words.clear()
                    set_answer()
                    return
                elif exit_rect.collidepoint(mouse_pos):
                    exited_from_play_again = 1
                    return
       
        pygame.draw.rect(screen, gray, rectangle)
        pygame.draw.rect(screen, white, inner_rectangle)
        font = pygame.font.Font(None, 50)
        text = font.render("Play again?", True, black)
        text_rect = text.get_rect(center=(width/2, height/2 + 120))
        exit = font.render("x", True, black)
        exit_rect = exit.get_rect(center=(width/2 + 150, height/2 - 180))
        screen.blit(exit, exit_rect)
        screen.blit(text, text_rect)
        pygame.display.flip()


set_answer()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if check_word() == 1:
                    if current_word == 5:
                        font = pygame.font.Font(None, 50)
                        text = font.render(answer, True, black)
                        text_rect = text.get_rect(center=(width/2, 150))
                        rectangle = pygame.Rect(width/2, 100, 120, 50)
                        rectangle.center = (width/2, 150)
                        pygame.draw.rect(screen, black, rectangle, 2)
                        screen.blit(text, text_rect)
                        play_again_request()
                    else:
                        current_word += 1
                        guessed_words.append(user_input)
                        user_input = ""
                elif check_word() == 2:
                    wins += 1
                    win_type[current_word] += 1
                    current_word += 1
                    guessed_words.append(user_input)
                    user_input = ""
                    set_up_colored_boxes()
                    display_guessed_words()
                    play_again_request()
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

    set_up_colored_boxes()

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