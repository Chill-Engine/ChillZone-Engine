import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
pygame.mixer.init()  

def playsound(filename):
    sound1 = pygame.mixer.Sound(f'{os.getcwd()}\\data\\audio\\{filename}')
    sound1.play()


