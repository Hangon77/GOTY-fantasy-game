import pygame
from sys import exit

#game variables 
GAME_WIDTH = 512
GAME_HEIGHT = 512

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("GOTY - ADAM'S GAME OF THE YEAR")
clock = pygame.time.Clock() #frame rate 

player = pygame.Rect(150, 150, 50, 50)

def draw():
    window.fill("#1f7a24")
    pygame.draw.rect(window, "#0920e8", player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    draw()
    pygame.display.update()
    clock.tick(60) #60 frames per second
