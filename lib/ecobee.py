import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
import logging
import sys
import base64

def get_ecobee_pin(api_key):
    params = {'response_type': 'ecobeePin',
              'client_id': api_key,
              'scope': 'smartWrite'}
    response = requests.get('https://api.ecobee.com/authorize', params=params)
    return response.json(), response.status_code


def get_ecobee_access_token(api_key):
    while True:
        pin, _ = get_ecobee_pin(api_key)
        params = {'grant_type': 'ecobeePin',
                  'code': pin['code'],
                  'client_id': api_key}

        print('      Go to your Ecobee account, login, go to your "My Apps" and click on "Add Application". ')
        print('      When prompted, enter the following code: ' + pin['ecobeePin'])
        print('      After entering, click on "Validate". In the resulting dialog, click on "Add Application".')
        input('      Once you have done that, press ENTER')

        with requests.Session() as s:
            retry = Retry(total = 3,
                          read = 3,
                          connect = 3,
                          backoff_factor=5,
                          status_forcelist=(500, 502, 504, 401),
                          method_whitelist=frozenset(['GET','POST']))
            adapter = HTTPAdapter(max_retries=retry)
            s.mount('http://', adapter)
            s.mount('https://', adapter)
            s.params=params

            response = s.post('https://api.ecobee.com/token')
            token, code = response.json(), response.status_code
            if code == 200:
                break

    return base64.b64encode(response.json()['access_token'].encode('UTF-8')).decode('UTF-8') + \
           '-' + \
           base64.b64encode(response.json()['refresh_token'].encode('UTF-8')).decode('UTF-8')


def refresh_ecobee_token(config):
    tokens = config['Keys']['EcobeeTokens'].split('-')
    api_key = config['Keys']['EcobeeAPI']
    refresh_token = base64.b64decode(tokens[1].encode('UTF-8')).decode('UTF-8')
    data = { 'grant_type': 'refresh_token', 'code': refresh_token, 'client_id': api_key}
    response = requests.post('https://api.ecobee.com/token', data)
    if response.status_code == 200:
        keys = base64.b64encode(response.json()['access_token'].encode('UTF-8')).decode('UTF-8') + \
               '-' + \
               base64.b64encode(response.json()['refresh_token'].encode('UTF-8')).decode('UTF-8')
        config.set('Keys','EcobeeTokens', keys)
        config.write()
    else:
        logging.error("Failed to refresh ecobee token. Status code: %d, message: %s", response.status_code, response.json())
    return response.json()



def get_ecobee_temp(access_token):
    request_data = {'selection': { 'selectionType': 'registered', 'selectionMatch': '', 'includeRuntime': 'true',
                                   'includeEquipmentStatus': 'true'}}
    params = {'format': 'json',
              'body': json.dumps(request_data)
              }
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + base64.b64decode(access_token.encode('UTF-8')).decode('UTF-8')
               }
    try:
        return requests.get('https://api.ecobee.com/1/thermostat', headers=headers, params=params)
    except:
        logging.warning("Failed to retrieve Ecobee Temperature. Will retry later...")
        return None


def get_ecobee_temperature(config):
    tokens = config['Keys']['EcobeeTokens'].split('-')
    response = get_ecobee_temp(tokens[0])
    if response is None or response.status_code != 200:
        try:
            new_tokens = refresh_ecobee_token(config)
            response = get_ecobee_temp(new_tokens['access_token'])
        except:
            logging.exception("Failure to get ecobee temperature")
            return None, None
    try:
        return response.json(), response.status_code
    except:
        logging.exception("Failure in getting response JSON")
        if response is not None:
            logging.error(response.text)
        return None, None
