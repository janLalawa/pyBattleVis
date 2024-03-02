from modules.graphics.graphics_engine import GraphicsEngine
from modules.graphics.model import Fish, Cube
from modules.models.wreck import Wreck
from modules.config import logger

logger = logger.setup_logging()


def build_scene_from_wreck_list(app: GraphicsEngine, tex_type: str, vao_name: str, wreck_list: list[Wreck]) -> None:
    """
    Build the scene from a wreck list by placing cubes or fish at the wreck positions. Fish used where no image found.
    :param app: GraphicsEngine
    :param tex_type: str (Valid: 'ship', 'char')
    :param vao_name: str (Valid: 'cube', 'cube_red', 'cube_blue', 'cat', 'fish')
    :param wreck_list: list[Wreck]
    :return: None
    """
    for wreck in wreck_list:
        if tex_type == 'ship':
            tex_id = wreck.ship_id
            tex_path = wreck.ship_img_path

        elif tex_type == 'char':
            tex_id = wreck.char_id
            tex_path = wreck.char_img_path

        else:
            tex_id = 3  # Default texture
            tex_path = 'modules/graphics/textures/test.png'

        logger.debug(f"Adding wreck of {wreck.victim_name}"
                     f" in a {wreck.ship_type_name}"
                     f" at {wreck.pos_x}, {wreck.pos_y}, {wreck.pos_z}")

        if tex_path:
            app.scene.add_object(
                Cube(app,
                     tex_id=tex_id,
                     vao_name=vao_name,
                     pos=(wreck.pos_x, wreck.pos_y, wreck.pos_z),
                     scale=(wreck.ship_scale, wreck.ship_scale, wreck.ship_scale)))
        else:
            app.scene.add_object(
                Fish(app,
                     vao_name=vao_name,
                     rot=(-90, 0, 0),
                     tex_id=7,
                     pos=(wreck.pos_x, wreck.pos_y, wreck.pos_z),
                     scale=(0.6, 0.6, 0.6)))
