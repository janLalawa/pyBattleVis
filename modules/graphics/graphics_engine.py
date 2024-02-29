import moderngl as mgl
import sys
from modules.graphics.model import *
from modules.graphics.camera import Camera
from modules.graphics.light import Light
from modules.graphics.mesh import Mesh
from modules.graphics.scene import Scene


class GraphicsEngine:
    def __init__(self, win_size=(1600, 900), win_title="Graphics Engine"):
        pg.init()
        self.WIN_SIZE = win_size
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption(win_title)
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        self.ctx = mgl.create_context()
        self.ctx.front_face = 'ccw'
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        self.light = Light()
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.hold_mouse_centre = True

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                self.hold_mouse_centre = True
            elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
                self.hold_mouse_centre = False

    def render(self):
        self.ctx.clear(0.03, 0.88, 0.59)
        self.scene.render()
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() / 1000

    def handle_mouse_window_focus(self):
        if pg.key.get_focused():
            pg.event.set_grab(False)
            if self.hold_mouse_centre:
                pg.mouse.set_pos([self.WIN_SIZE[0] // 2, self.WIN_SIZE[1] // 2])
                pg.mouse.set_visible(False)

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.handle_mouse_window_focus()
            self.delta_time = self.clock.tick(60)


def main():
    app = GraphicsEngine()

    app.run()


if __name__ == '__main__':
    main()
