import requests
import json


class Wreck:
    def __init__(self,
                 zkill_link: str = None,
                 pos_x: float = None,
                 pos_y: float = None,
                 pos_z: float = None,
                 ship_type_name: str = None,
                 victim_name: str = None,
                 total_value: float = None,
                 zkill_data: dict = None,
                 kill_hash: str = None,
                 esi_data: dict = None):
        self.zkill_link = zkill_link
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.ship_type_name = ship_type_name
        self.victim_name = victim_name
        self.total_value = total_value
        self.zkill_data = zkill_data
        self.kill_hash = kill_hash
        self.esi_data = esi_data

    def populate_pos(self):
        self.pos_x = float(self.esi_data['victim']['position']['x'])
        self.pos_y = float(self.esi_data['victim']['position']['y'])
        self.pos_z = float(self.esi_data['victim']['position']['z'])
        return self

    def populate_victim_name(self):
        victim_char_id = self.esi_data['victim']['character_id']
        victim_char_response = requests.get(
            'https://esi.evetech.net/latest/characters/' + str(victim_char_id) + '/?datasource=tranquility')
        self.victim_name = json.loads(victim_char_response.text)['name']
        return self

    def populate_ship_type(self):
        victim_ship_id = self.esi_data['victim']['ship_type_id']
        victim_ship_response = requests.get('https://esi.evetech.net/latest/universe/types/' + str(
            victim_ship_id) + '/?datasource=tranquility&language=en')
        self.ship_type_name = json.loads(victim_ship_response.text)['name']
        return self

    def populate_total_value(self):
        total_value = self.zkill_data[0]['zkb']['totalValue']
        self.total_value = float(total_value)
        return self
