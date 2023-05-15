import pygame
import random
import matplotlib
matplotlib.use('module://pygame_matplotlib.backend_pygame')
import matplotlib.pyplot as plt
import numpy as np
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
red = (255, 0, 0)

answer = "xxxxx"

wins = 0
win_type = [0, 0, 0, 0, 0, 0]
played = 0
max_streak = 0
current_streak = 0
exited_from_play_again = 0


stat_img = pygame.image.load("stats.png").convert()
stat_img = pygame.transform.scale(stat_img, (50, 50))



def set_answer():
    # print("hello")
    global answer, exited_from_play_again
    # file = open('words.txt')
    # content = file.readlines()
    # line_number = random.randint(0, len(content))
    # answer = content[line_number].strip()
    answer = "later"
    # we know for a fact a new game has started so
    exited_from_play_again = 0


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
    if exited_from_play_again == 1:
        return
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

def play_again_request():
    global user_input, current_word, played, exited_from_play_again
    played += 1
    display_stats(1)
    print(guessed_words)
    print("returning from play again")
    # rectangle = pygame.Rect(width/2, height/2, 350, 400)
    # rectangle.center = (width/2, height/2)
    # inner_rectangle = pygame.Rect(width/2, height/2, 280, 100)
    # inner_rectangle.center = (width/2, height/2 + 120)


    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             mouse_pos = event.pos
    #             if inner_rectangle.collidepoint(mouse_pos):
    #                 user_input = ""
    #                 current_word = 0
    #                 guessed_words.clear()
    #                 set_answer()
    #                 return
    #             elif exit_rect.collidepoint(mouse_pos):
    #                 exited_from_play_again = 1
    #                 return
       
    #     pygame.draw.rect(screen, gray, rectangle)
    #     pygame.draw.rect(screen, white, inner_rectangle)
    #     font = pygame.font.Font(None, 50)
    #     text = font.render("Play again?", True, black)
    #     text_rect = text.get_rect(center=(width/2, height/2 + 120))
    #     exit = font.render("x", True, black)
    #     exit_rect = exit.get_rect(center=(width/2 + 150, height/2 - 180))
    #     screen.blit(exit, exit_rect)
    #     screen.blit(text, text_rect)
    #     pygame.display.flip()

def create_graph():
    plt.rcdefaults()
    fig, ax = plt.subplots()

    number_labels = ('1', '2', '3', '4', '5', '6')
    bars = ax.barh(number_labels, win_type, align='center', color='gray')

    # Set a small height for bars with a value of 0
    small_height = max(max(win_type) * 0.05, 0.05)

    # Add the values as text annotations inside the bars
    for i, bar in enumerate(bars):
        value = win_type[i]
        if value == 0:
            bar.set_width(small_height)
        # ax.text(value + 0.01, bar.get_y() + bar.get_height() / 2, str(value),
        #         ha='left', va='center', fontsize=11, color='red', fontweight='bold')
        ax.annotate(str(value), xy=(bar.get_width() / 2 - 0.015, bar.get_y() + bar.get_height() / 2),
                xytext=(3, 0), textcoords='offset points', ha='left', va='center', fontsize=20, color='white')

        label = number_labels[i]
        ax.text(0, bar.get_y() + bar.get_height() / 2, label, ha='right', va='center', fontsize=20)

    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)



    plt.axis('off')
    # Remove the y-axis ticks and labels
    ax.yaxis.set_ticks([])
    ax.set_yticklabels([])


    fig.canvas.draw()
    fig = pygame.transform.scale(fig, (640*1/2, 480*1/2))
    return fig

def display_stats(play_again_flag):
    global exited_from_play_again, wins, played, max_streak, current_streak, win_type, screen, user_input, current_word, guessed_words
    rectangle = pygame.Rect(width/2, height/2, 400, 430)
    rectangle.center = (width/2, height * 1.1/2)

    win_percent = 0
    if played == 0:
        win_percent = 0
    else:
        win_percent = wins/played * 100

    inner_rectangle = pygame.Rect(width/2, height/2, 190, 60)
    inner_rectangle.center = (width/2, height * 4/5)

    fig = create_graph()
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if inner_rectangle.collidepoint(mouse_pos):
                    exited_from_play_again = 0
                    user_input = ""
                    current_word = 0
                    guessed_words.clear()
                    set_answer()
                    return
                elif exit_rect.collidepoint(mouse_pos):
                    if play_again_flag == 1:
                        exited_from_play_again = 1
                    return
                elif not rectangle.collidepoint(mouse_pos):
                    if play_again_flag == 1:
                        exited_from_play_again = 1
                    return
        
        pygame.draw.rect(screen, white, rectangle)
        pygame.draw.rect(screen, gray, rectangle, 2)
        exit = font.render("x", True, black)
        exit_rect = exit.get_rect(center=(width/2 + 180, height/2 - 160))
        graph_rect = fig.get_rect(center=(width/2, height/2 + 70))
        screen.blit(exit, exit_rect)
        if played != 0:
            screen.blit(fig, graph_rect)

        if play_again_flag == 1:
            pygame.draw.rect(screen, green, inner_rectangle)
            # font = pygame.font.Font(None, 50)
            smaller_font = pygame.font.Font(None, 40)
            text = smaller_font.render("Play again?", True, white)
            text_rect = text.get_rect(center=(width/2, height * 4/5))
            screen.blit(text, text_rect)
            
        pygame.display.flip()
        # pygame.display.update()

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if stat_img_rect.collidepoint(event.pos):
                if exited_from_play_again == 1:
                    display_stats(1)
                else:
                    display_stats(0)

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
    stat_img_rect = stat_img.get_rect(center=(width*3/4, height/6))
    screen.blit(stat_img, stat_img_rect)

        
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()