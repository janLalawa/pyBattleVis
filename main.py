import time

import modules.controllers.facade as facade
from modules.graphics.graphics_engine import GraphicsEngine
from modules.controllers.texture_controller import create_mgl_textures_from_wreck_list
from modules.controllers.scene_controller import build_scene_from_wreck_list
from modules.config.logger import setup_logging

logger = setup_logging()

TEXTURE_TYPE = 'ship'
# ZKILL_BR_LINK = 'https://zkillboard.com/related/31001761/202012040000'
ZKILL_BR_LINK = 'https://zkillboard.com/related/30002807/202403020300/'
# ZKILL_BR_LINK = 'https://zkillboard.com/related/31001880/202403020200/'


def main() -> None:
    wreck_list_a, wreck_list_b = facade.create_both_wreck_lists(ZKILL_BR_LINK)
    logger.info(f"Length of wreck_list_a: {len(wreck_list_a)}")
    logger.info(f"Length of wreck_list_b: {len(wreck_list_b)}")

    logger.info("Spinning up the graphics engine. This may take a moment!")

    time.sleep(3)  # Give the logger time to catch up and let the user know it's not frozen.

    app = GraphicsEngine()

    logger.info("Creating ModernGL textures from wreck lists")
    create_mgl_textures_from_wreck_list(app, tex_type=TEXTURE_TYPE, wreck_list=wreck_list_a)
    create_mgl_textures_from_wreck_list(app, tex_type=TEXTURE_TYPE, wreck_list=wreck_list_b)

    # for wreck in wreck_list_a:
    #     wreck.populate_ship_scale()
    # for wreck in wreck_list_b:
    #     wreck.populate_ship_scale()

    logger.info("Building scene from wreck lists")
    build_scene_from_wreck_list(app, tex_type=TEXTURE_TYPE, vao_name='cube_red', wreck_list=wreck_list_a)
    build_scene_from_wreck_list(app, tex_type=TEXTURE_TYPE, vao_name='cube_blue', wreck_list=wreck_list_b)

    logger.info("Rendering the scene")
    app.run()


if __name__ == '__main__':
    main()
