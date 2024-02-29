from modules.graphics.model import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        # add(Fish(app, tex_id=12, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)))

    def render(self):
        for obj in self.objects:
            obj.render()
