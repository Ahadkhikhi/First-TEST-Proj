import pygame
from pygame.locals import *
import random

pygame.init()

#framerate controler
Clock = pygame.time.Clock()
fps = 60
#Limite frame rate to 60

screen_wideth = 700
screen_hight = 700

#Create Screen game display and Arguments
screen = pygame.display.set_mode((screen_wideth, screen_hight))
#Finish screen display+Title Name
pygame.display.set_caption('Flappy Bird')

#define fonts
font = pygame.font.SysFont('Bauhas 93', 60)

#define colors
white = (255, 255, 255)

#Game Variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 185
pipe_frequency = 1500 #mS
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

#load images
bg = pygame.image.load('img\Background.png')
ground_img = pygame.image.load('img\ground.png')
button_img = pygame.image.load("img\Restart.png")

#Draw text on display
def draw_text(text, font, text_col, X, Y,):
    img = font.render(text, True, text_col)
    screen.blit(img,(X, Y))

#Reset game function    
def Reset_Game():
    Pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_hight / 2)
    score = 0
    return score

#Create Player icon+behaiviar
class Bird(pygame.sprite.Sprite):
    def __init__(self ,x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img\Bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        


    def update(self):
        #Gravity
        if flying == True:
         self.vel += 0.5
         if self.vel > 8:
             self.vel = 8
         if self.rect.bottom < 563:
             self.rect.y += int(self.vel)
             
        if game_over == False:
          #jump
          if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
              self.clicked = True
              self.vel = -10
          if pygame.mouse.get_pressed()[0] == 0:
              self.clicked = False
          #Animation 
          self.counter += 1
          flap_cooldown = 5
          
          if self.counter > flap_cooldown:
              self.counter = 0
              self.index += 1
              if self.index >= len(self.images):
                  self.index = 0
          self.image = self.images[self.index]
          self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
            
#create لوله class&& showin display
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, possition):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img\Pipe.png")
        self.rect = self.image.get_rect()
        #Possition 1 is frim top and -1 is botoom
        if possition == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y -int(pipe_gap / 2)]
        if possition == -1:
         self.rect.topleft = [x, y + int(pipe_gap / 2)]
         
 #Function updater after passing لوله seccesfuly        
    def update(self):
        self.rect.x -= scroll_speed
        #remove pipe after earning scores   
        if self.rect.right < 0:
            self.kill() 


#Create ResetBTN bihavar            
class Button():
    def __init__(self, X, Y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (X, Y)


#showing Reset BTN on display        
    def draw(self):
        
        action = False
        
        #mouse possition
        pos = pygame.mouse.get_pos()
        
        #if mouse is on Reset BTN
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        #draw BTN
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
        
#Manage item Game
#Sprite For manage items and put theme in groups
bird_group = pygame.sprite.Group()
Pipe_group = pygame.sprite.Group()

#int(screen_height / 2) for Y pos
flappy = Bird(100, int(screen_hight / 2))
bird_group.add(flappy)

#-1 for select position if 1its up and if -1 its down
btm_pipe = Pipe(300, int(screen_hight / 2), -1)
Pipe_group.add(btm_pipe)

#Create reset BTN 
button = Button(screen_wideth // 2 -50, screen_hight // 2 - 100, button_img)


#Gameloop Rules
run = True
while run:
    Clock.tick(fps)
    screen.blit(bg, (0, -185))
    bird_group.draw(screen)
    bird_group.update()
    Pipe_group.draw(screen)
    
    #draw ground
    screen.blit(ground_img, (ground_scroll, 565))
    
    
    #check for score
    if len(Pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > Pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < Pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > Pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
                
    draw_text(str(score), font, white, int(screen_wideth / 2), 20)
    if pygame.sprite.groupcollide(bird_group, Pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    #check if bird hit ground
    if flappy.rect.bottom > 565:
        game_over = True
        flying = False
        
    if game_over == False and flying == True:
      #make new pipes
      #محاسبه تایم بازی از ابتدا تا زمان اجزا بر حسب میلی ثانیه
      time_now  = pygame.time.get_ticks()
      if time_now - last_pipe > pipe_frequency:
          pipe_height = random.randint(-100, 100)
          btm_pipe = Pipe(screen_wideth, int(screen_hight /2) + pipe_height, -1)
          top_pipe = Pipe(screen_wideth, int(screen_hight /2) + pipe_height, 1)
          Pipe_group.add(btm_pipe)
          Pipe_group.add(top_pipe)
          last_pipe = time_now          
          
      #move the ground
      ground_scroll -= scroll_speed 
      if abs(ground_scroll) > 35:
          ground_scroll = 0
           
      Pipe_group.update()
      
    #check for game over and reset
    if game_over == True:
       if button.draw() == True:
           game_over = False
           score = Reset_Game()
           
           
           
#تنظیم وقفه‌ها، زمان‌بندی رویدادها، و اندازه‌گیری مدت زمان           
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    
            
#update display and Apply GUI             
    pygame.display.update()



#Quit the game and close all library that used for design apps
pygame.quit()