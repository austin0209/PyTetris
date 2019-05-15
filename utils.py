import objects
import pygame
import random
import main
from main import block_size
from main import screen

def fill_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            grid[y][x] = objects.Block(x * block_size, y * block_size,
                                      (0, 0, 0), (0, 0, 0))

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            grid[y][x].draw(surface)

def check_lost(grid, pieces):
    # check if lost
    lose = False
    for piece in pieces:
        if piece.find_top() < 0:
            lose = True
    if lose:
        for i in reversed(range(len(pieces))):
            del pieces[i]
    return lose

def update_grid(grid, pieces):
    # check if row is filled
    num_filled = 0
    for row in range(len(grid)):
        for block in grid[row]:
            block.occupied = False
            for piece in pieces:
                for other_block in piece.blocks:
                    if (block.rect.x == other_block.rect.x and
                            block.rect.y == other_block.rect.y):
                        block.occupied = True
        filled = True
        for block in grid[row]:
            if not block.occupied:
                filled = False
        if (filled):
            num_filled += 1
            for piece in pieces:
                #piece.blocks = [block for block in piece.blocks if not block.rect.x == row * block_size]
                for i in reversed(range(0, len(piece.blocks))):
                    if piece.blocks[i].rect.top == row * block_size:
                        del piece.blocks[i]
                    elif piece.blocks[i].rect.top < row * block_size:
                        piece.blocks[i].drop()
    return num_filled

def can_move(target, pieces, direction):
    if direction == "LEFT":
        result = target.find_left() > 0
    else:
        result = target.find_right() < screen.get_size()[0]
    for block in target.blocks:
        for other_piece in pieces:
            if not other_piece is target:
                for other_block in other_piece.blocks:
                    if (block.rect.right + block_size > other_block.rect.left
                            and block.rect.left - block_size < other_block.rect.right
                            and block.rect.bottom == other_block.rect.bottom):
                        result = False
    return result

def input(event, target, pieces):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            if can_move(target, pieces, "LEFT"):
                target.move(-block_size, pieces)
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            if can_move(target, pieces, "RIGHT"):
                target.move(block_size, pieces)
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            target.rotate(pieces)
