from random import randint
import pygame
 
class Player:
    def __init__(self, pos_x, H_0, depth):
        #Состояние организма
        self.health = 30
        self.hunger = 20
        self.fatigue = 50
        self.thirst = 20
        self.frostbite = 10
        self.disease = 0
        self.stage_of_disease = 0        
        
        #Координати игрока
        self.pos_y = 0
        self.pos_x = pos_x
        
        #Размеры игрока
        self.height = 100
        self.widht = 35
        
        #Движение
        self.speed = 1
        self.jump_speed = 6
        self.acceleration = 3*self.jump_speed/20
        self.speed_of_jump = self.jump_speed
        self.move_right = False
        self.move_left = False
        self.jump = False
        self.right = True
        self.move_right_time = 0
        self.move_left_time = 0
        
        #Вспомогательные переменные
        self.masturbation = 10
        self.sleep = 100/8
        self.hand = 1
        self.time = 0
        self.H_0 = H_0
        self.H = 0
        self.plate = []
        self.inventory = [1, 2, 0, 0, 0, 0, 0, 0, 0, 0]
        self.hand_image = 1
        self.block_size = 20
        self.new_y = self.pos_y
        self.depth = depth
        
        
    def jumping(self):
        if self.jump == False:
            self.jump = True
            self.new_y = self.pos_y
        else:
           pass
                
            
    def moving_right(self, bool):
        if not self.move_right and bool:
            self.move_right = True
            self.right = True
            self.move_left = False
            self.move_right_time = 0
        elif not bool:
            self.move_right = False
            self.hand_image = 1
        else:
            pass
        
        
    def moving_left(self, bool):
        if not self.move_left and bool:
            self.move_left = True
            self.right = False
            self.move_right = False
            self.move_left_time = 0
        elif not bool:
            self.move_left = False
            self.hand_image = 4
        else:
            pass
        
        
    def y_calculation(self, map, h_max): # Функция, высчитывающая  начальное положение игрока
        for i in range(1, self.depth):
            self.plate = []
            if map[i][int(self.pos_x)] != 0:
                self.plate.append(i)
                break
        for i in range(1, self.depth):
            if map[i][int(self.pos_x) + 1] != 0:
                self.plate.append(i)
                break
        self.pos_y = min(self.plate)
        
     
   
               
    def jumping_right(self, bool, map):
        if bool:
            if map[self.pos_y - int(self.H + 1)][int(self.pos_x + 2)] <= 0 and map[self.pos_y - int(self.H + 2)][int(self.pos_x + 2)] <= 0 and map[self.pos_y - int(self.H + 3)][int(self.pos_x + 2)] <= 0 and map[self.pos_y - int(self.H + 4)][int(self.pos_x + 2)] <= 0 and map[self.pos_y - int(self.H + 5)][int(self.pos_x + 2)] <= 0:
                self.pos_x += self.speed
            else:
                pass
        else:
            pass
    
               
    def jumping_left(self, bool, map):
        if bool:
            if map[self.pos_y - int(self.H + 1)][int(self.pos_x - 1)] <= 0 and map[self.pos_y - int(self.H + 2)][int(self.pos_x - 1)] <= 0 and map[self.pos_y - int(self.H + 3)][int(self.pos_x - 1)] <= 0 and map[self.pos_y - int(self.H + 4)][int(self.pos_x - 1)] <= 0 and map[self.pos_y - int(self.H + 5)][int(self.pos_x - 1)] <= 0:
                self.pos_x -= self.speed
            else:
                pass
        else:
            pass
            
        
    def recalculation(self, map):
        if self.move_left and not self.jump:
            
            if map[self.pos_y - 1][int(self.pos_x) - 1] != 0:
                if map[self.pos_y - 2][int(self.pos_x) - 1] != 0:
                    self.move_left = False
                elif map[self.pos_y - 3][int(self.pos_x) - 1] != 0:
                    self.move_left = False
                elif map[self.pos_y - 4][int(self.pos_x) - 1] != 0:
                    self.move_left = False
                elif map[self.pos_y - 5][int(self.pos_x) - 1] != 0:
                    self.move_left = False
                elif map[self.pos_y - 6][int(self.pos_x) - 1] != 0:
                    self.move_left = False
                elif map[self.pos_y - 6][int(self.pos_x)] != 0:
                    self.move_left = False
                elif map[self.pos_y - 6][int(self.pos_x) + 1] != 0:
                    self.move_left = False
                else:
                    self.plate[1] = self.plate[0]
                    self.plate[0] = self.pos_y - 1
                    self.pos_y = min(self.plate)
                    self.pos_x -= self.speed
                    
            else:
                if map[self.pos_y - 1][int(self.pos_x) - 1] != 0:
                    self.move_left = False
                elif map[self.pos_y - 2][int(self.pos_x) - 1] != 0:
                    self.move_left = False
                elif map[self.pos_y - 3][int(self.pos_x) - 1] != 0:
                    self.move_left = False
                elif map[self.pos_y - 4][int(self.pos_x) - 1] != 0:
                    self.move_left = False
                elif map[self.pos_y - 5][int(self.pos_x) - 1] != 0:
                    self.move_left = False
                else:
                    self.plate[1] = self.plate[0]
                    i = self.pos_y - 1
                    while map[i][int(self.pos_x) - 1] == 0:
                        i += 1
                    self.plate[0] = i
                    self.pos_x -= self.speed
                    self.pos_y = min(self.plate)
            
            self.move_left_time += 1 
            if self.move_left_time == 6:
                self.move_left = False
                self.hand_image = 4
            
        if self.move_right and not self.jump:
            
            if map[self.pos_y - 1][int(self.pos_x) + 2] != 0:
                if map[self.pos_y - 2][int(self.pos_x) + 2] != 0:
                    self.move_right = False
                elif map[self.pos_y - 3][int(self.pos_x) + 2] != 0:
                    self.move_right = False
                elif map[self.pos_y - 4][int(self.pos_x) + 2] != 0:
                    self.move_right = False
                elif map[self.pos_y - 5][int(self.pos_x) + 2] != 0:
                    self.move_right = False
                elif map[self.pos_y - 6][int(self.pos_x) + 2] != 0:
                    self.move_right = False
                elif map[self.pos_y - 6][int(self.pos_x) + 1] != 0:
                    self.move_right = False
                elif map[self.pos_y - 6][int(self.pos_x)] != 0:
                    self.move_right = False
                else:
                    self.plate[0] = self.plate[1]
                    self.plate[1] = self.pos_y - 1
                    self.pos_x += self.speed
                    self.pos_y = min(self.plate)
                    
            else:
                if map[self.pos_y - 1][int(self.pos_x) + 2] != 0:
                    self.move_right = False
                elif map[self.pos_y - 2][int(self.pos_x) + 2] != 0:
                    self.move_right = False
                elif map[self.pos_y - 3][int(self.pos_x) + 2] != 0:
                    self.move_right = False
                elif map[self.pos_y - 4][int(self.pos_x) + 2] != 0:
                    self.move_right = False
                elif map[self.pos_y - 5][int(self.pos_x) + 2] != 0:
                    self.move_right = False
                else:
                    self.plate[0] = self.plate[1]
                    i = self.pos_y - 1
                    while map[i][int(self.pos_x) + 2] == 0:
                        i += 1
                    self.plate[1] = i
                    self.pos_y = min(self.plate)
                    self.pos_x += self.speed
            
            self.move_right_time += 1
            if self.move_right_time == 6:
                self.move_right = False
                self.hand_image = 1
            
        if self.jump:
            self.speed_of_jump -= self.acceleration
            if (map[int(self.new_y - 6)][int(self.pos_x)] == 0 and map[int(self.new_y - 6)][int(self.pos_x) + 1] == 0) or (int(self.new_y - 6) <= 0):
                pass
            else:
                self.speed_of_jump = -1*abs(self.speed_of_jump)
            self.speed_of_jump -= self.acceleration
            self.H += self.speed_of_jump
            self.new_y -= self.speed_of_jump
        
        if (map[self.pos_y - int(self.H)][int(self.pos_x)] > 0 or map[self.pos_y - int(self.H)][int(self.pos_x) + 1] > 0) and self.speed_of_jump < 0:
            self.pos_y = self.pos_y - int(self.H)
            self.jump = False
            self.speed_of_jump = self.jump_speed
            self.H = 0
            if map[self.pos_y - 1][int(self.pos_x)] > 0 or map[self.pos_y - 1][int(self.pos_x) + 1] > 0:
                while map[self.pos_y - 1][int(self.pos_x)] > 0 or map[self.pos_y - 1][int(self.pos_x) + 1] > 0:
                    self.pos_y -= 1
            elif map[self.pos_y][int(self.pos_x)] <= 0 and map[self.pos_y][int(self.pos_x) + 1] <= 0:
                while map[self.pos_y][int(self.pos_x)] <= 0 and map[self.pos_y][int(self.pos_x) + 1] <= 0:
                    self.pos_y += 1
            else:
                pass
            return self.pos_x, self.pos_y, self.H, True
        else:
            pass
        
        return self.pos_x, self.pos_y, self.H, False 
        
        
    def draw(self):
        if self.jump:
            if self.right:
                self.hand_image = 1
                return 0, self.height 
            else:
                self.hand_image = 4
                return 3, self.height
        elif self.move_right:
            if self.move_right_time < 3:
                self.hand_image = 2
                return 1, self.height
            elif self.move_right_time < 5:
                self.hand_image = 3
                return 2, self.height
            else:
                return 0, self.height
        elif self.move_left:
            if self.move_left_time < 3:
                self.hand_image = 5
                return 4, self.height
            elif self.move_left_time < 5:
                self.hand_image = 6
                return 5, self.height
            else:
                self.hand_image = 4
                return 3, self.height
        else:
            if self.right:
                self.hand_image = 1
                return 0, self.height 
            else:
                self.hand_image = 4
                return 3, self.height
            
    
    def player_inventory(self):
        return self.inventory, self.hand, self.hand_image, self.height
    
    
    def doing(self):
        if self.inventory[self.hand - 1] == 1:
            return 1
        elif self.inventory[self.hand - 1] == 2:
            return 2
        else:
            return 0
    
    
    def checking(self, map):
        if map[self.pos_y - 1][int(self.pos_x)] > 0 or map[self.pos_y - 1][int(self.pos_x) + 1] > 0:
            while map[self.pos_y - 1][int(self.pos_x)] > 0 or map[self.pos_y - 1][int(self.pos_x) + 1] > 0:
                self.pos_y -= 1
        elif map[self.pos_y][int(self.pos_x)] <= 0 and map[self.pos_y][int(self.pos_x) + 1] <= 0:
            while map[self.pos_y][int(self.pos_x)] <= 0 and map[self.pos_y][int(self.pos_x) + 1] <= 0:
                    self.pos_y += 1
        else:
            pass
        
    
    def change_hand(self, number):
        self.hand = number
    
    
    
class Backpack:
    def __init__(self):
        self.size = 100
        self.sizes = [1, 1]
        self.backpack_size = 4*6
        self.slots = []
        for i in range(0, self.backpack_size):
            self.slots.append(0)
        self.count = []
        for i in range(0, self.backpack_size):
            self.count.append(0)
            
    def add(self, type):
        if self.size - self.sizes[type - 1] < 0:
            return 0
        else:
            for i in range(0, self.backpack_size):
                if self.slots[i] == type:
                    self.count[i] += 1
                    self.size -= self.sizes[type - 1]
                    return 0
            for i in range(0, self.backpack_size):
                if self.slots[i] == 0:
                    self.slots[i] = type
                    self.count[i] += 1
                    self.size -= self.sizes[type - 1]
                    return 0
                    
    def show(self):
        return self.slots, self.count, self.backpack_size
                
    
    
    
    
    
    
    

