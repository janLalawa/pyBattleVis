import requests
import json
from modules.config.logger import setup_logging
import time
import re
from modules.config.constants import Constants

logger = setup_logging()


def get_zkill_id_from_link(zkill_link: str) -> str:
    """
    Extracts the zkill id from a zkill link
    :param zkill_link: str
    :return: str
    """
    return zkill_link.split('/')[-2]


def get_solarsystemid_and_timestamp_from_zkillbr_link(zkill_br_link: str) -> tuple:
    """
    Extracts the solar system id and timestamp from a zkill battle report link
    :param zkill_br_link: str
    :return: tuple
    """
    pattern = r".*/related/(\d+)/(\d+)/?$"
    match = re.search(pattern, zkill_br_link)
    if match:
        solar_system_id, timestamp = match.groups()
        return solar_system_id, timestamp
    else:
        logger.error(f"Could not find solar system id and timestamp from {zkill_br_link}")
        return None, None


def get_zkill_data(zkill_id: str):
    """
    Gets zkill data for a given zkill id
    :param zkill_id: str
    :return: dict
    """
    logger.info(f"Getting zkill data for {zkill_id}, waiting 1.1 seconds to avoid rate limiting")
    time.sleep(1.1)
    zkill_response = requests.get('https://zkillboard.com/api/killID/' + zkill_id + '/')
    logger.info(f"API Response Code: {zkill_response.status_code} and reason: {zkill_response.reason}")
    zkill_data = json.loads(zkill_response.text)
    return zkill_data


def get_battle_report_data(solarsystemid: str, timestamp: str) -> dict:
    """
    Gets battle report data for a given solar system id and timestamp
    :param solarsystemid: str
    :param timestamp: str
    :return: Battle Report Data Json dict
    """
    base_url = 'https://zkillboard.com/api/related'
    battle_report_api_url = f'{base_url}/{solarsystemid}/{timestamp}'

    logger.info(f"Getting battle report data for {solarsystemid} at {timestamp}")
    battle_report_response = requests.get(battle_report_api_url)
    logger.info(f"API Response Code: {battle_report_response.status_code} and reason: {battle_report_response.reason}")
    battle_report_data = json.loads(battle_report_response.text)

    if len(battle_report_data) == 0:
        logger.error(f"No data found for {solarsystemid} at {timestamp}. Might be caused by the zkill API being weird")
        logger.info(f"Trying again in 2 seconds with a different URL")
        time.sleep(2)
        battle_report_api_url = battle_report_api_url + '/'
        battle_report_response = requests.get(battle_report_api_url)
        battle_report_data = json.loads(battle_report_response.text)

        if len(battle_report_data) == 0:
            logger.error(f"Nope, adding a / didn't help. Sorry about that. Returning None.")
            return None
        else:
            logger.info(f"Success! Got data from {battle_report_api_url}")
            return battle_report_data

    return battle_report_data


def get_kill_hash(zkill_data: dict) -> str:
    """
    Gets the kill hash from zkill data
    :param zkill_data: dict
    :return: str
    """
    return zkill_data[0]['zkb']['hash']


def get_esi_data(kill_hash: str, zkill_id: str) -> dict:
    """
    Gets ESI data for a given kill hash and zkill id
    :param kill_hash: str
    :param zkill_id: str
    :return: esi data Json dict
    """
    logger.info(f"Getting ESI data for {zkill_id}")
    time.sleep(Constants.ESI_RATE_LIMIT_SECONDS)
    esi_response = requests.get(
        'https://esi.evetech.net/latest/killmails/' + zkill_id + '/' + kill_hash + '/?datasource=tranquility')
    logger.info(f"API Response Code: {esi_response.status_code} and reason: {esi_response.reason}")
    esi_data = json.loads(esi_response.text)
    return esi_data


def scale_locals_to_game(pos_x, pos_y, pos_z, scale_factor=1000):
    """
    Scales local coordinates to game coordinates
    :param pos_x: int
    :param pos_y: int
    :param pos_z: int
    :param scale_factor: int
    :return: (x, y, z) coordinates tuple
    """
    return pos_x / scale_factor, pos_y / scale_factor, pos_z / scale_factor


def scale_coordinates_to_local_positions(pos_x, pos_y, pos_z):
    """
    Scales game coordinates to local coordinates by taking the modulo 100000 of the coordinates. Effectively narrows
    down from system-wide coordinates to local coordinates.
    :param pos_x: int
    :param pos_y: int
    :param pos_z: int
    :return: (x, y, z) coordinates tuple
    """
    local_pos_x: int = int(pos_x) % 100000
    local_pos_y: int = int(pos_y) % 100000
    local_pos_z: int = int(pos_z) % 100000
    return local_pos_x, local_pos_y, local_pos_z
