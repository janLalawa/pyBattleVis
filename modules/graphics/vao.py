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

        self.vaos['cat'] = self.get_vao(
            program=self.shader_program.programs['default'],
            vbo=self.vbos.vbos['cat'])

        self.vaos['fish'] = self.get_vao(
            program=self.shader_program.programs['default'],
            vbo=self.vbos.vbos['fish'])

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao

    def destroy(self):
        self.vbos.destroy()
        self.shader_program.destroy()