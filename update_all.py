#!/usr/bin/env python3

'''
Run this script to backup scheduling data to json (locally) and Google Sheets.

More info on the API that's accessed here is available
on the relevant Google Sheet.
'''


from pday.data import Data
from pday.query import PlandayQuery
from pday.sheets_client import SheetsClient
from pday.utils import auth_dir, data_dir


# Instantiate PlandayQuery and Google Sheets objects
planday_obj = PlandayQuery(auth_dir=auth_dir())
google_client = SheetsClient(auth_dir=auth_dir())
data_obj = Data()

# Get absence requests
absence_query = planday_obj.get_absence_requests
data_obj.save_to_json(
    planday_query=absence_query,
    data_dir=data_dir(),
    title='absence_requests.json'
)
data_obj.save_to_sheets(
    planday_query=absence_query,
    google_client=google_client,
    sheet_name='absence_requests'
)

# Get absence types
data_obj.save_to_json(
    planday_query=planday_obj.get_account_types,
    data_dir=data_dir(),
    title='account_types.json'
)
data_obj.save_to_sheets(
    planday_query=planday_obj.get_account_types,
    google_client=google_client,
    sheet_name='account_types'
)

# Get all shifts
data_obj.save_to_json(
    planday_query=planday_obj.get_all_shifts,
    data_dir=data_dir(),
    title='all_shifts.json'
)
data_obj.save_to_sheets(
    planday_query=planday_obj.get_all_shifts,
    google_client=google_client,
    sheet_name='all_shifts'
)

departments_query = planday_obj.get_departments
# Departments_list
data_obj.save_to_json(
    planday_query=departments_query,
    data_dir=data_dir(),
    title='departments_list.json'
)
data_obj.save_to_sheets(
    planday_query=departments_query,
    google_client=google_client,
    sheet_name='departments_list'
)

# Employee groups
data_obj.save_to_json(
    planday_query=planday_obj.get_employee_groups,
    data_dir=data_dir(),
    title='employee_groups.json'
)
data_obj.save_to_sheets(
    planday_query=planday_obj.get_employee_groups,
    google_client=google_client,
    sheet_name='employee_groups'
)

# Employees_list
data_obj.save_to_json(
    planday_query=planday_obj.get_employees,
    data_dir=data_dir(),
    title='employees_list.json'
)
data_obj.save_to_sheets(
    planday_query=planday_obj.get_employees,
    google_client=google_client,
    sheet_name='employees_list'
)

# Get shift types
data_obj.save_to_json(
    planday_query=planday_obj.get_shift_types,
    data_dir=data_dir(),
    title='shift_types.json'
)
data_obj.save_to_sheets(
    planday_query=planday_obj.get_shift_types,
    google_client=google_client,
    sheet_name='shift_types'
)
