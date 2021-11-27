from re import compile as re_compile
from requests import get, ConnectionError, exceptions, Timeout
import os, json
import urllib.parse

DEFAULT_CONFIG = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/tc.json"))
CHAT_TOKEN = "CHAT_TOKEN"
CHAT_ID = "CHAT_ID"

class Chat():
    def __init__(self, config_path = DEFAULT_CONFIG):
        self.api = 'https://api.telegram.org/bot'
        self.config_path = config_path
        self._token, self._client_id = self.parse_config(config_path)

        p = re_compile(r"^\d{1,10}:[A-z0-9-_]{35,35}$")
        if not p.match(self._token):
            raise Exception('Telegram token is invalid')

        p = re_compile(r"^-?\d{7,13}$")
        if not p.match(self._client_id):
            raise Exception('Telegram client_id is invalid')

        #print('Telegram configure with for client "' + client_id + '" with token "' + token + '"')

    def parse_config(self, config_path):
        with open(config_path) as f:
            config = json.load(f)
            if CHAT_TOKEN in config.keys() and CHAT_ID in config.keys():
                return config[CHAT_TOKEN], config[CHAT_ID]
        return "",""

    def send(self, message='') -> str:
        try:
            escaped_message = message.translate(message.maketrans({"*":  r"\*"}))
            payload = self.api + self._token + '/sendMessage?chat_id=' + self._client_id + '&parse_mode=html&text=' + escaped_message
            resp = get(payload)

            if resp.status_code != 200:
                return ''

            resp.raise_for_status()
            json = resp.json()

        except ConnectionError as err:
            print(err)
            return ''

        except exceptions.HTTPError as err:
            print(err)
            return ''

        except Timeout as err:
            print(err)
            return ''

        return json
