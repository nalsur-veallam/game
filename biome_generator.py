import random
import numpy as np

#Создаем биомы, жидкость - (-1)
#
#х3 - снежный биом
#
#
#
#



def water_generator(seed, size, biome_map, lakes_number):
    random.seed(seed)
    for i in range(0, lakes_number):
        n = random.randint(0, size)
        k = 0
        h = 0
        while k == 0:
            k = biome_map[h + 1][n]
            h += 1
        h -= 1
        k = 0
        while k == 0 and n + 1 < size:
            k = biome_map[h][n + 1]
            n += 1
        n_2 = n 
        k = 0
        while k == 0 and n - 1 > 0:
            k = biome_map[h][n-1]
            n -= 1
        n_1 = n + 1
        H = h
        for j in range(n_1, n_2):
            h = H
            biome_map[h][j] = -1
            while biome_map[h][j] != 1:
                biome_map[h][j] = -1
                h += 1
    return biome_map

max_snow = 20
min_snow = 4



def snow_generator(seed, size, biome_map, snow_size, map):
    random.seed(seed)
    n = random.randint(0, size)
    if n - snow_size > 0:
        max_0 = random.randint(min_snow, max_snow/2)
        for i in range(0, int(snow_size/2)):
            max = random.randint(-2, 2)
            max_0 = max
            if max_0 > max_snow or max_0 < min_snow:
                max_0 = random.randint(max_snow/2, max_snow)
            k = 0
            j = 0
            while k < max_0:
                if biome_map[j][n + i] != 0:
                    if biome_map[j][n + i] < 0:
                        biome_map[j][n + i] = 2*10
                        map[j][n+i] = 2
                    else:
                        biome_map[j][n + i] = biome_map[j][n + i] * 10
                    k += 1
                else:
                    pass
                j += 1
    return biome_map, map
                    



def biome_generator(seed, depth, size, map, lakes_number):
    biome_map = np.zeros((depth,size))
    for i in range(0, depth):
        for j in range(0, size):
            if map[i][j] != 0:
                biome_map[i][j] = map[i][j]
    
    
    biome_map = water_generator(seed, size, biome_map, lakes_number)
        
    snow_size = size/5
    biome_map, map = snow_generator(seed, size, biome_map, snow_size, map)
    
    for i in range(0, size):
        bool = True
        for j in range(0, depth):
            if biome_map[j][i] == -1:
                bool = False
            if biome_map[j][i] == 1 and bool:
                biome_map[j][i] = 0.5
                bool = False 
    
    return biome_map, map
                
                
