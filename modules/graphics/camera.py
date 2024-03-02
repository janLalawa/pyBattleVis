import glm
import pygame as pg

FOV = 80.0
NEAR = 0.1
FAR = 350.0
SPEED = 0.04
SENSITIVITY = 0.1

class Camera:
    def __init__(self, app, position=(-30, 90, 80), yaw=2, pitch=-30):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        self.m_view = self.get_view_matrix()
        self.m_projection = self.get_projection_matrix()

    def rotate(self):
        """
        Rotates the camera based on mouse movement
        """
        if pg.key.get_focused():
            rel_x, rel_y = pg.mouse.get_rel()
            self.yaw += rel_x * SENSITIVITY
            self.pitch -= rel_y * SENSITIVITY
            self.pitch = max(-89, min(89, self.pitch))

            self.forward.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))

    def update_camera_vectors(self):
        """
        Updates the camera vectors based on the current yaw and pitch
        """
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        """
        Updates the camera's view and projection matrices
        """
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()
        self.m_projection = self.get_projection_matrix()

    def move(self):
        """
        Moves the camera based on keyboard input
        """
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity

    def get_view_matrix(self):
        """
        Returns the view matrix for the camera
        """
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        """
        Returns the projection matrix for the camera
        """
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
