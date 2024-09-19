import pygame
from pygame.locals import *
import math
from math import atan2

pygame.init()

FPS = 60
TS = 16  # tile size
SIZE = 32 * TS  # unscaled window size (map size * tile size)
SCALE = 2  # window scale factor
LW = 2  # line width
RANGE = 50  # trace to n tiles away

start_position = ((SIZE//2), (SIZE//2))  # click mouse to set a new position

# colors
RED, GREEN, BLUE, YELLOW, PURPLE = (201, 48, 56), (48, 156, 99), (65, 114, 145), (255, 229, 150), (130, 100, 129)
WALL_A, WALL_B, FLOOR_A, FLOOR_B = (31, 24, 51), (43, 46, 66), (144, 161, 168), (182, 203, 207)

screen = pygame.Surface((SIZE, SIZE))
scaled_screen = pygame.display.set_mode((SIZE * SCALE, SIZE * SCALE))
clock = pygame.time.Clock()

tilemap = [  # 1 is wall tile, 0 is floor tile
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1),
    (1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1),
    (1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1),
    (1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1),
    (1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1),
    (1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1),
    (1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
    (1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
    (1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
    (1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1),
    (1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1),
    (1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1),
    (1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1),
    (1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1),
    (1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1),
    (1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1),
    (1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1),
    (1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1),
    (1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)]

# generate wall coordinates as strings
wall_tiles = []
for y in range(len(tilemap)):
    for x in range(len(tilemap[y])):
        tile = tilemap[y][x]
        if tile == 1:
            wall_tiles.append(str(int(x)) + ';' + str(int(y)))

# generate tile graphics
tile_graphics = screen.copy()
for y in range(len(tilemap)):
    for x in range(len(tilemap[y])):
        tile = tilemap[y][x]
        if tile == 1:
            pygame.draw.rect(tile_graphics, WALL_A, (x * TS, y * TS, TS, TS), 0)
            pygame.draw.rect(tile_graphics, WALL_B, (x * TS, y * TS, TS, TS), LW)
        else:
            pygame.draw.rect(tile_graphics, FLOOR_A, (x * TS, y * TS, TS, TS), 0)
            pygame.draw.rect(tile_graphics, FLOOR_B, (x * TS, y * TS, TS, TS), LW)

def _raycast(sx, sy, mx, my):
    angle = atan2(my - sy, mx - sx)
    rx = math.cos(angle)
    ry = math.sin(angle)
    map_x = sx // TS
    map_y = sy // TS
    pygame.draw.rect(screen, RED, (map_x * TS, map_y * TS, TS, TS), LW)

    t_max_x = sx / TS - map_x
    if rx > 0:
        t_max_x = 1 - t_max_x
    t_max_y = sy / TS - map_y
    if ry > 0:
        t_max_y = 1 - t_max_y

    hit_wall = False
    side = 0

    for i in range(RANGE):
        if ry == 0 or t_max_x < t_max_y * abs(rx / ry):
            side = 0
            map_x += 1 if rx > 0 else -1
            t_max_x += 1
            # draw floor rect for moving x ('x' -> 0)
            pygame.draw.rect(screen, GREEN, (map_x * TS, map_y * TS, TS, TS), LW)

        else:
            side = 1
            map_y += 1 if ry > 0 else -1
            t_max_y += 1
            # draw floor rect for moving y ('y' -> 1)
            pygame.draw.rect(screen, BLUE, (map_x * TS, map_y * TS, TS, TS), LW)

        # check if tile is a wall
        loc_str = str(int(map_x)) + ';' + str(int(map_y))
        if loc_str in wall_tiles:
            pygame.draw.rect(screen, RED, (map_x * TS, map_y * TS, TS, TS), LW)
            hit_wall = True
            break

    if side == 0:
        x = (map_x + (1 if rx < 0 else 0)) * TS
        y = sy + (x - sx) * ry / rx

    else:
        y = (map_y + (1 if ry < 0 else 0)) * TS
        x = sx + (y - sy) * rx / ry

    if hit_wall:
        pygame.draw.rect(screen, YELLOW, (x - LW, y - LW, 1 + (2 * LW), 1 + (2 * LW)), LW)
    return (x, y)

while True:
    mx, my = pygame.mouse.get_pos()
    mx = int(mx // SCALE)
    my = int(my // SCALE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                start_position = (int(mx), int(my))

    screen.blit(tile_graphics, (0, 0))
    pygame.draw.line(screen, PURPLE, start_position, (mx, my), LW)
    intersection = _raycast(start_position[0], start_position[1], mx, my)
    #print(intersection)
    scaled_screen.blit(pygame.transform.scale(screen, (SIZE * SCALE, SIZE * SCALE)), (0, 0))
    pygame.display.update()
    clock.tick(FPS)
