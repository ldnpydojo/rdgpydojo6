import time
import random
import pygame
from pygame import Color
from hcf import HexCoordFactory
from collections import defaultdict

GRASS = 0
SPORE = 1
SHROOM = 2
DEAD = 3


SIZE = 40
YOFF = SIZE * 0.5 * 3 ** 0.5
WHITE = Color('white')
GREEN = Color(0, 128, 0)
RED = Color(200, 0, 0)
BROWN = Color(120, 68, 33)

COLOUR_MAP = {
    GRASS: GREEN,
    SPORE: GREEN,
    SHROOM: RED,
    DEAD: BROWN
}


def grid_to_screen(x, y):
    return int((2 * x + (y % 2)) * SIZE * 0.5 + 0.5) + 30, int(y * YOFF + 0.5) + 30 


class Grid(object):
    def __init__(self, size):
        self.cells = defaultdict(int)
        self.coords = HexCoordFactory(size, size)

    def create_spores(self, num=10):
        for i in xrange(num):
            rn = range(len(self.coords))
            pos = random.choice(rn)
            self.cells[pos] = SPORE

    def create_shrooms(self, num=10):
        for i in xrange(num):
            rn = range(len(self.coords))
            pos = random.choice(rn)
            self.cells[pos] = SHROOM

    def iter_coords(self):
        for v in range(len(self.coords)):
            yield self.coords.cxy(v), self.cells[v]	

    def __iter__(self):
        for v in xrange(len(self.coords)):
            yield self.cells[v]	

    def compute_next_gen(self):
        next = defaultdict(int)
        for i, type in enumerate(self):
            neighbours = self.coords.Ring1(i)
            types = defaultdict(int)
            for n in neighbours:
                types[self.cells[n]] += 1
            ntype = type
            if type == GRASS:
                if types[SHROOM] > 1:
                    ntype = SPORE
            elif type == SPORE:
                if types[SHROOM] > 2:
                    ntype = GRASS
                else:
                    ntype = SHROOM
            elif type == SHROOM:
                if not random.randint(0, 2):
                    ntype = DEAD
            elif type == DEAD:
                ntype = GRASS
                
            next[i] = ntype

        self.cells = next

    def draw(self, screen):
        for (x, y), type in self.iter_coords():
            sx, sy = grid_to_screen(x, y)
            try:
                col = COLOUR_MAP[type]
            except KeyError:
                col = WHITE
            pygame.draw.circle(screen, col, (sx, sy), 15)
    

def main():
    pygame.init()
    try:
        screen = pygame.display.set_mode((900, 800) )
        grid = Grid(20)
        grid.create_spores()
        grid.create_shrooms()
        while True:
            grid.draw(screen)
            pygame.display.flip()
            grid.compute_next_gen()
            time.sleep(1)
    finally:
        pygame.quit()
        pass


if __name__ == '__main__':
    main()
