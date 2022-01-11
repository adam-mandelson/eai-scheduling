#!/usr/bin/env python3


'''
Rebuilds shift_data.json to match employees (ids, names, etc),
departments, and absence accounts.

More info on the Planday api is available at
    https://openapi.planday.com
'''


import json
import time

from config import config
from planday_client import PlandayClient


eai_client = PlandayClient()

with open('shifts.json', 'w') as f:
    json.dump(
        {'last_updated': time.strftime('%X %x %Z')}, f,
        ensure_ascii=False, indent=4
    )


def get_shifts():
    try:
        params = config(section='shifts')
        url = 'https://openapi.planday.com/scheduling/v1/shifts'
        response = eai_client.session.get(
            url=url,
            headers=eai_client.new_headers,
            params=params
            ).json()

        with open('shifts.json', 'r+') as f:
            shift_data = json.load(f)
            shift_data.update({'shifts': response})
            f.seek(0)
            json.dump(shift_data, f, ensure_ascii=False, indent=4)

    except Exception as error:
        print(error)


def get_absences():
    try:
        params = config(section='shifts')
        url = 'https://openapi.planday.com/absence/v1/absencerequests'
        response = eai_client.session.get(
            url=url,
            headers=eai_client.new_headers,
            params=params
            ).json()

        with open('shifts.json', 'r+') as f:
            shift_data = json.load(f)
            shift_data.update({'absence_requests': response})
            f.seek(0)
            json.dump(shift_data, f, ensure_ascii=False, indent=4)

    except Exception as error:
        print(error)


if __name__ == '__main__':
    get_shifts()
    get_absences()
