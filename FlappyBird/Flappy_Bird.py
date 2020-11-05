import pygame
import random
import numpy as np
import sys
print("Running")
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird')
screen = pygame.display.set_mode((432, 768))
default_font = pygame.font.SysFont('04b19',40)
#Game Variables
Speed = 10
flight = 20
gravity = 3
bird_movement = 0
Score = 0
high_score = 0
Pipe_Gap = 120
pygame.font.init()
label = default_font.render("Score: " + str(Score), 1, (255, 255, 255))
screen.blit(label, (10,10))
bg_surface = pygame.image.load("bg.png").convert() #runs game at more consistent speed
bg_surface = pygame.transform.scale(bg_surface,(432, 768))
floor = pygame.image.load("base.png").convert()
floor = pygame.transform.scale(floor,(504,168))
floor_position = 0
#Pipes
Pipe_Down_Position = [random.randint(150,500),random.randint(100,600),random.randint(100,600)]
pipe_position = 500
pipe = pygame.image.load("pipe.png").convert()
pipe = pygame.transform.scale(pipe,(78,480))
pipe_top = pygame.transform.flip(pipe,False,True)
pipe_top = pygame.transform.scale(pipe_top,(78,480))
pipe_rect = pipe.get_rect(midtop = (pipe_position,Pipe_Down_Position[0]))
pipe_rect1 = pipe.get_rect(midtop = (pipe_position+300,Pipe_Down_Position[1]))
pipe_rect2 = pipe.get_rect(midtop = (pipe_position+600,Pipe_Down_Position[2]))
pipe_top_rect = pipe_top.get_rect(midbottom = (pipe_position,Pipe_Down_Position[0]-Pipe_Gap))
pipe_top_rect1 = pipe_top.get_rect(midbottom = (pipe_position+300,Pipe_Down_Position[1]-Pipe_Gap))
pipe_top_rect2 = pipe_top.get_rect(midbottom = (pipe_position+600,Pipe_Down_Position[2]-Pipe_Gap))
pipes = [[pipe_rect,pipe_top_rect],[pipe_rect1,pipe_top_rect1],[pipe_rect2,pipe_top_rect2]]
#Bird
bird_downflap = pygame.image.load("bird1.png").convert_alpha()
bird_downflap = pygame.transform.scale(bird_downflap,(51,36))
bird_midflap = pygame.image.load("bird2.png").convert_alpha()
bird_midflap = pygame.transform.scale(bird_midflap,(51,36))
bird_upflap = pygame.image.load("bird3.png").convert_alpha()
bird_upflap = pygame.transform.scale(bird_upflap,(51,36))
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird = bird_frames[bird_index]
bird_rect = bird.get_rect(center = (100,384))

def draw_floor():
    screen.blit(floor,(floor_position,600))
    screen.blit(floor,(floor_position+432,600))

def draw_pipes(pipes):
    if len(pipes):
        screen.blit(pipe_top,pipes[0][1])
        screen.blit(pipe,pipes[0][0])
        screen.blit(pipe_top,pipes[1][1])
        screen.blit(pipe,pipes[1][0])
        screen.blit(pipe_top,pipes[2][1])
        screen.blit(pipe,pipes[2][0])
    else:
        return False

def move_pipes(Pipes):
    for a in Pipes:
        for Pipe in a:
            Pipe.centerx -=Speed
    return Pipes

def Collision_Check(Pipes):
    for A in Pipes:
        for B in A:
            if bird_rect.colliderect(B): # Inbuilt from Pygame
                return True
    if bird_rect.top <= -10 or bird_rect.bottom >=610:
        return True
    else:
        return False
def Rotate_Bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement,1)
    return new_bird

def High_Score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement = -flight
            if event.key == pygame.K_SPACE and Collision_Check(pipes) == True:
                bird_rect.centerx, bird_rect.centery = 100,384
                Score, flight, gravity = 0, 20, 3
                Pipe_Down_Position = [random.randint(150, 500), random.randint(100, 600), random.randint(100, 600)]
                pipe_rect = pipe.get_rect(midtop=(pipe_position, Pipe_Down_Position[0]))
                pipe_rect1 = pipe.get_rect(midtop=(pipe_position + 300, Pipe_Down_Position[1]))
                pipe_rect2 = pipe.get_rect(midtop=(pipe_position + 600, Pipe_Down_Position[2]))
                pipe_top_rect = pipe_top.get_rect(midbottom=(pipe_position, Pipe_Down_Position[0] - Pipe_Gap))
                pipe_top_rect1 = pipe_top.get_rect(midbottom=(pipe_position + 300, Pipe_Down_Position[1] - Pipe_Gap))
                pipe_top_rect2 = pipe_top.get_rect(midbottom=(pipe_position + 600, Pipe_Down_Position[2] - Pipe_Gap))
                pipes = [[pipe_rect, pipe_top_rect], [pipe_rect1, pipe_top_rect1], [pipe_rect2, pipe_top_rect2]]
    screen.blit(bg_surface,(0,0))
    bird_index = (bird_index + 1)%3
    bird = bird_frames[bird_index]
    bird_movement += gravity
    rotated_bird = Rotate_Bird(bird)
    bird_rect.centery += bird_movement
    screen.blit(rotated_bird,bird_rect)
    draw_pipes(pipes)
    move_pipes(pipes)
    if pipe_top_rect.centerx <= -100:
        pipe_top_rect = pipe_top_rect1
        pipe_top_rect1 = pipe_top_rect2
        pipe_rect = pipe_rect1
        pipe_rect1 = pipe_rect2
        Pipe_Down_Position.pop(0)
        Pipe_Down_Position.append(random.randint(150, 500))
        pipe_top_rect2 = pipe_top.get_rect(midbottom = (pipe_position+300,Pipe_Down_Position[2]-Pipe_Gap))
        pipe_rect2 = pipe.get_rect(midtop = (pipe_position+300,Pipe_Down_Position[2]))
        pipes.pop(0)
        pipes.append([pipe_rect2,pipe_top_rect2])
    if Collision_Check(pipes) == False and pipe_top_rect.centerx == 100:
        Score += 1
    pygame.font.init()
    label = default_font.render("Score: " + str(Score), 1, (255, 255, 255))
    screen.blit(label, (10,10))
    draw_floor()
    floor_position -= Speed
    if floor_position <= -432:
        floor_position = 0
    if Collision_Check(pipes) == True:
        high_score = High_Score(Score,high_score)
        bird_rect.centerx, bird_rect.centery = 0, 800
        gravity, flight = 0, 0
        pipes = []
        screen.blit(bg_surface, (0, 0))
        draw_floor()
        label = default_font.render("High Score: " + str(high_score), 1, (255, 255, 255))
        screen.blit(label, (100, 300))
        highscore_font = pygame.font.SysFont('04b19', 80)
        label = highscore_font.render("Score: " + str(Score), 1, (255, 255, 255))
        screen.blit(label, (50, 210))
    pygame.display.update()