#!/usr/bin/env python3


'''
Creates a class object to refresh the auth token for Planday
and create a session to access data.

More info on the Planday api is available at
    https://openapi.planday.com
'''


import json
import os

import requests

from config import config


class PlandayClient(object):

    config_dir = './config'

    token_url = config(section='planday_token')['token_url']
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def __init__(self):

        self.load_token()

        self.session = requests.Session()

        self.access_token()

        self.new_headers = {
            'X-ClientId': self.params['client_id'],
            'Authorization': 'Bearer ' + self.new_token['access_token']
        }

    def load_token(self):
        self.params = config(section='access_token')

    def access_token(self):
        self.new_token = self.session.post(
            url=self.token_url,
            headers=self.headers,
            data=self.params
        ).json()

        with open(os.path.join(
                  self.config_dir, 'planday_token.json'), 'w') as f:
            json.dump(self.new_token, f, ensure_ascii=False, indent=4)
