# Add background image and music

import pygame
from pygame.locals import *
import time
import random
from tkinter import *
import pandas as pd
import time as tm



SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

def donothing(var=''):
    pass


class Interface(Tk):
    def __init__(self, name='Interface', size=None):
        super(Interface, self).__init__()
        if size:
            self.geometry(size)
        self.title(name)
        self.frame = Frame(self)
        self.frame.pack()

    def gui_print(self, text='This is some text', command=donothing):
        self.frame.destroy()
        self.frame = Frame(self)
        self.frame.pack()
        Label(self.frame, text=text).pack()
        Button(self.frame, text='Ok', command=command).pack()

    def gui_input(self, text='Enter something', command=donothing):
        self.geometry("400x200")
        self.frame.destroy()
        self.frame = Frame(self ,bg='#ffffff', width=350, height=70)
        self.frame.pack()  
        self.frame.pack_propagate(0)
        Label(self.frame, text=text).pack()
        entry = StringVar(self)
        Entry(self.frame, textvariable=entry).pack()
        Button(self.frame, text='Ok', command=lambda: command(entry.get())).pack()
        
    def handle_enter(self,event) :
        entry = StringVar(self)
        entry.get()
        self.foo(entry)
        
        

    def end(self):
        self.destroy()

    def start(self):
        mainloop()
        
        
    def foo(self, value):
        self.user = value
        self.end()
        
    def bar(self):
        self.gui_input('Fellow Samurai, Please Enter your Gamer Name?', self.foo)
        
    


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120
        

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,25)*SIZE
        self.y = random.randint(1,20)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'
        self.key = K_DOWN      
        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'
        self.key = K_LEFT

    def move_right(self):
        self.direction = 'right'
        self.key = K_RIGHT

    def move_up(self):
        self.direction = 'up'
        self.key = K_UP

    def move_down(self):
        self.direction = 'down'
        self.key = K_DOWN

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            if i%6 == 0 :
                self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
            elif i%6 == 1 :
                self.parent_screen.blit(pygame.image.load("resources/n.jpg").convert(), (self.x[i], self.y[i]))
            elif i%6 == 2 :
                self.parent_screen.blit(pygame.image.load("resources/o.jpg").convert(), (self.x[i], self.y[i]))
            elif i%6 == 3 :
                self.parent_screen.blit(pygame.image.load("resources/k.jpg").convert(), (self.x[i], self.y[i]))
            elif i%6 == 4 :
                self.parent_screen.blit(pygame.image.load("resources/i.jpg").convert(), (self.x[i], self.y[i]))
            elif i%6 == 5 :
                self.parent_screen.blit(pygame.image.load("resources/a.jpg").convert(), (self.x[i], self.y[i]))              
            else :
                self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
            
            

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Nokia Mobile Snake Game")
        main = Interface('Window')
        main.bar()
        main.start()
        self.event = K_ESCAPE



        pygame.mixer.init()
        self.play_background_music()
        
        if len(main.user) == 0 :
            self.player_name = "player" + str(random.randint(1,40))
        else :
            self.player_name = main.user
        #self.surface = pygame.display.set_mode((1920, 1100))
        self.surface = pygame.display.set_mode((1280, 1035))
       
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load('resources/mario.wav')
        pygame.mixer.music.play(-1, 0)
        pygame.mixer.music.play(-1, 0)
       
    def play_sound(self, sound_name):
        if sound_name == "crash": 
            sound = pygame.mixer.Sound("resources/dead.wav")                       
        elif sound_name == 'ding':
            if  self.snake.length %6 == 5 :
                sound = pygame.mixer.Sound("resources/grow.wav")
                sound = pygame.mixer.Sound("resources/grow.wav")
            else :            
                sound = pygame.mixer.Sound("resources/jump2.wav")
            
        pygame.mixer.Sound.play(sound)
        if sound_name == "crash" :        
            pygame.mixer.music.stop()


    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)


    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/SMALL_MONITOR.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1270 and 0 <= self.snake.y[0] <= 1000):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def display_score(self):
        font = pygame.font.SysFont('arial',25)
        player = font.render(f"Player: {self.player_name}",True,(0,0,0))
        self.surface.blit(player,(1075,10))       
        score = font.render(f"Score: {self.snake.length//6}",True,(0,0,0))
        self.surface.blit(score,(1075,35))

    def show_game_over(self):
    
        # reading the csv file
        self.event =  K_ESCAPE
        data = [[self.player_name, self.snake.length//6 , int(tm.time())]]
        df = pd.DataFrame(data)
        df.to_csv('resources/AllDetails.csv',header=False, index=False, mode='a')
        df = pd.read_csv('resources/AllDetails.csv', header=None)
        df = df.sort_values([1, 2], ascending=[False, True])
        df.to_csv('resources/AllDetails.csv',header=False, index=False)
        self.render_background()
        font = pygame.font.SysFont('arial', 45)
        font.set_bold(1)
        line1 = font.render(f"Never Quit, That is the way of Samurai, Your score is {self.snake.length//6}", True, (0, 0, 0))
        self.surface.blit(line1, (100, 100))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (0, 0, 0))
        self.surface.blit(line2, (170, 900))
        line3 = font.render("Top Scores!", True, (0, 0, 0))
        self.surface.blit(line3, (500, 175))
        line5 = font.render("          Name                        Score", True, (0, 0, 0))
        self.surface.blit(line5, (220, 250))
        if(df.shape[0] >= 1):
            line4 = font.render(f"        {df.iloc[0][0]}", True, (0, 0, 0))
            self.surface.blit(line4, (220, 325))
        if(df.shape[0] >= 2):
            line6 = font.render(f"        {df.iloc[1][0]}", True, (0, 0, 0))
            self.surface.blit(line6, (220, 375))
        if(df.shape[0] >= 3):
            line6 = font.render(f"        {df.iloc[2][0]}", True, (0, 0, 0))
            self.surface.blit(line6, (220, 425))
        if(df.shape[0] >= 4):
            line7 = font.render(f"        {df.iloc[3][0]}", True, (0, 0, 0))
            self.surface.blit(line7, (220, 475))
        if(df.shape[0] >= 5):
            line8 = font.render(f"        {df.iloc[4][0]}", True, (0, 0, 0))
            self.surface.blit(line8, (220, 525))
        if(df.shape[0] >=6):
            line4 = font.render(f"        {df.iloc[5][0]}", True, (0, 0, 0))
            self.surface.blit(line4, (220, 575))
        if(df.shape[0] >= 7):
            line6 = font.render(f"        {df.iloc[6][0]}", True, (0, 0, 0))
            self.surface.blit(line6, (220, 625))
        if(df.shape[0] >= 8):
            line6 = font.render(f"        {df.iloc[7][0]}", True, (0, 0, 0))
            self.surface.blit(line6, (220, 675))
        if(df.shape[0] >= 9):
            line7 = font.render(f"        {df.iloc[8][0]}", True, (0, 0, 0))
            self.surface.blit(line7, (220, 725))
        if(df.shape[0] >= 10):
            line8 = font.render(f"        {df.iloc[9][0]}", True, (0, 0, 0))
            self.surface.blit(line8, (220, 775))
        
        if(df.shape[0] >= 1):
            line9 = font.render(f"{df.iloc[0][1]}", True, (0, 0, 0))
            self.surface.blit(line9, (850, 325))
        if(df.shape[0] >= 2):
            line10 = font.render(f"{df.iloc[1][1]}", True, (0, 0, 0))
            self.surface.blit(line10, (850, 375))
        if(df.shape[0] >= 3):
            line11 = font.render(f"{df.iloc[2][1]}", True, (0, 0, 0))
            self.surface.blit(line11, (850, 425))
        if(df.shape[0] >= 4):
            line12 = font.render(f"{df.iloc[3][1]}", True, (0, 0, 0))
            self.surface.blit(line12, (850, 475))
        if(df.shape[0] >= 5):
            line13 = font.render(f"{df.iloc[4][1]}", True, (0, 0, 0))
            self.surface.blit(line13, (850, 525))
        if(df.shape[0] >= 6):
            line9 = font.render(f"{df.iloc[5][1]}", True, (0, 0, 0))
            self.surface.blit(line9, (850, 575))
        if(df.shape[0] >= 7):
            line10 = font.render(f"{df.iloc[6][1]}", True, (0, 0, 0))
            self.surface.blit(line10, (850, 625))
        if(df.shape[0] >= 8):
            line11 = font.render(f"{df.iloc[7][1]}", True, (0, 0, 0))
            self.surface.blit(line11, (850, 675))
        if(df.shape[0] >= 9):
            line12 = font.render(f"{df.iloc[8][1]}", True, (0, 0, 0))
            self.surface.blit(line12, (850, 725))
        if(df.shape[0] >= 10):
            line13 = font.render(f"{df.iloc[9][1]}", True, (0, 0, 0))
            self.surface.blit(line13, (850, 775))


        
        
        
        time.sleep(1)
        pygame.mixer.music.load('resources/naruto.wav')
        pygame.mixer.music.play(-1, 0)
        pygame.mixer.music.play(-1, 0)
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        if(self.event ==  K_RETURN):
                            continue
                        self.event =  K_RETURN
                        main = Interface('Window')
                        main.bar()
                        main.start()
                        if len(main.user) == 0 :
                            self.player_name = "player" + str(random.randint(1,40))
                        else :
                            self.player_name = main.user
        
                        self.play_background_music()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            if self.snake.key == K_RIGHT :
                                continue
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            if self.snake.key == K_LEFT : 
                                continue
                            self.snake.move_right()

                        if event.key == K_UP:
                            if self.snake.key == K_DOWN :
                                continue
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            if self.snake.key == K_UP :
                                continue
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            if self.snake.length < 6 :
                time.sleep(.1)
            elif self.snake.length < 12 :
                time.sleep(.075)
            elif self.snake.length < 18:
                time.sleep(.05)
            elif self.snake.length < 24:
                time.sleep(.025)
            elif self.snake.length < 30 :
                time.sleep(.02)
            elif self.snake.length < 36 :
                time.sleep(.01)
            elif self.snake.length < 42 :
                time.sleep(.005)
            elif self.snake.length < 48 :
                time.sleep(.003)
            else : 
                time.sleep(.002)

            

if __name__ == '__main__':
    game = Game()
    game.run()