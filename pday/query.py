'''
Creates an object to refresh the auth token for
and create a session to access data.
'''


import json
from json import JSONDecodeError
from pathlib import Path

from requests import Response, Session


class PlandayQuery(object):

    def __init__(self, auth_dir: Path) -> None:
        '''
        Instantiate query object for running queries.
        Authenticates and prints a response status code.

        :param auth_dir: location of token.json (with Planday client_id and
                         refresh_token) and access_token.json (generated
                         by handshake)
        '''
        self._auth_dir = auth_dir
        self._authenticate()
        self._check_response()

    def _authenticate(self) -> None:
        '''
        Swap refresh token for access token.
        '''
        refresh_token_path = self._auth_dir / "refresh_token.json"
        self._session = Session()

        with open(refresh_token_path) as creds:
            auth_info = json.load(creds)
            self._token_url = auth_info['token_url']
            self._test_url = auth_info['test_url']
            self._params = auth_info['params']
            self._planday_client_id = auth_info['params']['client_id']

        # POST call for access token
        self._new_token = self._session.post(
            url=self._token_url,
            data=self._params
        ).json()

        # Write the access token
        with open(
                  self._auth_dir / "access_token.json", 'w'
                  ) as access_creds:
            json.dump(
                self._new_token,
                access_creds,
                ensure_ascii=False,
                indent=4
            )

        # New token and headers
        self._access_token = self._new_token['access_token']
        self._access_headers = {
            'Authorization': 'Bearer ' + self._new_token['access_token'],
            'X-ClientId': self._planday_client_id
        }

    def _check_response(self) -> None:
        '''
        Check that the API call worked.
        '''
        test_response = self._session.get(
            url=self._test_url,
            headers=self._access_headers
        )
        if test_response.status_code != 200:
            print('There was an authentication problem')
        else:
            print('PlandayClient: Authentication okay.')

    def get_response(self, url: str, params=None) -> Response:
        response = self._session.get(
            url,
            headers=self._access_headers,
            params=params
        )

        status_code = response.status_code
        if status_code in [400, 401]:
            self._authenticate()

        return response

    def query(self, url: str, limit=0):
        response = self.get_response(url, params={'Limit': limit})
        raw_response_data = response.json()['data']
        return raw_response_data

    def get_employees(self):
        '''
        Retrieve all employees

        :rtype: list
        :return: list of employees
        '''
        return sorted(
            self.query(
                'https://openapi.planday.com/hr/v1/employees'
            ),
            key=lambda x: x.get("id")
        )

    def get_departments(self):
        '''
        Retrieve all departments

        :rtype: list
        :return: list of departments
        '''
        return sorted(
            self.query(
                'https://openapi.planday.com/hr/v1/departments'
            ),
            key=lambda x: x.get("id")
        )

    def get_employee_groups(self):
        '''
        Retrieve all employee groups

        :rtype: list
        :return: list of employee groups
        '''
        return sorted(
            self.query(
                'https://openapi.planday.com/hr/v1/employeegroups'
            ),
            key=lambda x: x.get("id")
        )

    def get_shift_types(self):
        '''
        Retrieve shift types

        :rtype: list
        :return: list of employee shift types
        '''
        return sorted(
            self.query(
                'https://openapi.planday.com/scheduling/v1/shifttypes'
            ),
            key=lambda x: x.get("id")
        )

    def get_all_shifts(self):
        '''
        Retrieve all shifts

        :rtype: list
        :return: list of employee shifts
        '''
        return sorted(
            self.query(
                'https://openapi.planday.com/scheduling/v1/shifts'
            ),
            key=lambda x: x.get("date")
        )

    def get_account_types(self):
        '''
        Retrieve account types

        :rtype: list:
        :return: list of account types
        '''
        return sorted(
            self.query(
                'https://openapi.planday.com/absence/v1/accounttypes'
            ),
            key=lambda x: x.get("id")
        )

    def get_absence_requests(self):
        '''
        Retrieve account types

        :rtype: list:
        :return: list of account types
        '''
        return sorted(
            self.query(
                'https://openapi.planday.com/absence/v1/absencerequests'
            ),
            key=lambda x: x.get("id")
        )
