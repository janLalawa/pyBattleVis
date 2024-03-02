import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        # There are a ton of random test textures here.
        self.textures[0] = self.get_texture(path='modules/graphics/textures/img.png')
        self.textures[1] = self.get_texture(path='modules/graphics/textures/img_1.png')
        self.textures[2] = self.get_texture(path='modules/graphics/textures/img_2.png')
        self.textures[3] = self.get_texture(path='modules/graphics/textures/test.png')
        self.textures[4] = self.get_texture(path='modules/graphics/textures/foxholers.png')
        self.textures[5] = self.get_texture(path='modules/graphics/textures/outblobbed_1.png')
        self.textures[6] = self.get_texture(path='modules/graphics/objects/cat/20430_cat_diff_v1.jpg')
        self.textures[7] = self.get_texture(path='modules/graphics/objects/fish/fish_texture.png')
        self.textures['skybox'] = self.get_texture_cube(dir_path='modules/graphics/textures/skyboxc5', ext='png')

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        textures = []
        for face in faces:
            texture = pg.image.load(f'{dir_path}/{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, True, False)
            else:
                texture = pg.transform.flip(texture, False, True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path):
        """
        Get a texture from a file path
        :param path: file path
        :return: texture
        """
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, False, True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        # mipmap
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        """
        Destroy the textures
        :return: None
        """
        [texture.release() for texture in self.textures.values()]
