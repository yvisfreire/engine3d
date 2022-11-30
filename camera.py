import pygame as pg
import numpy as np
import math

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3 # 60 degrees
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 5
        self.rotation_speed = 0.005

        self.anglePitch = 0
        self.angleYaw = 0
        self.angleRoll = 0

    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_SPACE]:
            self.position += self.up * self.moving_speed
        if key[pg.K_LSHIFT]:
            self.position -= self.up * self.moving_speed

        x, y = pg.mouse.get_rel()
        if (x != 0 or y != 0):
            self.camera_yaw(x * self.rotation_speed)
            self.camera_pitch(y * self.rotation_speed)

    def camera_yaw(self, angle):
        self.angleYaw += angle

    def camera_pitch(self, angle):
        self.anglePitch += angle


    def projection_matrix(self):
        NEAR = self.render.camera.near_plane
        FAR = self.render.camera.far_plane
        return np.array([[(self.render.HEIGHT/self.render.WIDTH) * (1 / math.tan(self.render.camera.h_fov / 2)), 0, 0, 0],
                         [0, 1 / math.tan(self.render.camera.h_fov / 2), 0, 0,],
                         [0, 0, FAR / (FAR - NEAR), 1],
                         [0, 0, -1 * NEAR * FAR / (FAR - NEAR), 0]])
    
    def to_screen_matrix(self):
        return np.array([[self.render.WIDTH // 2, 0, 0, 0],
                         [0, -self.render.HEIGHT // 2, 0, 0],
                         [0, 0, 1, 0],
                         [self.render.WIDTH // 2, self.render.HEIGHT // 2, 0, 1]])
        
    def axiiIdentity(self):
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def camera_update_axii(self):
        rotation_x = lambda a: np.array([[1, 0, 0, 0],
                               [0, math.cos(a), math.sin(a), 0],
                               [0, -math.sin(a), math.cos(a), 0],
                               [0, 0, 0, 1]])

        rotation_y =lambda a: np.array([[math.cos(a), 0, -math.sin(a), 0],
                             [0, 1, 0, 0],
                             [math.sin(a), 0, math.cos(a), 0],
                             [0, 0, 0, 1]])
        
        rotate = rotation_x(self.anglePitch) @ rotation_y(self.angleYaw)
        self.axiiIdentity()
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_matrix(self):
        self.camera_update_axii()
        x, y, z, w = self.position
        translation_m = np.array([[1, 0, 0, 1],
                                  [0, 1, 0, 1],
                                  [0, 0, 1, 1],
                                  [-x, -y, -z, 1]])

        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        rotation_m = np.array([[rx, ux, fx, 0],
                               [ry, uy, fy, 0],
                               [rz, uz, fz, 0],
                               [0, 0, 0, 1]])

        return translation_m @ rotation_m