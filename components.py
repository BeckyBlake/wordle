import pygame

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
green = (50, 168, 82)
yellow = (204, 183, 78)
red = (255, 0, 0)
dark_gray = (100, 100, 100)

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
    

class ToggleSwitch:
    def __init__(self, x, y, first_color, second_color):
        self.x = x
        self.y = y
        self.first_color = first_color
        self.second_color = second_color
        self.is_on = False

    def draw(self, screen):
        rectangle = pygame.Rect(self.x, self.y, 50, 25)
        if self.is_on == False:
            pygame.draw.rect(screen, self.first_color, rectangle, 0, 10)
            pygame.draw.circle(screen, white, (self.x + 12, self.y + 12), 10)
        else:
            pygame.draw.rect(screen, self.second_color, rectangle, 0, 10)
            pygame.draw.circle(screen, white, (self.x + 38, self.y + 12), 10)

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + 50:
            if pos[1] > self.y and pos[1] < self.y + 25:
                return True 
        return False

    def get_color(self):
        return self.current_color

    def toggle(self):
        if self.is_on == True:
            self.is_on = False
            # self.current_color = self.first_color
        else:
            self.is_on = True
            # self.current_color = self.second_color

    def get_state(self):
        return self.is_on