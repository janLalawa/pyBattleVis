

class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}
        self.programs['default'] = self.get_program('default')
        self.programs['default_red'] = self.get_program('default_red')
        self.programs['default_blue'] = self.get_program('default_blue')
        self.programs['skybox'] = self.get_program('skybox')

    def get_program(self, shader_program_name):
        """
        Get the shader program
        :param shader_program_name: The name of the shader program
        :return: Program
        """
        with open(f'modules/graphics/shaders/{shader_program_name}.vert', 'r') as file:
            vertex_shader = file.read()

        with open(f'modules/graphics/shaders/{shader_program_name}.frag', 'r') as file:
            fragment_shader = file.read()

        shader_program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return shader_program

    def destroy(self):
        """
        Release the shader programs
        """
        [program.release() for program in self.programs.values()]