import json
import os

CONFIG_FILE="settings.json"
CONFIG_PATH="pyguard/user/settings/"
CONFIG__=f"{CONFIG_PATH}{CONFIG_FILE}"


def load_config():
    if not os.path.exists(CONFIG__):
        os.makedirs(os.path.dirname(CONFIG__), exist_ok=True)
        with open(CONFIG__, 'w') as file:
            json.dump({"APP_AUTO_UPDATE": True}, file)

    with open(CONFIG__, 'r') as file:
        config = json.load(file)
        
    # Convert JSON booleans to Python booleans
    config['APP_AUTO_UPDATE'] = bool(config.get('APP_AUTO_UPDATE', True))
    return config

def save_config(config):
    with open(CONFIG__, 'w') as file:
        json.dump(config, file, indent=4)
