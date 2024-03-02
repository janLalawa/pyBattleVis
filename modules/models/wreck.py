import requests, json, os, time
from modules.config.logger import setup_logging
from modules.config.constants import Paths

logger = setup_logging()


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
                 esi_data: dict = None,
                 char_id: int = None,
                 char_img_path: str = None,
                 ship_id: int = None,
                 ship_img_path: str = None,
                 ship_scale: float = 0.6):
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
        self.char_id = char_id
        self.char_img_path = char_img_path
        self.ship_id = ship_id
        self.ship_img_path = ship_img_path
        self.ship_scale = ship_scale

    def populate_pos(self):
        """
        Populates the position of the wreck from the ESI data
        :return: self
        """
        self.pos_x = float(self.esi_data['victim']['position']['x'])
        self.pos_y = float(self.esi_data['victim']['position']['y'])
        self.pos_z = float(self.esi_data['victim']['position']['z'])
        return self

    def populate_victim_name(self):
        """
        Populates the victim name from the ESI data
        :return: self
        """
        if 'character_id' in self.esi_data['victim']:
            victim_char_id = self.esi_data['victim']['character_id']
            victim_char_response = requests.get(
                'https://esi.evetech.net/latest/characters/' + str(victim_char_id) + '/?datasource=tranquility')
            victim_char_data = json.loads(victim_char_response.text)
            if 'name' in victim_char_data:
                self.victim_name = victim_char_data['name']
            else:
                self.victim_name = 'Unknown'
        else:
            self.victim_name = 'Unknown'
        return self

    def populate_ship_type(self):
        """
        Populates the ship type name from the ESI data
        :return: self
        """
        victim_ship_id = self.esi_data['victim']['ship_type_id']
        victim_ship_response = requests.get('https://esi.evetech.net/latest/universe/types/' + str(
            victim_ship_id) + '/?datasource=tranquility&language=en')
        victim_ship_data = json.loads(victim_ship_response.text)
        if 'name' in victim_ship_data:
            self.ship_type_name = victim_ship_data['name']
        else:
            'Unknown'
        return self

    def populate_total_value(self):
        """
        Populates the total value from the zkill data
        :return: self
        """
        total_value = self.zkill_data[0]['zkb']['totalValue']
        self.total_value = float(total_value)
        return self

    def populate_char_img(self):
        if 'character_id' in self.esi_data['victim']:
            self.char_id = self.esi_data['victim']['character_id']
            file_path = f'{Paths.CHAR_IMG_PATH}/{self.char_id}.png'

            if not os.path.exists(Paths.CHAR_IMG_PATH):
                os.makedirs(Paths.CHAR_IMG_PATH)
            if not os.path.exists(file_path):
                logger.debug(f"Getting character image for {self.char_id}")
                time.sleep(0.5)
                victim_char_img_response = requests.get(
                    f'https://images.evetech.net/characters/' + str(self.char_id) + '/portrait?size=256')
                if victim_char_img_response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(victim_char_img_response.content)
                else:
                    self.char_img_path = None
                    return self
            else:
                logger.debug(f"Character image for {self.char_id} already exists!")
                self.char_img_path = file_path
        else:
            self.char_img_path = None
        return self

    def populate_ship_img(self):
        if 'ship_type_id' not in self.esi_data['victim']:
            self.ship_img_path = None
            return self

        self.ship_id = self.esi_data['victim']['ship_type_id']
        file_path = f'{Paths.SHIP_IMG_PATH}/{self.ship_id}.png'

        if not os.path.exists(Paths.SHIP_IMG_PATH):
            os.makedirs(Paths.SHIP_IMG_PATH)

        if not os.path.exists(file_path):
            logger.debug(f"Getting ship image for {self.ship_type_name}")
            time.sleep(0.5)
            ship_img_response = requests.get(
                f'https://images.evetech.net/types/' + str(self.ship_id) + '/render?size=256')

            if ship_img_response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(ship_img_response.content)

            else:
                self.ship_img_path = None
                return self

        else:
            logger.debug(f"Ship image for {self.ship_type_name} already exists!")
            self.ship_img_path = file_path
        return self

    def populate_ship_scale(self):
        if self.total_value:
            self.ship_scale = self.total_value / 200000000
        return self
