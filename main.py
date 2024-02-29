from modules.helpers.helpers import get_zkill_id_from_link
from modules.controllers.kill_data_controllers import get_zkill_and_esi_data, create_wreck_from_killData, scale_wreck
from modules.models.killdata import KillData
from modules.graphics.graphics_engine import GraphicsEngine
from modules.graphics.model import Fish, Cat, Cube

zkill_link_list = ['https://zkillboard.com/kill/107761136/',
                   'https://zkillboard.com/kill/107761119/',
                   'https://zkillboard.com/kill/107760928/',
                   'https://zkillboard.com/kill/107760946/',
                   'https://zkillboard.com/kill/107761063/',
                   'https://zkillboard.com/kill/107760999/']

def main() -> None:
    wreck_list = []

    for zkill_link in zkill_link_list:
        zkill_id = get_zkill_id_from_link(zkill_link)
        zkill_data, esi_data = get_zkill_and_esi_data(zkill_id)
        kill_data_obj = KillData(zkill_id, zkill_data, esi_data)
        wreck = create_wreck_from_killData(kill_data_obj)
        if wreck is not None:
            wreck_list.append(wreck)

    for wreck in wreck_list:
        print(f"pos_x: {wreck.pos_x}, pos_y: {wreck.pos_y}, pos_z: {wreck.pos_z}")
        wreck = scale_wreck(wreck)
        print(f"pos_x: {wreck.pos_x}, pos_y: {wreck.pos_y}, pos_z: {wreck.pos_z}")

    app = GraphicsEngine()

    for wreck in wreck_list:
        app.scene.add_object(
            Cube(app, tex_id=4, pos=(wreck.pos_x, wreck.pos_y, wreck.pos_z), scale=(0.6, 0.6, 0.6)))

    app.run()


if __name__ == '__main__':
    main()
