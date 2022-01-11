#!/usr/bin/env python3


'''
Rebuilds definitions.json to match employees (ids, names, etc),
departments, and absence accounts.

More info on the Planday api is available at
    https://openapi.planday.com
'''


import json
import time

from config import config
from planday_client import PlandayClient


eai_client = PlandayClient()

with open('definitions.json', 'w') as f:
    json.dump(
        {'last_updated': time.strftime('%X %x %Z')}, f,
        ensure_ascii=False, indent=4
    )


def get_employees():
    try:
        params = config()
        url = 'https://openapi.planday.com/hr/v1/employees'
        response = eai_client.session.get(
            url=url,
            headers=eai_client.new_headers,
            params=params
            ).json()

        with open('definitions.json', 'r+') as f:
            definitions = json.load(f)
            definitions.update({'employee_list': response})
            f.seek(0)
            json.dump(definitions, f, ensure_ascii=False, indent=4)

    except Exception as error:
        print(error)


def get_departments():
    try:
        params = config(section='department_ids')
        url = 'https://openapi.planday.com/hr/v1/departments'
        response = eai_client.session.get(
            url=url,
            headers=eai_client.new_headers,
            params=params
        ).json()

        with open('definitions.json', 'r+') as f:
            definitions = json.load(f)
            definitions.update({'department_list': response})
            f.seek(0)
            json.dump(definitions, f, ensure_ascii=False, indent=4)

    except Exception as error:
        print(error)


def get_employee_groups():
    try:
        params = config(section='employee_groups')
        url = 'https://openapi.planday.com/hr/v1/employeegroups'
        response = eai_client.session.get(
            url=url,
            headers=eai_client.new_headers,
            params=params
        ).json()

        with open('definitions.json', 'r+') as f:
            definitions = json.load(f)
            definitions.update({'employee_groups_list': response})
            f.seek(0)
            json.dump(definitions, f, ensure_ascii=False, indent=4)

    except Exception as error:
        print(error)


def get_accounts():
    try:
        params = config(section='absence_accounts')
        url = 'https://openapi.planday.com/absence/v1/accounts'
        response = eai_client.session.get(
            url=url,
            headers=eai_client.new_headers,
            params=params
        ).json()

        with open('definitions.json', 'r+') as f:
            definitions = json.load(f)
            definitions.update({'absence_accounts': response})
            f.seek(0)
            json.dump(definitions, f, ensure_ascii=False, indent=4)

    except Exception as error:
        print(error)


if __name__ == '__main__':
    get_employees()
    get_departments()
    get_employee_groups()
    get_accounts()
