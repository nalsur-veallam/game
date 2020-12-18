import pygame
from pygame.draw import *
from game import Game
import time


class Menu:
    
    def __init__(self):
        # Инициализируем пайгейм
        pygame.init()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        pygame.display.update()
        
        # Размеры окна
        self.WINDOW_X, self.WINDOW_Y = pygame.display.get_surface().get_size()
        self.ORIGINAL_WINDOW_X = 1920
        self.ORIGINAL_WINDOW_Y = 1080
        self.RATIO_X = self.WINDOW_X/self.ORIGINAL_WINDOW_X
        self.RATIO_Y = self.WINDOW_Y/self.ORIGINAL_WINDOW_Y
        

        # Подгружаем музыку на фон
        pygame.mixer.music.load('sounds/menu_sound.wav')

        # Выгружаем настройки из файла
        f = open('saves/settings.txt', 'r')
        l = [line.strip() for line in f]
        self.volume = int(l[0])
        self.map_size = int(l[1])
        f.close()

        # Подгружаем картинки меню
        self.logo = pygame.image.load('resources/menu/logo.png')
        self.logo = pygame.transform.scale(self.logo, (self.WINDOW_X, self.WINDOW_Y))
        self.screenshot = pygame.image.load('resources/menu/screenshot.png')
        self.screenshot = pygame.transform.scale(self.screenshot, (self.WINDOW_X, self.WINDOW_Y))
        self.buttons = [pygame.image.load('resources/menu/new_game_button.png'),
                        pygame.image.load('resources/menu/load_game_button.png'),
                        pygame.image.load('resources/menu/settings_button.png'),
                        pygame.image.load('resources/menu/exit_button.png'),
                        pygame.image.load('resources/menu/click_button.png')]
        self.BUTTON_SIZE_X = 600
        self.BUTTON_SIZE_X = int(600*self.RATIO_X)
        self.BUTTON_SIZE_Y = 200
        self.BUTTON_SIZE_Y = int(200*self.RATIO_Y)
        for i in range(0, len(self.buttons)):
            self.buttons[i] = pygame.transform.scale(self.buttons[i], (self.BUTTON_SIZE_X, self.BUTTON_SIZE_Y))
        
        # Подгружаем картинки настроек
        self.settings_page = pygame.image.load('resources/menu/settings_page.png')
        self.settings_page = pygame.transform.scale(self.settings_page, (int(self.WINDOW_X/2), int(self.WINDOW_Y/2)))
        self.size_images = [pygame.image.load('resources/menu/size_1.png'),
                             pygame.image.load('resources/menu/size_2.png'),
                             pygame.image.load('resources/menu/size_3.png')]
        for i in range(0, len(self.size_images)):
            self.size_images[i] = pygame.transform.scale(self.size_images[i], (int(self.WINDOW_X/2), int(self.WINDOW_Y/2)))
        self.volume_images = [pygame.image.load('resources/menu/volume_0.png'),
                              pygame.image.load('resources/menu/volume_1.png'),
                              pygame.image.load('resources/menu/volume_2.png'),
                              pygame.image.load('resources/menu/volume_3.png'),
                              pygame.image.load('resources/menu/volume_4.png'),
                              pygame.image.load('resources/menu/volume_5.png'),]
        for i in range(0, len(self.volume_images)):
            self.volume_images[i] = pygame.transform.scale(self.volume_images[i], (int(self.WINDOW_X/2), int(self.WINDOW_Y/2)))
        
        # Константы для меню
        self.finished = False
        self.LOGO_TIME = 3000
        self.BUTTON_X = int(self.WINDOW_X / 10)
        self.BUTTON_Y = int(self.WINDOW_Y - 4*self.BUTTON_SIZE_Y - self.WINDOW_Y / 40)
        self.SETTINGS_X = int(self.WINDOW_X/4)
        self.SETTINGS_Y = int(self.WINDOW_Y/4)
        self.VOLUME_MINUS_X = int(self.WINDOW_X/4 + self.WINDOW_X/20)
        self.VOLUME_MINUS_Y = int(self.WINDOW_Y/4 + self.WINDOW_Y*3/20)
        self.VOLUME_PLUS_X = int(self.WINDOW_X/4 + self.WINDOW_X*9/20)
        self.VOLUME_PLUS_Y = int(self.WINDOW_Y/4 + self.WINDOW_Y*3/20)
        self.VOLUME_BUTTON_SIZE = 30 * self.RATIO_Y
        self.SIZE_BUTTON_X = int(self.WINDOW_X/4 + self.WINDOW_X*7/80)
        self.SIZE_BUTTON_Y =  int(self.WINDOW_Y*3/4 - self.WINDOW_Y/8)
        self.SIZE_BUTTON_COUNT = 320 * self.RATIO_X
        self.SIZE_BUTTON_SIZE = 50  * self.RATIO_Y
        self.SEED = 15
        
        # Координаты мыши
        self.mouse_pos_x = 0
        self.mouse_pos_y = 0
        

    def main(self):
        self.screen.blit(self.logo, (0, 0))
        pygame.display.update()
        pygame.time.delay(self.LOGO_TIME)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.volume/5)
        
        while not self.finished:
            self.screen.blit(self.screenshot, (0, 0))
            
            for i in range(0, len(self.buttons) - 1):
                self.screen.blit(self.buttons[i], (self.BUTTON_X, self.BUTTON_Y + self.BUTTON_SIZE_Y*i))
                
                if (self.mouse_pos_x > self.BUTTON_X 
                    and self.mouse_pos_x < self.BUTTON_SIZE_X + self.BUTTON_X):
                    if (self.mouse_pos_y > self.BUTTON_Y + self.BUTTON_SIZE_Y*i 
                        and self.mouse_pos_y < self.BUTTON_Y + self.BUTTON_SIZE_Y*(i + 1)):
                        self.screen.blit(self.buttons[4], (self.BUTTON_X, self.BUTTON_Y + self.BUTTON_SIZE_Y*i))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True  
                
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_pos_x, self.mouse_pos_y = event.pos
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    # EXIT 
                    if x > self.BUTTON_X and x < self.BUTTON_SIZE_X + self.BUTTON_X:
                        if (y > self.BUTTON_Y + self.BUTTON_SIZE_Y*3 
                            and y < self.BUTTON_Y + self.BUTTON_SIZE_Y*(3 + 1)):
                            pygame.quit()
                    # NEWGAME 
                    if x > self.BUTTON_X and x < self.BUTTON_SIZE_X + self.BUTTON_X:
                        if (y > self.BUTTON_Y + self.BUTTON_SIZE_Y*0 
                            and y < self.BUTTON_Y + self.BUTTON_SIZE_Y*(0 + 1)):
                            pygame.quit()
                            game = Game(self.SEED, self.map_size, self.volume)
                            game.main()
                            
                    # LOADGAME 
                    if x > self.BUTTON_X and x < self.BUTTON_SIZE_X + self.BUTTON_X:
                        if (y > self.BUTTON_Y + self.BUTTON_SIZE_Y*1 
                            and y < self.BUTTON_Y + self.BUTTON_SIZE_Y*(1 + 1)):
                            pass
                    # SETTINGS
                    if x > self.BUTTON_X and x < self.BUTTON_SIZE_X + self.BUTTON_X:
                        if (y > self.BUTTON_Y + self.BUTTON_SIZE_Y*2 
                            and y < self.BUTTON_Y + self.BUTTON_SIZE_Y*(2 + 1)):
                            menu.change_settings()
                
            keys = pygame.key.get_pressed()
            
            pygame.display.update()
                
        pygame.quit()
    
    
    def change_settings(self):
        set_finished = False
        while not set_finished:
            self.screen.blit(self.settings_page, (self.SETTINGS_X, self.SETTINGS_Y))
            self.screen.blit(self.volume_images[self.volume], (self.SETTINGS_X, self.SETTINGS_Y))
            self.screen.blit(self.size_images[self.map_size - 1], (self.SETTINGS_X, self.SETTINGS_Y))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (x > self.VOLUME_MINUS_X - self.VOLUME_BUTTON_SIZE 
                        and x < self.VOLUME_MINUS_X + self.VOLUME_BUTTON_SIZE):
                        if (y > self.VOLUME_MINUS_Y - self.VOLUME_BUTTON_SIZE 
                            and y < self.VOLUME_MINUS_Y + self.VOLUME_BUTTON_SIZE):
                            if self.volume > 0:
                                self.volume -= 1
                                pygame.mixer.music.set_volume(self.volume/5)
                    
                    if (x > self.VOLUME_PLUS_X - self.VOLUME_BUTTON_SIZE 
                        and x < self.VOLUME_PLUS_X + self.VOLUME_BUTTON_SIZE):
                        if (y > self.VOLUME_PLUS_Y - self.VOLUME_BUTTON_SIZE 
                            and y < self.VOLUME_PLUS_Y + self.VOLUME_BUTTON_SIZE):
                            if self.volume < 5:
                                self.volume += 1
                                pygame.mixer.music.set_volume(self.volume/5)
                                
                    if (x > self.SIZE_BUTTON_X - self.SIZE_BUTTON_SIZE
                        and x < self.SIZE_BUTTON_X + self.SIZE_BUTTON_SIZE):
                        if (y > self.SIZE_BUTTON_Y - self.SIZE_BUTTON_SIZE 
                            and y < self.SIZE_BUTTON_Y + self.SIZE_BUTTON_SIZE):
                            self.map_size = 1
                                
                    if (x > self.SIZE_BUTTON_X + self.SIZE_BUTTON_COUNT - self.SIZE_BUTTON_SIZE
                        and x < self.SIZE_BUTTON_X + self.SIZE_BUTTON_COUNT + self.SIZE_BUTTON_SIZE):
                        if (y > self.SIZE_BUTTON_Y - self.SIZE_BUTTON_SIZE 
                            and y < self.SIZE_BUTTON_Y + self.SIZE_BUTTON_SIZE):
                            self.map_size = 2
                            
                    if (x > self.SIZE_BUTTON_X + 2*self.SIZE_BUTTON_COUNT - self.SIZE_BUTTON_SIZE
                        and x < self.SIZE_BUTTON_X + 2*self.SIZE_BUTTON_COUNT + self.SIZE_BUTTON_SIZE):
                        if (y > self.SIZE_BUTTON_Y - self.SIZE_BUTTON_SIZE 
                            and y < self.SIZE_BUTTON_Y + self.SIZE_BUTTON_SIZE):
                            self.map_size = 3
                                
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                f = open('saves/settings.txt', 'w')
                f.write(str(self.volume) + '\n')
                f.write(str(self.map_size))
                f.close()
                return 0
            
            
            pygame.display.update()
            




menu = Menu()
menu.main()

