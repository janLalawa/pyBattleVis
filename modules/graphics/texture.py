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

    def get_texture(self, path):
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
        [texture.release() for texture in self.textures.values()]
