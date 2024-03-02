from modules.controllers.kill_data_controllers import (create_killdata_objs_from_battle_report_data,
                                                       create_wreck_from_killdata,
                                                       scale_wreck, get_zkill_and_esi_data)
from modules.helpers.helpers import (get_solarsystemid_and_timestamp_from_zkillbr_link,
                                     get_battle_report_data, get_zkill_id_from_link)
from modules.models.killdata import KillData
from modules.models.wreck import Wreck


def create_both_wreck_lists(zkill_br_link: str) -> tuple[list[Wreck], list[Wreck]]:
    """
    Create two lists of wreck objects from a battle report link
    :param zkill_br_link: zkillboard battle report link
    :return: tuple of two lists of wreck objects
    """
    wreck_list_a = []
    wreck_list_b = []

    br_solarsystemid, br_timestamp = get_solarsystemid_and_timestamp_from_zkillbr_link(zkill_br_link)
    battle_report_data = get_battle_report_data(br_solarsystemid, br_timestamp)

    killdata_list_a = create_killdata_objs_from_battle_report_data(battle_report_data, 'teamA')
    killdata_list_b = create_killdata_objs_from_battle_report_data(battle_report_data, 'teamB')

    for kill_data in killdata_list_a:
        wreck = create_wreck_from_killdata(kill_data)
        if wreck is not None:
            wreck_list_a.append(wreck)

    for kill_data in killdata_list_b:
        wreck = create_wreck_from_killdata(kill_data)
        if wreck is not None:
            wreck_list_b.append(wreck)

    for wreck in wreck_list_a:
        wreck = scale_wreck(wreck)

    for wreck in wreck_list_b:
        wreck = scale_wreck(wreck)

    return wreck_list_a, wreck_list_b


def create_wreck_list_from_link_list(zkill_link_list) -> list[KillData]:
    """
    Create a list of wreck objects from a list of zkillboard links
    :param zkill_link_list: list of zkillboard links
    :return: list of wreck objects
    """
    wreck_list = []
    for zkill_link in zkill_link_list:
        zkill_id = get_zkill_id_from_link(zkill_link)
        zkill_data, esi_data = get_zkill_and_esi_data(zkill_id)
        kill_data_obj = KillData(zkill_id, zkill_data, esi_data)
        wreck = create_wreck_from_killdata(kill_data_obj)
        if wreck is not None:
            wreck_list.append(wreck)
    return wreck_list
