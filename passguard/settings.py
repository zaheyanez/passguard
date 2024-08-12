import json
import os
from passguard.config import CONFIG_FILE, CONFIG_PATH

SETTINGS=f"{CONFIG_PATH}{CONFIG_FILE}"

def load_config():
    if not os.path.exists(SETTINGS):
        os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
        with open(SETTINGS, 'w') as file:
            json.dump({"APP_AUTO_UPDATE": True}, file)

    with open(SETTINGS, 'r') as file:
        config = json.load(file)
        
    # Convert JSON booleans to Python booleans
    config['APP_AUTO_UPDATE'] = bool(config.get('APP_AUTO_UPDATE', True))
    return config

def save_config(config):
    with open(SETTINGS, 'w') as file:
        json.dump(config, file, indent=4)
