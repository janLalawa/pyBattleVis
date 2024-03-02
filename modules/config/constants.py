class Paths:
    LOG_PATH = "./application.log"
    CHAR_IMG_PATH = "./static/char_images"
    SHIP_IMG_PATH = "./static/ship_images"


class Constants:
    IMG_DOWNLOAD_RETIRES = 2
    IMG_DOWNLOAD_SLEEP_TIME = 0.75
    ESI_RATE_LIMIT_SECONDS = 0.5
    ZKILL_RATE_LIMIT_SECONDS = 1.1


class ShipScales:
    SCALE_DICT: dict = {
        25: 0.3,  # Frigate
        26: 0.6,  # Cruiser
        27: 1.1,  # Battleship
        28: 0.7,  # Hauler
        29: 0.2,  # Capsule
        30: 3.4,  # Titan
        31: 0.25,  # Shuttle
        237: 0.25,  # Corvette
        324: 0.3,  # Assault Frigate
        358: 0.6,  # Heavy Assault Cruiser
        380: 0.7,  # Deep Space Transport
        381: 1.2,  # Elite Battleship
        419: 0.8,  # Combat Battlecruiser
        420: 0.4,  # Destroyer
        463: 0.5,  # Mining Barge
        485: 2.5,  # Dreadnought
        513: 2,  # Freighter
        540: 0.8,  # Command Ship
        541: 0.45,  # Interdictor
        543: 0.5,  # Exhumer
        547: 2,  # Carrier
        659: 2.8,  # Supercarrier
        830: 0.35,  # Covert Ops
        831: 0.35,  # Interceptor
        832: 0.6,  # Logistics
        833: 0.6,  # Force Recon Ship
        834: 0.35,  # Stealth Bomber
        883: 2.1,  # Capital Industrial Ship
        893: 0.25,  # Electronic Attack Ship
        894: 0.6,  # Heavy Interdiction Cruiser
        898: 1.2,  # Black Ops
        900: 1.2,  # Marauder
        902: 2.4,  # Jump Freighter
        906: 0.6,  # Combat Recon Ship
        941: 0.8,  # Industrial Command Ship
        963: 0.6,  # Strategic Cruiser
        1022: 0.25,  # Prototype Exploration Ship
        1201: 0.8,  # Attack Battlecruiser
        1202: 0.7,  # Blockade Runner
        1283: 0.35,  # Expedition Frigate
        1305: 0.45,  # Tactical Destroyer
        1527: 0.3,  # Logistics Frigate
        1534: 0.45,  # Command Destroyer
        1538: 2.7,  # Force Auxiliary
        1972: 0.65,  # Flag Cruiser
        2001: 0.25,  # Citizen Ships
        4594: 2.5,  # Lancer Dreadnought
    }


class UiText:
    APP_TITLE = 'Zkillboard 3D View Generator'
    HELP_TEXT = "Enter a zkillboard battle report link and click 'Generate' to start. It WILL take a moment!"
