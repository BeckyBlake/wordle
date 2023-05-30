import pygame
import random
import matplotlib
matplotlib.use('module://pygame_matplotlib.backend_pygame')
import matplotlib.pyplot as plt
import pandas as pd
pygame.init()

df = pd.read_excel('words.xlsx')

# read the 5th column of the excel file
words = df.iloc[:, 5].tolist()
print(type(words))


clock = pygame.time.Clock()

# Set up the Pygame window
width = 600
height = 800
window_size = (width, height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Wordle")

guessed_words = []

game_type = "wordle"

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
green = (50, 168, 82)
yellow = (204, 183, 78)
red = (255, 0, 0)
dark_gray = (100, 100, 100)

answer = "xxxxx"

most_recent_win_type = -1

wins = 0
win_type = [0, 0, 0, 0, 0, 0]
played = 0
max_streak = 0
current_streak = 0
exited_from_play_again = 0

# load the images
stat_img = pygame.image.load("stats.png").convert()
stat_img = pygame.transform.scale(stat_img, (50, 50))

back_img = pygame.image.load("back.png").convert_alpha()
back_img = pygame.transform.scale(back_img, (35, 35))

keyboard_img = pygame.image.load("keyboard.png").convert_alpha()
keyboard_img = pygame.transform.scale(keyboard_img, (50, 70))

wordle_icon_img = pygame.image.load("wordle-icon.png").convert_alpha()
wordle_icon_img = pygame.transform.scale(wordle_icon_img, (50, 50))

visible_img = pygame.image.load("visible.png").convert_alpha()
visible_img = pygame.transform.scale(visible_img, (30, 30))

invisible_img = pygame.image.load("invisible.png").convert_alpha()
invisible_img = pygame.transform.scale(invisible_img, (30, 30))

counter = 0

def set_answer():
    # print("hello")
    global answer, exited_from_play_again, words
    # file = open('words.txt')
    # content = file.readlines()
    line_number = random.randint(0, len(words))
    answer = words[line_number].strip().lower()
    # answer = "later"
    # we know for a fact a new game has started so...
    exited_from_play_again = 0
    print(answer)


# set up boxes
def set_up_boxes():
    for i in range(0, 5):
        for j in range(0, 6):
            box = pygame.Rect(600/4 + i * 65, 800/6 + j * 70, 60, 60)
            pygame.draw.rect(screen, gray, box, 2)
    # box = pygame.Rect(10, 10, 50, 60)
    # pygame.draw.rect(screen, black, box, 2)

# returning -1 means word is too short
# returning 0 means word is not in wordlist
# returning 1 means word is in wordlist but not correct
# returning 2 means word is found and game is over
def check_word():
    global user_input, answer, counter
    if len(user_input) < 5:
        counter = 2
        return -1
    elif user_input == answer:
        return 2
    else:
        # check it's in the words.txt file
        with open("words.txt", "r") as f:
            for line in f:
                if line.strip() == user_input:
                    return 1
        counter = 1
        return 0



current_word = 0

top_row = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
middle_row = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
bottom_row = ['z', 'x', 'c', 'v', 'b', 'n', 'm']

top_row_keys = []
middle_row_keys = []
bottom_row_keys = []

class Button:
    # create a button class
    def __init__(self, color, x, y, width, height, text='', text_color=black, text_size=30):
        self.color = color
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.text = text
        self.text_color = text_color
        self.text_size = text_size


    def draw(self, screen, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0, 5)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0, 5)

        if self.text != '':
            font = pygame.font.Font(None,  self.text_size)
            text = font.render(self.text, 1, self.text_color)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True 
        return False

    def change_color(self, color, text_color=black):
        self.color = color
        self.text_color = text_color

    def get_color(self):
        return self.color

enter_key = Button(gray, 600/10 + 20, 800*3/4 + 110, 70, 50, "ENTER", text_size=25)
backspace_key = Button(gray, 600/4 + 90*4 - 40, 800*3/4 + 110, 70, 50, "")

visibility_of_rows = [1, 1, 1]
back_img_rect = back_img.get_rect(center=(600/4 + 90*4 - 40 + 35, 800*3/4 + 110 + 25))

def set_up_keyboard():
    global top_row_keys, middle_row_keys, bottom_row_keys, game_type, enter_key, backspace_key, back_img_rect

    for i in range(0, 10):
        if game_type == "wordle":
            key = Button(gray, 600/8 + 15 + i * 45, 800*3/4, 40, 50, top_row[i].upper())
        elif game_type == "keyboardle":
            key = Button(gray, 600/8 + 15 + i * 45, 800*1/3, 40, 50, top_row[i].upper(), text_size=20)
        if len(top_row_keys) < 10:
            top_row_keys.append(key)
            
        top_row_keys[i].draw(screen)

    for i in range(0, 9):
        if game_type == "wordle":
            key = Button(gray, 600/6 + 10 + i * 45, 800*3/4 + 55, 40, 50, middle_row[i].upper())
        elif game_type == "keyboardle":
            key = Button(gray, 600/6 + 10 + i * 45, 800*1/3 + 55, 40, 50, middle_row[i].upper(), text_size=20)
        if len(middle_row_keys) < 9:
            middle_row_keys.append(key)

        middle_row_keys[i].draw(screen)

    for i in range(0, 7):
        if game_type == "wordle":
            key = Button(gray, 600/4 + 5 + i * 45, 800*3/4 + 110, 40, 50, bottom_row[i].upper())
        elif game_type == "keyboardle":
            key = Button(gray, 600/4 + 5 + i * 45, 800*1/3 + 110, 40, 50, bottom_row[i].upper(), text_size=20)
        if len(bottom_row_keys) < 7:
            bottom_row_keys.append(key)
        bottom_row_keys[i].draw(screen)
    
    if game_type == "wordle":  
        enter_key = Button(gray, 600/10 + 20, 800*3/4 + 110, 70, 50, "ENTER", text_size=25)
        backspace_key = Button(gray, 600/4 + 90*4 - 40, 800*3/4 + 110, 70, 50, "")
    elif game_type == "keyboardle":
        enter_key = Button(gray, 600/10 + 20, 800*1/3 + 110, 70, 50, "ENTER", text_size=25)
        backspace_key = Button(gray, 600/4 + 90*4 - 40, 800*1/3 + 110, 70, 50, "")
    enter_key.draw(screen) 
    backspace_key.draw(screen)

    if game_type == "wordle":
        back_img_rect = back_img.get_rect(center=(600/4 + 90*4 - 40 + 35, 800*3/4 + 110 + 25))
    elif game_type == "keyboardle":
        back_img_rect = back_img.get_rect(center=(600/4 + 90*4 - 40 + 35, 800*1/3 + 110 + 25))
    screen.blit(back_img, back_img_rect)


def change_keyboard_color(letter, color):
    global top_row_keys, middle_row_keys, bottom_row_keys, top_row, middle_row, bottom_row
    if letter in top_row:
        i = top_row.index(letter)
        if top_row_keys[i].get_color() != green:
            top_row_keys[i].change_color(color, white)
    elif letter in middle_row:
        i = middle_row.index(letter)
        if middle_row_keys[i].get_color() != green:
            middle_row_keys[i].change_color(color, white)
    elif letter in bottom_row:
        i = bottom_row.index(letter)
        if bottom_row_keys[i].get_color() != green:
            bottom_row_keys[i].change_color(color, white)
    

def set_up_colored_boxes():
    global answer
    for i in range(0, len(guessed_words)):
        list = [0, 0, 0, 0, 0]

        for j in range(0, len(guessed_words[i])):
            if (guessed_words[i][j] == answer[j]):
                list[j] = 1
                if game_type == "wordle":
                    box = pygame.Rect(600/4 + j * 65, 800/6 + i * 70, 60, 60)
                    pygame.draw.rect(screen, green, box)
                change_keyboard_color(answer[j], green)

        for j in range(0, len(guessed_words[i])):
            if (guessed_words[i][j] != answer[j]):
                for k in range(0, len(answer)):
                    if (guessed_words[i][j] == answer[k] and list[k] == 0):
                        list[k] = 1
                        if game_type == "wordle":
                            box = pygame.Rect(600/4 + j * 65, 800/6 + i * 70, 60, 60)
                            pygame.draw.rect(screen, yellow, box)
                        change_keyboard_color(answer[k], yellow)
                        break
                else:
                    if game_type == "wordle":
                        box = pygame.Rect(600/4 + j * 65, 800/6 + i * 70, 60, 60)
                        pygame.draw.rect(screen, dark_gray, box)
                    change_keyboard_color(guessed_words[i][j], dark_gray)

def display_user_input():
    if exited_from_play_again == 1:
        return
    y = current_word*70 + 800/6 + 15
    font = pygame.font.Font(None, 50)
    for i in range(0, len(user_input)):
        text = font.render(user_input[i].upper(), True, black)
        text_rect = text.get_rect(center=(600/4 + i * 65 + 30, 800/6 + current_word * 70 + 35))
        screen.blit(text, text_rect)

def display_guessed_words():
    for i in range(0, len(guessed_words)):
        for j in range(0, len(guessed_words[i])):
            font = pygame.font.Font(None, 50)
            text = font.render(guessed_words[i][j].upper(), True, white)
            # box = pygame.Rect(600/4 + i * 65, 800/6 + j * 70, 60, 60)
            text_rect = text.get_rect(center=(600/4 + j * 65 + 30, 800/6 + i * 70 + 35))
            screen.blit(text, text_rect)

user_input = ""

def play_again_request():
    global user_input, current_word, played, exited_from_play_again
    played += 1
    display_stats(1)

def create_graph():
    plt.rcdefaults()
    fig, ax = plt.subplots()

    number_labels = ('1', '2', '3', '4', '5', '6')
    bars = ax.barh(number_labels, win_type, align='center', color='gray')

    # Set a small height for bars with a value of 0
    small_height = max(max(win_type) * 0.05, 0.1)

    if wins == 0:
        ax.set_xlim(0, 1)

    # Add the values as text annotations inside the bars
    for i, bar in enumerate(bars):
        value = win_type[i]
        if value == 0 or bar.get_width() < small_height:
            bar.set_width(small_height)
        ax.annotate(str(value), xy=(bar.get_width() / 2 - 0.025, bar.get_y() + bar.get_height() / 2),
                xytext=(0, 0), textcoords='offset points', ha='left', va='center', fontsize=20, color='white')
        if i == most_recent_win_type:
            bar.set_color((50/256, 168/256, 82/256))
            # (50, 168, 82)

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
    if play_again_flag == 1:
        rectangle = pygame.Rect(width/2, height/2 - 20, 400, 430)
        rectangle.center = (width/2, height * 1.1/2 - 20)
    else:
        rectangle = pygame.Rect(width/2, height/2 - 20, 400, 390)
        rectangle.center = (width/2, height / 2)

    win_percent = 0
    if played == 0:
        win_percent = 0
    else:
        win_percent = round(wins/played * 100)
    
    really_big_font = pygame.font.Font(None, 55)
    really_small_font = pygame.font.Font(None, 20)

    win_percentage = really_big_font.render(str(win_percent), True, black)
    win_rect = win_percentage.get_rect(center=(width*4/9, height/2 - 130))
    win_perc = really_small_font.render("Win %", True, black)
    win_perc_rect = win_perc.get_rect(center=(width*4/9, height/2 - 100))

    cur_streak = really_big_font.render(str(current_streak), True, black)
    cur_streak_rect = cur_streak.get_rect(center=(width*5/9, height/2 - 130))
    cur_streak_text = really_small_font.render("Current\nStreak", True, black)
    cur_streak_text_rect = cur_streak_text.get_rect(center=(width*5/9, height/2 - 92))

    max_streak_text = really_big_font.render(str(max_streak), True, black)
    max_streak_rect = max_streak_text.get_rect(center=(width*6/9, height/2 - 130))
    max_streak_small_text = really_small_font.render("Max\nStreak", True, black)
    max_streak_small_rect = max_streak_small_text.get_rect(center=(width*6/9, height/2 - 92))

    played_text = really_big_font.render(str(played), True, black)
    played_rect = played_text.get_rect(center=(width*3/9, height/2 - 130))
    played_small_text = really_small_font.render("Played", True, black)
    played_small_rect = played_small_text.get_rect(center=(width*3/9, height/2 - 100))
    

    if played == 0:
        rectangle = pygame.Rect(width/2, height/2 - 20, 400, 280)
        rectangle.center = (width/2, height /2 - 60)
        no_data_font = pygame.font.Font(None, 25)
        no_data_text = no_data_font.render("No data", True, black)
        no_data_text_rect = no_data_text.get_rect(center=(width/2, height/2 + 50))
        

    pygame.draw.rect(screen, white, rectangle)
    pygame.draw.rect(screen, gray, rectangle, 2)

    inner_rectangle = pygame.Rect(width/2, height/2 - 20, 190, 60)
    inner_rectangle.center = (width/2, height * 4/5 - 45)

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
                    # reset keyboard colors
                    top_row_keys.clear()
                    middle_row_keys.clear()
                    bottom_row_keys.clear()
                    plt.close()
                    return
                elif exit_rect.collidepoint(mouse_pos):
                    if play_again_flag == 1:
                        exited_from_play_again = 1
                    plt.close()
                    return
                elif not rectangle.collidepoint(mouse_pos):
                    if play_again_flag == 1:
                        exited_from_play_again = 1
                    plt.close()
                    return
        
        pygame.draw.rect(screen, white, rectangle)
        pygame.draw.rect(screen, gray, rectangle, 2)
        exit = font.render("x", True, dark_gray)
        exit_rect = exit.get_rect(center=(width/2 + 180, height/2 - 180))
        graph_rect = fig.get_rect(center=(width/2, height/2 + 65))
        
        if played != 0:
            screen.blit(fig, graph_rect)

        even_smaller_font = pygame.font.Font(None, 25)
        text2 = even_smaller_font.render("GUESS DISTRIBUTION", True, black)
        text2_rect = text2.get_rect(center=(width/2, height/2 - 30))

        text3 = even_smaller_font.render("STATISTICS", True, black)
        text3_rect = text3.get_rect(center=(width/2, height/3 - 40))

        if play_again_flag == 1:
            pygame.draw.rect(screen, green, inner_rectangle)
            # font = pygame.font.Font(None, 50)
            smaller_font = pygame.font.Font(None, 40)
            text = smaller_font.render("Play again?", True, white)
            text_rect = text.get_rect(center=(width/2, height * 4/5 - 45))
            screen.blit(text, text_rect)
    
        screen.blit(exit, exit_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text3, text3_rect)
        screen.blit(win_percentage, win_rect)
        screen.blit(cur_streak, cur_streak_rect)
        screen.blit(max_streak_text, max_streak_rect)
        screen.blit(played_text, played_rect)
        screen.blit(win_perc, win_perc_rect)
        screen.blit(cur_streak_text, cur_streak_text_rect)
        screen.blit(max_streak_small_text, max_streak_small_rect)
        screen.blit(played_small_text, played_small_rect)
        if played == 0:
            screen.blit(no_data_text, no_data_text_rect)
            
        pygame.display.flip()
        plt.close()

def return_key_pressed():
    global user_input, wins, current_word, current_streak, max_streak, played, guessed_words, win_type, play_again_flag, exited_from_play_again, most_recent_win_type
    if check_word() == 1:
        if current_word == 5:
            # loss
            guessed_words.append(user_input)
            current_streak = 0 # :( so sad
            font = pygame.font.Font(None, 50)
            text = font.render(answer, True, white)
            text_rect = text.get_rect(center=(width/2, 130))
            rectangle = pygame.Rect(width/2, 100, 120, 50)
            rectangle.center = (width/2, 130)
            pygame.draw.rect(screen, black, rectangle, 0, 3)
            screen.blit(text, text_rect)
            most_recent_win_type = -1
            play_again_request()
        else:
            current_word += 1
            guessed_words.append(user_input)
            user_input = ""
    elif check_word() == 2:
        wins += 1
        win_type[current_word] += 1
        most_recent_win_type = current_word
        current_word += 1
        current_streak += 1
        if current_streak > max_streak:
            max_streak = current_streak
        guessed_words.append(user_input)
        user_input = ""
        set_up_colored_boxes()
        set_up_keyboard()
        display_guessed_words()
        play_again_request()


not_a_word = pygame.font.Font(None, 30).render("Not in word list", True, black)
not_a_word_rect = not_a_word.get_rect(center=(width/2, 110))

too_few_letters = pygame.font.Font(None, 30).render("Not enough letters", True, black)
too_few_letters_rect = too_few_letters.get_rect(center=(width/2, 110))

set_answer()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return_key_pressed()
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
            elif keyboard_img_rect.collidepoint(event.pos):
                if game_type == "wordle":
                    game_type = "keyboardle"
                    top_row_keys.clear()
                    middle_row_keys.clear()
                    bottom_row_keys.clear()
                elif game_type == "keyboardle":
                    game_type = "wordle"
                    top_row_keys.clear()
                    middle_row_keys.clear()
                    bottom_row_keys.clear()
            elif visibility_top_rect.collidepoint(event.pos):
                visibility_of_rows[0] ^= 1
                top_row_keys.clear()
            elif visibility_middle_rect.collidepoint(event.pos):
                visibility_of_rows[1] ^= 1
                middle_row_keys.clear()
            elif visibility_bottom_rect.collidepoint(event.pos):
                visibility_of_rows[2] ^= 1
                bottom_row_keys.clear()
            else:
                for i in range(len(top_row_keys)):
                    if top_row_keys[i].is_over(event.pos):
                        if len(user_input) != 5:
                            user_input += top_row[i]
                for i in range(len(middle_row_keys)):
                    if middle_row_keys[i].is_over(event.pos):
                        if len(user_input) != 5:
                            user_input += middle_row[i]
                for i in range(len(bottom_row_keys)):
                    if bottom_row_keys[i].is_over(event.pos):
                        if len(user_input) != 5:
                            user_input += bottom_row[i]
                if backspace_key.is_over(event.pos):
                    if len(user_input) != 0:
                        user_input = user_input[:-1]
                if enter_key.is_over(event.pos):
                    return_key_pressed()

    # Clear the screen
    screen.fill(white)
    
    if game_type == "wordle":
        set_up_boxes()
    set_up_keyboard()
    set_up_colored_boxes()
    if game_type == "wordle":
        display_guessed_words()
        display_user_input()
    


    # display "Wordle"
    font = pygame.font.Font(None, 50)
    if game_type == "wordle":
        text = font.render("Wordle", True, black)
    elif game_type == "keyboardle":
        text = font.render("Keyboardle", True, black)
    text_rect = text.get_rect(center=(width/2, 50))
    screen.blit(text, text_rect)
    stat_img_rect = stat_img.get_rect(center=(width*3/4, 50))
    screen.blit(stat_img, stat_img_rect)
    if game_type == "wordle":
        keyboard_img_rect = keyboard_img.get_rect(center=(width*3/4 + 60, 50))
        screen.blit(keyboard_img, keyboard_img_rect)
    elif game_type == "keyboardle":
        wordle_icon_rect = wordle_icon_img.get_rect(center=(width*3/4 + 60, 50))
        screen.blit(wordle_icon_img, wordle_icon_rect)

    if game_type == "keyboardle":
        visibility_top_rect = visible_img.get_rect(center=(40, 290))
        visibility_middle_rect = visible_img.get_rect(center=(40, 345))
        visibility_bottom_rect = visible_img.get_rect(center=(40, 400))

        if visibility_of_rows[0] == 1:
            screen.blit(invisible_img, visibility_top_rect)
        else:
            screen.blit(visible_img, visibility_top_rect)
            for i in range(0, 10):
                top_row_keys[i].change_color(white)
                top_row_keys[i].draw(screen)
        if visibility_of_rows[1] == 1:
            screen.blit(invisible_img, visibility_middle_rect)
        else:
            screen.blit(visible_img, visibility_middle_rect)
            for i in range(0, 9):
                middle_row_keys[i].change_color(white)
                middle_row_keys[i].draw(screen)
        if visibility_of_rows[2] == 1:
            screen.blit(invisible_img, visibility_bottom_rect)
        else:
            screen.blit(visible_img, visibility_bottom_rect)
            for i in range(0, 7):
                bottom_row_keys[i].change_color(white)
                bottom_row_keys[i].draw(screen)
                enter_key.change_color(white)
                enter_key.draw(screen)
                backspace_key.change_color(white)
                backspace_key.draw(screen)
                screen.blit(back_img, back_img_rect)

        # screen.blit(visible_img, visibility_top_rect)
        # screen.blit(visible_img, visibility_middle_rect)
        # screen.blit(visible_img, visibility_bottom_rect)

    if counter > 1024:
        counter = 0

    if counter != 0:
        if counter % 2 == 0:
            screen.blit(too_few_letters, too_few_letters_rect)
        else:
            screen.blit(not_a_word, not_a_word_rect)
        counter = counter + 2
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
