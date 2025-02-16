import configparser

def get_config(CONFIG_DIR):
    CONFIG = configparser.ConfigParser()
    CONFIG.read(f"{CONFIG_DIR}/development.cfg")
    return CONFIG
