import time
import random
import pygame
import numpy as np
from pygame.draw import *
from map_generator import generate_map
from objects import Player, Backpack
from biome_generator import biome_generator, water_generator


class Game:
    def __init__(self, seed, size, volume):
        # Константы генерации карты
        self.SEED = 15
        self.SIZE = int(1024 * size)
        self.H_MAX = 20
        self.SHARP = 2
        self.DEPTH = 100
        self.PROBABILITY = 1/2
        self.H_0 = 12
        self.LAKES_NUMBER = int(10*size)
        
        # Инициализируем пайгейм
        pygame.init()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        pygame.display.update()
        self.clock = pygame.time.Clock()
        
        # Константы игры
        self.FPS = 20    
        self.finished = False
        self.BLOCK_SIZE = 20
        self.DO_RADIUS = 140
        self.inventory_bool = False
        self.volume = volume
        
        # Размеры окна
        self.WINDOW_X, self.WINDOW_Y = pygame.display.get_surface().get_size()
        self.ORIGINAL_WINDOW_X = 1920
        self.ORIGINAL_WINDOW_Y = 1080
        self.RATIO_X = self.WINDOW_X/self.ORIGINAL_WINDOW_X
        self.RATIO_Y = self.WINDOW_Y/self.ORIGINAL_WINDOW_Y        
        
        # Подгружаем текстуры карты
        self.dirt_grass = pygame.image.load('resources/map/dirt_grass.png')

        self.blocks = [[pygame.image.load('resources/map/dirt.png'), 
                        pygame.image.load('resources/map/stone.png')],
                       [pygame.image.load('resources/map/snow.png'), 
                        pygame.image.load('resources/map/ice.png')]]

        self.water = [pygame.image.load('resources/map/water.png'), 
                      pygame.image.load('resources/map/ice_water.png')]
        
        # Подгружаем текстуры персонажа
        self.player_animation = [pygame.image.load('resources/player_animation/player_right.png'), 
                    pygame.image.load('resources/player_animation/move_right_1.png'),
                    pygame.image.load('resources/player_animation/move_right_2.png'),
                    pygame.image.load('resources/player_animation/player_left.png'), 
                    pygame.image.load('resources/player_animation/move_left_1.png'),
                    pygame.image.load('resources/player_animation/move_left_2.png')]
        
        # Подгружаем бэкграунд
        self.bg = pygame.image.load('resources/bg.png')
        self.bg = pygame.transform.scale(self.bg, (self.WINDOW_X, self.WINDOW_Y))
        
        # Подгружаем текстуры инвентаря
        self.inventory_image = pygame.image.load('resources/inventory/inventory.png')
        self.INVENTORY_IMAGE_SIZE_X = int(1000*self.RATIO_X)
        self.INVENTORY_IMAGE_SIZE_Y = int(100*self.RATIO_Y)
        self.inventory_image = pygame.transform.scale(self.inventory_image, (self.INVENTORY_IMAGE_SIZE_X, self.INVENTORY_IMAGE_SIZE_Y))
        
        self.tools_invent = [pygame.image.load('resources/inventory/inventory_image/dirt.png'),
                             pygame.image.load('resources/inventory/inventory_image/stone.png')]
        self.TOOLS_INVENT_SIZE_X = int(100*self.RATIO_X)
        self.TOOLS_INVENT_SIZE_Y = int(100*self.RATIO_Y)
        for i in range(0, len(self.tools_invent)):
            self.tools_invent[i] = pygame.transform.scale(self.tools_invent[i], (self.TOOLS_INVENT_SIZE_X, self.TOOLS_INVENT_SIZE_Y))                           

        self.cell = pygame.image.load('resources/inventory/cell.png')
        self.CELL_SIZE_X = int(100*self.RATIO_X)
        self.CELL_SIZE_Y = int(120*self.RATIO_Y)
        self.cell = pygame.transform.scale(self.cell, (self.CELL_SIZE_X, self.CELL_SIZE_Y))
        
        # Подгружаем текстуры инструментов
        self.tools_images = [[pygame.image.load('resources/tools/shovel.png'),
                         pygame.image.load('resources/tools/pick.png')],
                        [pygame.image.load('resources/tools/shovel_right.png'),
                         pygame.image.load('resources/tools/pick_right.png')],     
                        [pygame.image.load('resources/tools/shovel_right_1.png'), 
                         pygame.image.load('resources/tools/pick_right_1.png')],
                        [pygame.image.load('resources/tools/shovel_right_2.png'), 
                         pygame.image.load('resources/tools/pick_right_2.png')],
                        [pygame.image.load('resources/tools/shovel_left.png'),
                         pygame.image.load('resources/tools/pick_left.png')],
                        [pygame.image.load('resources/tools/shovel_left_1.png'),
                         pygame.image.load('resources/tools/pick_left_1.png')],
                        [pygame.image.load('resources/tools/shovel_left_2.png'),
                         pygame.image.load('resources/tools/pick_left_2.png')]]
        for i in range(0, 2):
            self.tools_images[0][i] = pygame.transform.scale(self.tools_images[0][i], (self.TOOLS_INVENT_SIZE_X, self.TOOLS_INVENT_SIZE_Y))  
            
        self.check = pygame.image.load('resources/tools/check.png')
        self.check = pygame.transform.scale(self.check, (self.TOOLS_INVENT_SIZE_X, self.TOOLS_INVENT_SIZE_Y))
        
        # Создаем карту
        self.map = generate_map(self.SEED, self.SIZE, self.H_MAX, self.SHARP, self.DEPTH, self.PROBABILITY) 
        self.biome_map, map = biome_generator(self.SEED, self.DEPTH, self.SIZE, self.map, self.LAKES_NUMBER)
        
        # Создаем персонажа и его рюкзак
        self.player = Player(self.SIZE/2, self.H_0, self.DEPTH)
        self.player.y_calculation(self.map, self.H_MAX)
        self.backpack = Backpack()
        
        # Загружаем музыку
        pygame.mixer.music.load('sounds/background_music.wav')
        
        #Загружаем шрифт
        pygame.font.init()
        self.font_1 = pygame.font.Font(None, 36)
        
        
    def draw_map(self, x, y, H):
        self.screen.blit(self.bg, (0, 0))
        
        for i in range(0, int(self.WINDOW_X/self.BLOCK_SIZE)):
            h = -1
            for j in range(1, 1 + y + self.H_0 - H):
                if self.map[j][x - int(self.WINDOW_X/self.BLOCK_SIZE/2) + i] != 0:
                    h = y - j + self.H_0 - H
                    break
                
            if h >= 0:
                # Рисуем верхние блоки
                if self.biome_map[y + self.H_0 - H - h][x - int(self.WINDOW_X/self.BLOCK_SIZE/2) + i] == 0.5: 
                    self.screen.blit(self.dirt_grass,(20*i, self.WINDOW_Y - 20*(h)))
                elif self.biome_map[y + self.H_0 - H - h][x - int(self.WINDOW_X/self.BLOCK_SIZE/2) + i]  > 2:
                    self.screen.blit(self.blocks[1][int(self.map[y + self.H_0 - H - h][x - int(self.WINDOW_X/self.BLOCK_SIZE/2) + i] - 1)], (20*i, self.WINDOW_Y - 20*(h)))
                elif self.map[y + self.H_0 - H - h][x - int(self.WINDOW_X/self.BLOCK_SIZE/2) + i] > 0.5:
                    self.screen.blit(self.blocks[0][int(self.map[y + self.H_0 - H - h][x - int(self.WINDOW_X/self.BLOCK_SIZE/2) + i] - 1)], (20*i, self.WINDOW_Y - 20*h))
                    
                #Рисуем твердые блоки
                for j in range(y + self.H_0 - H - h + 1, 1 + y + self.H_0 - H): 
                    if self.biome_map[j][x - int(self.WINDOW_X/self.BLOCK_SIZE/2) + i]  > 2:
                        self.screen.blit(self.blocks[1][int(self.map[j][x - int(self.WINDOW_X/self.BLOCK_SIZE/2) + i] - 1)], (20*i, self.WINDOW_Y - 20*(y - j + self.H_0 - H)))
                    elif self.map[j][x - int(self.WINDOW_X/self.BLOCK_SIZE/2) + i] > 0:
                        self.screen.blit(self.blocks[0][int(self.map[j][x - int(self.WINDOW_X/self.BLOCK_SIZE/2) + i] - 1)], (20*i, self.WINDOW_Y - 20*(y - j + self.H_0 - H)))
        
            #Рисуем воду
            for j in range(1 + y + self.H_0 - H - int(self.WINDOW_Y/self.BLOCK_SIZE), 1 + y + self.H_0 - H):  
                if self.biome_map[j][x - int(self.WINDOW_X/self.BLOCK_SIZE/2) + i] < 0:
                    self.screen.blit(self.water[0], (20*i, self.WINDOW_Y - 20*(y - j + self.H_0 - H)))
                    
                    
    def draw_player(self, number, height):
        self.screen.blit(self.player_animation[number], (self.WINDOW_X/2, self.WINDOW_Y - self.H_0*self.BLOCK_SIZE - height))
    
    
    def draw_inventory(self, inventory, hand, hand_image, height):
        self.screen.blit(self.inventory_image, (0, 0))
        self.screen.blit(self.check, ((hand - 1)*self.TOOLS_INVENT_SIZE_X, 0))
        for i in range(0, len(inventory)):
            if inventory[i] != 0:
                self.screen.blit(self.tools_images[0][inventory[i] - 1], (i*self.TOOLS_INVENT_SIZE_X, 0))
                if hand_image == 4:
                    self.screen.blit(self.tools_images[4][hand - 1], (self.WINDOW_X/2 - 30, self.WINDOW_Y - self.H_0*self.BLOCK_SIZE - 150))
                elif hand_image == 1:
                    self.screen.blit(self.tools_images[1][hand - 1], (self.WINDOW_X/2 - 30, self.WINDOW_Y - self.H_0*self.BLOCK_SIZE - 150))
                else:
                    self.screen.blit(self.tools_images[hand_image][hand - 1], (self.WINDOW_X/2, self.WINDOW_Y - self.H_0*self.BLOCK_SIZE - height))
            
        if self.inventory_bool:
            slots, count, size = self.backpack.show()
            for i in range(0, size):
                self.screen.blit(self.cell, (300 + 100*(i - 4*(i//4)), 100 + 120*(i//4)))
                if slots[i] != 0:
                    self.screen.blit(self.tools_invent[int(slots[i] - 1)], (310 + 100*(i - 4*(i//4)), 110 + 120*(i//4)))
                    self.screen.blit(self.font_1.render(str(count[i]), True, (0, 0, 0)), (380 + 100*(i - 4*(i//4)), 195 + 120*(i//4)))
        
    
    # Проверка на воду
    def water_check(self, i, j):
        if self.biome_map[i-1][j] == -1 or self.biome_map[i][j-1] == -1 or self.biome_map[i][j+1] == -1:
            self.biome_map[i][j] = -1
            if self.map[i][j-1] == 0 and self.biome_map[i][j-1] >= 0:
                self.water_check(i, j-1)
            if self.map[i][j+1] == 0 and self.biome_map[i][j+1] >= 0:
                self.water_check(i, j+1)
            if self.map[i+1][j] == 0 and self.biome_map[i+1][j] >= 0:
                self.water_check(i+1, j)
                
                
    #
    def doing(self, x, y, player_x, player_y, type, height):
        if (x > self.WINDOW_X/2 + self.BLOCK_SIZE - self.DO_RADIUS 
            and x < self.WINDOW_X/2 + self.BLOCK_SIZE + self.DO_RADIUS):
            if (y > self.WINDOW_Y - self.H_0*self.BLOCK_SIZE - height/2 - self.DO_RADIUS 
                and y < self.WINDOW_Y - self.H_0*self.BLOCK_SIZE - height/2 + self.DO_RADIUS):
                x = x - self.WINDOW_X/2
                y = y - self.WINDOW_Y + self.H_0*self.BLOCK_SIZE
                new_y = int(player_y + y//self.BLOCK_SIZE)
                new_x = int(player_x + x//self.BLOCK_SIZE)
                if self.map[new_y][new_x] == type:
                    self.map[new_y][new_x] = 0
                    self.backpack.add(int(self.biome_map[new_y][new_x]))
                    self.water_check(new_y, new_x)
    
    
        
    def main(self):
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.volume/5)
        
        while not self.finished:
            self.player.checking(self.map)
            start_time = time.time()
            self.clock.tick(self.FPS)
            x, y, H, bool = self.player.recalculation(self.map)
            if x >= self.SIZE - self.WINDOW_X/self.BLOCK_SIZE/2:
                x = self.SIZE - self.WINDOW_X/self.BLOCK_SIZE/2 - 1
            if x <= self.WINDOW_X/self.BLOCK_SIZE/2:
                x = self.WINDOW_X/self.BLOCK_SIZE/2 + 1
            self.draw_map(int(x), int(y), int(H))
            
            number, height = self.player.draw()
            self.draw_player(number, height)
            
            inventory, hand, hand_image, height = self.player.player_inventory()
            self.draw_inventory(inventory, hand, hand_image, height)
            
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    coord = event.pos
                    if self.player.doing() == 0:
                        pass
                    else:
                        self.doing(coord[0], coord[1], x, y, self.player.doing(), height)
                        pass
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        if self.inventory_bool:
                            self.inventory_bool = False
                        else:
                            self.inventory_bool = True
                        
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if keys[pygame.K_d]:
                    self.player.jumping_right(True, self.map)
                if keys[pygame.K_a]:
                    self.player.jumping_left(True, self.map)
                self.player.jumping()
            elif keys[pygame.K_d]:
                self.player.moving_right(True)
            elif keys[pygame.K_a]:
                self.player.moving_left(True)
            else:
                self.player.moving_right(False)
                self.player.moving_left(False)
                
            if keys[pygame.K_1]:
                self.player.change_hand(1)
            
            if keys[pygame.K_2]:
                self.player.change_hand(2)
            
            if keys[pygame.K_3]:
                self.player.change_hand(3)
            
            if keys[pygame.K_4]:
                self.player.change_hand(4)
                    
            if keys[pygame.K_5]:
                self.player.change_hand(5)
            
            if keys[pygame.K_6]:
                self.player.change_hand(6)
            
            if keys[pygame.K_7]:
                self.player.change_hand(7)
            
            if keys[pygame.K_8]:
                self.player.change_hand(8)
            
            if keys[pygame.K_9]:
                self.player.change_hand(9)
            
            if keys[pygame.K_0]:
                self.player.change_hand(10)
            
                    
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
        
            pygame.display.update()
            print("FPS: ", 1.0 / (time.time() - start_time))
        
        
        pygame.quit()
