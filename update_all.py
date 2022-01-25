#!/usr/bin/env python3

'''
Run this script to backup scheduling data to json (locally) and Google Sheets.

More info on the API that's accessed here is available
on the relevant Google Sheet.
'''


from pathlib import Path
import os

from pday.data import Data
from pday.query import PlandayQuery
from pday.sheets_client import SheetsClient


def auth_dir() -> Path:
    '''
    Returns a Path object with the location of the config folder.
    '''
    return Path('config/')


def data_dir() -> Path:
    '''
    Returns a Path object with the location of the data folder.
    Makes a new one if it doesn't exist.
    '''
    if not os.path.exists('./data/'):
        os.makedirs('./data/')
    return Path('data/')


# Instantiate PlandayQuery and Google Sheets objects
planday_obj = PlandayQuery(auth_dir=auth_dir())
google_client = SheetsClient(auth_dir=auth_dir())

# Employees_list
Data.save_to_json(
    planday_query=planday_obj.get_employees,
    data_dir=data_dir(),
    title='employees_list.json'
)
Data.save_to_sheets(
    planday_query=planday_obj.get_employees,
    google_client=google_client,
    sheet_name='employees_list'
)

# Departments_list
Data.save_to_json(
    planday_query=planday_obj.get_departments,
    data_dir=data_dir(),
    title='departments_list.json'
)
Data.save_to_sheets(
    planday_query=planday_obj.get_departments,
    google_client=google_client,
    sheet_name='departments_list'
)

# Employee groups
Data.save_to_json(
    planday_query=planday_obj.get_employee_groups,
    data_dir=data_dir(),
    title='employee_groups.json'
)
Data.save_to_sheets(
    planday_query=planday_obj.get_employee_groups,
    google_client=google_client,
    sheet_name='employee_groups'
)

# Get shift types
Data.save_to_json(
    planday_query=planday_obj.get_shift_types,
    data_dir=data_dir(),
    title='shift_types.json'
)
Data.save_to_sheets(
    planday_query=planday_obj.get_shift_types,
    google_client=google_client,
    sheet_name='shift_types'
)

# Get all shifts
Data.save_to_json(
    planday_query=planday_obj.get_all_shifts,
    data_dir=data_dir(),
    title='all_shifts.json'
)
Data.save_to_sheets(
    planday_query=planday_obj.get_all_shifts,
    google_client=google_client,
    sheet_name='all_shifts'
)

# Get absence types
Data.save_to_json(
    planday_query=planday_obj.get_account_types,
    data_dir=data_dir(),
    title='account_types.json'
)
Data.save_to_sheets(
    planday_query=planday_obj.get_account_types,
    google_client=google_client,
    sheet_name='account_types'
)

# Get absence requests
Data.save_to_json(
    planday_query=planday_obj.get_absence_requests,
    data_dir=data_dir(),
    title='absence_requests.json'
)
Data.save_to_sheets(
    planday_query=planday_obj.get_absence_requests,
    google_client=google_client,
    sheet_name='absence_requests'
)
