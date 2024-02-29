from modules.config.logger import setup_logging
from modules.helpers.helpers import (get_zkill_data, get_esi_data, get_kill_hash, scale_locals_to_game,
                                     scale_coordinates_to_local_positions)
from modules.models.killdata import KillData
from modules.models.wreck import Wreck

logger = setup_logging()


def get_zkill_and_esi_data(zkill_id: str):
    zkill_data = get_zkill_data(zkill_id)
    if len(zkill_data) != 1:
        logger.error(f"No zkill data found for {zkill_id}")
        return None
    kill_hash = get_kill_hash(zkill_data)
    esi_data = get_esi_data(kill_hash, zkill_id)
    return zkill_data, esi_data


def create_wreck_from_killData(kill_data: KillData):
    current_kill_hash = get_kill_hash(kill_data.zkill_data)
    wreck = Wreck(kill_data.killmail_id,
                  zkill_data=kill_data.zkill_data,
                  esi_data=kill_data.esi_data,
                  kill_hash=current_kill_hash
                  )
    wreck.populate_pos()
    wreck.populate_ship_type()
    wreck.populate_victim_name()
    wreck.populate_total_value()
    return wreck


def scale_wreck(wreck):
    wreck.pos_x, wreck.pos_y, wreck.pos_z = scale_coordinates_to_local_positions(wreck.pos_x, wreck.pos_y, wreck.pos_z)
    wreck.pos_x, wreck.pos_y, wreck.pos_z = scale_locals_to_game(wreck.pos_x, wreck.pos_y, wreck.pos_z)
    return wreck
