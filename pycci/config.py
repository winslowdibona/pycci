import os
import yaml

CONFIG_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/config.yaml'

class Config:
    BASE_URL = 'https://circleci.com/api/v2'
    ORG = None
    API_KEY = None

    @staticmethod
    def API_HEADER():
        return {'Circle-Token': Config.API_KEY}

    @staticmethod
    def ORG_SLUG():
        return f'gh/{Config.ORG}'

    @staticmethod
    def initialize(org, api_key, store=False):
        Config.ORG = org
        Config.API_KEY = api_key
        if store:
            Config._store_config()

    @staticmethod
    def _load_config():
        with open(CONFIG_PATH, 'r') as config_file:
            data = yaml.load(config_file, Loader=yaml.FullLoader)
            Config.ORG = data['config']['org']
            Config.API_KEY = data['config']['api_key']

    @staticmethod
    def _store_config():
        _config = {'config': {'org': Config.ORG, 'api_key': Config.API_KEY}}
        with open(CONFIG_PATH, 'w') as config_file:
            _ = yaml.dump(_config, config_file)
