import numpy as np
import moderngl as mgl
import pywavefront


class VBO:
    def __init__(self, ctx):
        self.vbos = {}
        self.vbos['cube'] = CubeVBO(ctx)
        self.vbos['cat'] = CatVBO(ctx)
        self.vbos['fish'] = FishVBO(ctx)
        self.vbos['skybox'] = SkyboxVBO(ctx)

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]


class BaseVBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attribs: list = None

    def get_vertex_data(self):
        """
        Get the vertex data for the VBO
        """
        pass

    def get_vbo(self):
        """
        Get the VBO for the vertex data
        """
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        """
        Release the VBO
        """
        self.vbo.release()


class CubeVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    @staticmethod
    def get_data(vertices, indices):
        """
        Get the data for the cube
        """
        data = [vertices[i] for triangle in indices for i in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        """
        Get the vertex data for the cube
        """
        cube_vertices = [(1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1),
                         (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1)]
        cube_indices = [(0, 1, 2), (0, 2, 3),
                        (0, 4, 5), (0, 5, 1),
                        (0, 3, 7), (0, 7, 4),
                        (6, 2, 1), (6, 1, 5),
                        (6, 5, 4), (6, 4, 7),
                        (6, 7, 3), (6, 3, 2)]

        vertex_data = self.get_data(cube_vertices, cube_indices)

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 1, 2), (0, 2, 3),
                             (0, 1, 2), (0, 2, 3),
                             (0, 1, 2), (0, 2, 3),
                             (0, 1, 2), (0, 2, 3),
                             (0, 1, 2), (0, 2, 3),
                             (0, 1, 2), (0, 2, 3)]
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        normals = [(0, 0, 1) * 6,
                   (0, 0, -1) * 6,
                   (1, 0, 0) * 6,
                   (-1, 0, 0) * 6,
                   (0, 1, 0) * 6,
                   (0, -1, 0) * 6]
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data


class CatVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('modules/graphics/objects/cat/20430_Cat_v1_NEW.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = np.array(obj.vertices, dtype='f4')
        return vertex_data


class FishVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('modules/graphics/objects/fish/fish.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = np.array(obj.vertices, dtype='f4')
        return vertex_data


class SkyboxVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f'
        self.attribs = ['in_position']

    @staticmethod
    def get_data(vertices, indices):
        """
        Get the data for the cube
        """
        data = [vertices[i] for triangle in indices for i in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        """
        Get the vertex data for the cube
        """
        cube_vertices = [(1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1),
                         (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1)]
        cube_indices = [(0, 1, 2), (0, 2, 3),
                        (0, 4, 5), (0, 5, 1),
                        (0, 3, 7), (0, 7, 4),
                        (6, 2, 1), (6, 1, 5),
                        (6, 5, 4), (6, 4, 7),
                        (6, 7, 3), (6, 3, 2)]

        vertex_data = self.get_data(cube_vertices, cube_indices)
        vertex_data = np.flip(vertex_data, 1).copy(order='C')

        return vertex_data
