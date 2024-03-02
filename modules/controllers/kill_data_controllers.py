from modules.config.logger import setup_logging
from modules.helpers.helpers import (get_zkill_data, get_esi_data, get_kill_hash, scale_locals_to_game,
                                     scale_coordinates_to_local_positions)
from modules.models.killdata import KillData
from modules.models.wreck import Wreck

logger = setup_logging()


def get_zkill_and_esi_data(zkill_id: str):
    """
    Get zkill and esi data for a single killmail
    :param zkill_id: str
    :return: tuple
    """
    zkill_data = get_zkill_data(zkill_id)
    if len(zkill_data) != 1:
        logger.error(f"No zkill data found for {zkill_id}")
        return None
    kill_hash = get_kill_hash(zkill_data)
    esi_data = get_esi_data(kill_hash, zkill_id)
    return zkill_data, esi_data


def get_zkillids_from_battle_report_data(battle_report_data: dict, team: str) -> list[int]:
    """
    Get zkill_ids from a battle report data
    :param battle_report_data: dict
    :param team: str
    :return: list[int]
    """
    zkill_ids = []
    for kill in battle_report_data['summary'][team]['kills']:
        zkill_ids.append(kill['killmail_id'])
    return zkill_ids


def create_killdata_objs_from_battle_report_data(battle_report_data: dict, team: str):
    """
    Create a list of KillData objects from a battle report data
    :param battle_report_data: dict
    :param team: str
    :return: list[KillData]
    """
    killdata_list = []

    kill_dict: dict = battle_report_data['summary'][team]['kills']

    for kill in kill_dict.values():
        logger.info(f"Creating killdata object for {kill.get('killID')}")
        zkill_id = str(kill.get('killID'))
        kill_hash = kill.get('zkb').get('hash')
        esi_data = get_esi_data(kill_hash, zkill_id)
        killdata_obj = KillData(zkill_id, [kill], esi_data)
        killdata_list.append(killdata_obj)
        logger.info(f"Created KillData object {killdata_obj}")

    return killdata_list


def create_wreck_from_killdata(kill_data: KillData):
    """
    Create a Wreck object from a KillData object
    :param kill_data: KillData
    :return: Wreck
    """
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


def scale_wreck(wreck, scale_factor=1000):
    """
    Scale a Wreck object first down to locals in the battle and then by a factor to make viewable.
    :param wreck: Wreck
    :param scale_factor: int
    :return: Wreck
    """
    wreck.pos_x, wreck.pos_y, wreck.pos_z = scale_coordinates_to_local_positions(wreck.pos_x, wreck.pos_y, wreck.pos_z)
    wreck.pos_x, wreck.pos_y, wreck.pos_z = scale_locals_to_game(wreck.pos_x, wreck.pos_y, wreck.pos_z, scale_factor)
    return wreck
