from modules.graphics.model import *
from modules.config.logger import setup_logging

logger = setup_logging()


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        self.skybox = SkyBox(app)

    def add_object(self, obj):
        """
        Add an object to the scene
        :param obj: object to add
        :return: None
        """
        self.objects.append(obj)

    def load(self):
        """
        Load objects into the scene
        :return: None
        """
        app = self.app
        add = self.add_object

        # add(Fish(app, tex_id=12, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)))

    def render(self):
        """
        Render the scene
        :return: None
        """
        for obj in self.objects:
            obj.render()
        self.skybox.render()
