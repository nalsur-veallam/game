import random
import numpy as np


def generate_map(seed, size, h_max, sharp, depth, probability):
    k = probability
    random.seed(seed)
    border = []
    border.append(0)
    border.append(0)
    for i in range(2, size):     #Высчитываем горизонт
        if border[i-1] == border[i-2]:
            coef = 0.8
        else:
            coef = 0.5
        H = random.random()
        if H < coef:
            h = border[i-1]
        else:
            h = random.randint(border[i-1] - sharp, border[i-1] + sharp)
        if h > h_max:
            border.append(h_max)
        elif h < -1*h_max:
            border.append(-1*h_max)
        else:
            border.append(h)

    map = np.zeros((depth,size))
    
    for i in range(0, depth):    #Заполняем левый край землей
        if h_max + 1 - border[0] == i:
            for j in range(i, depth):
                map[j][0] = 1
            break
                
    for i in range(0, depth):    #Заполняем правый край землей
        if h_max + 1 - border[size - 1] == i:
            for j in range(i, depth):
                map[j][size - 1] = 1
            break
    
    for i in range(1, depth):    #Заполняем карту землей и камнем
        for j in range(1, size - 1):
            if map[i-1][j] == 0 and h_max + 1 - border[j] != i:
                map[i][j] = 0
            elif h_max + 1 - border[j] == i:
                map[i][j] = 1
            else:
                prob = random.random()
                summ = map[i-1][j] + map[i-1][j-1] + map[i-1][j+1] + map[i][j-1]
                if prob <= k*(i - h_max + border[i])/depth + summ/100:
                    map[i][j] = 2
                else:
                    map[i][j] = 1
    
   
    return map
