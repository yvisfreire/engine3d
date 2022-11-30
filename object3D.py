import pygame as pg
import numpy as np
import math

class Object3D:
    def __init__(self, render) -> None:
        self.render = render
        #self.vertices = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1),
        #                          (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)])
        self.vertices = np.array([(1, -1, -1, 1), (1, -1, 1, 1), (1, 1, 1, 1), (1, 1, -1, 1),
                                  (-1, -1, -1, 1), (-1, -1, 1, 1), (-1, 1, 1, 1), (-1, 1, -1, 1)])
        self.position = self.vertices
        self.pos = (100, 100, 100)
        self.faces = np.array([(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (3, 2, 6, 7)])
        self.angle = math.pi / self.render.FPS
        self.scale(50)

    def draw(self):
        position = self.position @ self.render.camera.camera_matrix()
        position = position @ self.render.camera.projection_matrix()
        position /= position[:, -1].reshape(-1, 1)
        position = position @ self.render.camera.to_screen_matrix()
        vertices = position[:, :2]
        for face in self.faces:
            points = [vertices[j] for j in face]
            pg.draw.polygon(self.render.screen, (255, 0, 0), points, 3)

        self.rotate_z(self.angle)
        self.rotate_y(self.angle)
        self.rotate_x(self.angle)
        self.translate(self.pos)
        self.move((0, 0, 0))

    def move(self, pos):
      self.pos = tuple(map(sum, zip(self.pos, pos)))

    def translate(self, pos):
        tx, ty, tz = pos
        translation_m = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [tx, ty, tz, 1]])
        self.position = self.vertices @ translation_m

    def scale(self, value):
        scale_m = np.array([[value, 0, 0, 0],
                            [0, value, 0, 0],
                            [0, 0, value, 0],
                            [0, 0, 0, 1]])
        self.vertices = self.vertices @ scale_m

    def rotate_x(self, a):
        rotation_m = np.array([[1, 0, 0, 0],
                             [0, math.cos(a), math.sin(a), 0],
                             [0, -math.sin(a), math.cos(a), 0],
                             [0, 0, 0, 1]])
        self.vertices = self.vertices @ rotation_m

    def rotate_y(self, a):
        rotation_m = np.array([[math.cos(a), 0, -math.sin(a), 0],
                             [0, 1, 0, 0],
                             [math.sin(a), 0, math.cos(a), 0],
                             [0, 0, 0, 1]])
        self.vertices = self.vertices @ rotation_m

    def rotate_z(self, a):
        rotation_m = np.array([[math.cos(a), -math.sin(a), 0, 0],
                             [math.sin(a), math.cos(a), 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]])
        self.vertices = self.vertices @ rotation_m