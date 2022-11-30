from object3D import *
from camera import *

import pygame as pg
import numpy as np
import math

class Render:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.WIDTH = 800
        self.HEIGHT = 600
        self.RES = self.WIDTH, self.HEIGHT
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES, pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.clock.tick(self.FPS)
        self.cube = Object3D(self)
        self.camera = Camera(self, [0, 0, 0])

    def draw(self):
        self.screen.fill(pg.Color('darkslategray'))
        self.cube.draw()

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    app = Render()
    app.run()