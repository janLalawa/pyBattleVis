import numpy as np
import glm
import pygame as pg
from modules.config import logger

logger = logger.setup_logging()


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = app.camera

    def update(self):
        """
        Update the model
        """
        ...

    def get_model_matrix(self):
        """
        Get the model matrix
        Takes the position, rotation and scale and returns the model matrix
        return: m_model glm.mat4
        """
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def render(self):
        self.update()
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.rotate()
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_model'].write(self.m_model)
        self.program['m_view'].write(self.camera.m_view)

    def rotate(self):
        """
        Rotate the model around (0, 1, 1)
        """
        self.m_model = glm.rotate(self.m_model, self.app.delta_time * 0.0001, glm.vec3(0, 1, 1))

    def on_init(self):
        """
        Set the initial uniforms
        """
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()

        self.program['m_projection'].write(self.camera.m_projection)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)


class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class Cat(ExtendedBaseModel):
    def __init__(self, app, vao_name='cat', tex_id=6, pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class Fish(ExtendedBaseModel):
    def __init__(self, app, vao_name='fish', tex_id=12, pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class SkyBox(BaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)

        self.program['m_projection'].write(self.camera.m_projection)
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))
