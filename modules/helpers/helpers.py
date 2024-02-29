import requests
import json
from modules.config.logger import setup_logging
import time

logger = setup_logging()


def get_zkill_id_from_link(zkill_link: str) -> str:
    return zkill_link.split('/')[-2]


def get_zkill_data(zkill_id: str):
    logger.info(f"Getting zkill data for {zkill_id}, waiting 1.1 seconds to avoid rate limiting")
    time.sleep(1.1)
    zkill_response = requests.get('https://zkillboard.com/api/killID/' + zkill_id + '/')
    logger.info(f"API Response Code: {zkill_response.status_code} and reason: {zkill_response.reason}")
    zkill_data = json.loads(zkill_response.text)
    return zkill_data


def get_kill_hash(zkill_data: dict) -> str:
    return zkill_data[0]['zkb']['hash']


def get_esi_data(kill_hash: str, zkill_id: str) -> dict:
    logger.info(f"Getting ESI data for {zkill_id}")
    esi_response = requests.get(
        'https://esi.evetech.net/latest/killmails/' + zkill_id + '/' + kill_hash + '/?datasource=tranquility')
    logger.info(f"API Response Code: {esi_response.status_code} and reason: {esi_response.reason}")
    esi_data = json.loads(esi_response.text)
    return esi_data


def scale_locals_to_game(pos_x, pos_y, pos_z, scale_factor=2000):
    return pos_x / scale_factor, pos_y / scale_factor, pos_z / scale_factor


def scale_coordinates_to_local_positions(pos_x, pos_y, pos_z):
    local_pos_x: int = int(pos_x) % 100000
    local_pos_y: int = int(pos_y) % 100000
    local_pos_z: int = int(pos_z) % 100000
    return local_pos_x, local_pos_y, local_pos_z
