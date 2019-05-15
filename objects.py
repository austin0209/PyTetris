import pygame
from main import block_size
from main import screen

class Block:

    def __init__(self, x, y, color, outline_color=None):
        self.rect = pygame.rect.Rect(x, y, block_size, block_size)
        self.outline = pygame.rect.Rect(x, y, block_size, block_size)
        self.occupied = False
        if outline_color is None:
            self.color = color
            self.outline_color = (0, 0, 0)
        else:
            self.color = color
            self.outline_color = outline_color

    def drop(self):
        self.rect.y += block_size
        self.outline.y += block_size

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.outline.x = x
        self.outline.y = y

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, self.outline_color, self.outline, 1)

class Piece:

    def __init__(self, id):
        self.has_settled = False
        if id == 0: # creates square
            color = (255, 255, 0)
            self.blocks = [Block(4 * block_size, -block_size, color),
                           Block(4 * block_size, -block_size * 2, color),
                           Block(5 * block_size, -block_size, color),
                           Block(5 * block_size, -block_size * 2, color)]
        elif id == 1: # create line
            color = (0, 255, 255)
            self.blocks = [Block(4 * block_size, -block_size * 4, color),
                          Block(4 * block_size, -block_size * 3, color),
                          Block(4 * block_size, -block_size * 2, color),
                          Block(4 * block_size, -block_size, color)]
        elif id == 2: # create z
            color = (255, 0, 0)
            self.blocks = [Block(4 * block_size, -block_size * 2, color),
                          Block(5 * block_size, -block_size * 2, color),
                          Block(5 * block_size, -block_size, color),
                          Block(6 * block_size, -block_size, color)]
        elif id == 3: # create upside down L
            color = (255, 128, 0)
            self.blocks = [Block(4 * block_size, -block_size * 3, color),
                          Block(5 * block_size, -block_size * 3, color),
                          Block(5 * block_size, -block_size * 2, color),
                          Block(5 * block_size, -block_size, color)]
        elif id == 4: # create upside down T
            color = (255, 0, 255)
            self.blocks = [Block(4 * block_size, -block_size, color),
                          Block(5 * block_size, -block_size, color),
                          Block(5 * block_size, -block_size * 2, color),
                          Block(6 * block_size, -block_size, color)]
        elif id == 5: # create sideways J
            color = (0, 0, 255)
            self.blocks = [Block(4 * block_size, -block_size, color),
                          Block(4 * block_size, -block_size * 2, color),
                          Block(5 * block_size, -block_size, color),
                          Block(6 * block_size, -block_size, color)]
        elif id == 6: # create s
            color = (0, 255, 0)
            self.blocks = [Block(4 * block_size, -block_size, color),
                          Block(5 * block_size, -block_size, color),
                          Block(5 * block_size, -block_size * 2, color),
                          Block(6 * block_size, -block_size * 2, color)]

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)

    def find_top(self):
        min = 10000
        for block in self.blocks:
            if (block.rect.top < min):
                min = block.rect.top
        return min

    def find_bottom(self):
        max = -10000
        for block in self.blocks:
            if (block.rect.bottom > max):
                max = block.rect.bottom
        return max

    def find_right(self):
        max = -10000
        for block in self.blocks:
            if (block.rect.right > max):
                max = block.rect.right
        return max

    def find_left(self):
        min = 10000
        for block in self.blocks:
            if (block.rect.left < min):
                min = block.rect.left
        return min

    def move(self, amount, pieces):
        for block in self.blocks:
            block.rect.x += amount
            block.outline.x += amount

    def find_floor(self, pieces):
        min = screen.get_size()[1]
        for piece in pieces:
            if not piece is self:
                for block in piece.blocks:
                    if (block.rect.left >= self.find_left() and
                            block.rect.right <= self.find_right()):
                        if min > block.rect.top:
                            min = block.rect.top
        return min

    def rotate(self, pieces):
        root_point = (self.find_left(), self.find_top())
        reference_point = (self.find_bottom(), self.find_left())
        for block in self.blocks:
            x_offset = abs(block.rect.bottom - reference_point[0])
            y_offset = abs(block.rect.left - reference_point[1])
            block.set_position(root_point[0] + x_offset, root_point[1] + y_offset)
        # correct after rotation:
        while self.find_left() < 0:
            for block in self.blocks:
                 block.set_position(block.rect.x + block_size, block.rect.y)
        while self.find_right() > screen.get_size()[0]:
            for block in self.blocks:
                 block.set_position(block.rect.x - block_size, block.rect.y)
        while self.find_bottom() > self.find_floor(pieces):
            for block in self.blocks:
                 block.set_position(block.rect.x, block.rect.y - block_size)

    def fall(self, pieces):
        can_fall = self.find_bottom() < screen.get_size()[1]
        for block in self.blocks:
            for other_piece in pieces:
                if not other_piece is self:
                    for other_block in other_piece.blocks:
                        if (block.rect.bottom == other_block.rect.top
                        and block.rect.left == other_block.rect.left
                        and block.rect.right == other_block.rect.right):
                            can_fall = False
        if can_fall:
            for block in self.blocks:
                block.rect.y += block_size
                block.outline.y += block_size
        else: self.has_settled = True
