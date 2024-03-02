from modules.graphics.vbo import VBO
from modules.graphics.shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx,):

        self.ctx = ctx
        self.vbos = VBO(ctx)
        self.shader_program = ShaderProgram(ctx)
        self.vaos = {}

        self.vaos['cube'] = self.get_vao(
            program=self.shader_program.programs['default'],
            vbo=self.vbos.vbos['cube'])

        self.vaos['cube_red'] = self.get_vao(
            program=self.shader_program.programs['default_red'],
            vbo=self.vbos.vbos['cube'])

        self.vaos['cube_blue'] = self.get_vao(
            program=self.shader_program.programs['default_blue'],
            vbo=self.vbos.vbos['cube'])

        self.vaos['cat'] = self.get_vao(
            program=self.shader_program.programs['default'],
            vbo=self.vbos.vbos['cat'])

        self.vaos['fish'] = self.get_vao(
            program=self.shader_program.programs['default'],
            vbo=self.vbos.vbos['fish'])

        self.vaos['skybox'] = self.get_vao(
            program=self.shader_program.programs['skybox'],
            vbo=self.vbos.vbos['skybox'])

    def get_vao(self, program, vbo):
        """
        Create a vertex array object
        :param program: shader program
        :param vbo: vertex buffer object
        :return: vertex array object
        """
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao

    def destroy(self):
        """
        Destroy the vertex array object
        :return: None
        """
        self.vbos.destroy()
        self.shader_program.destroy()
