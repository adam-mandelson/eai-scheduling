'''
Creates an object to update and backup scheduling data.

More info on the API that's accessed here is available
on the relevant Google Sheet.
'''


import json
from pathlib import Path

import pandas as pd


class PDayUpdate(object):

    def __init__(self, pday_obj, data_obj, data_dir: Path, google_obj=None) -> None:
        '''
        Instantiates object.

        :param pday_obj: The PdayQuery object.
        :param data_obj: The Data object.
        :param data_dir: The directory to save data to.
        :param google_obj: An optional Google Sheets object. If None then
                           JSON data will only be saved to the data_dir.
        '''
        self._pday_obj = pday_obj
        self._google_obj = google_obj
        self._data_obj = data_obj
        self._data_dir = data_dir

    def _return_dataframe(self, file_name: str) -> pd.DataFrame:
        '''
        A function to save the data in memory to a Pandas DataFrame
        for further manipulation.

        :returns: A Pandas DataFrame
        '''
        file_path = self._data_dir / file_name
        try:
            with open(file_path) as f:
                json_struct = json.load(f)
                df = pd.json_normalize(json_struct)
                return df
        except Exception as err:
            print(err)

    def get_absence_accounts(self, update_sheets=False) -> pd.DataFrame:
        '''
        A function to save data to a JSON file, and return a Pandas DataFrame
        in memory for further use.

        :param update_sheets: True if Google Sheets should be updated.
        :returns: A Pandas DataFrame
        '''
        _file_name = 'absence_accounts.json'
        query = self._pday_obj.get_absence_accounts
        self._data_obj.save_to_json(
            pday_query=query,
            data_dir=self._data_dir,
            title=_file_name
        )
        if update_sheets:
            self._data_obj.save_to_sheets(
                pday_query=query,
                google_client=self._google_obj,
                sheet_name='absence_accounts'
            )
        df = self._return_dataframe(file_name=_file_name)
        return df

    def get_absence_requests(self, update_sheets=False) -> pd.DataFrame:
        '''
        A function to save data to a JSON file, and return a Pandas DataFrame
        in memory for further use.

        :param update_sheets: True if Google Sheets should be updated.
        :returns: A Pandas DataFrame
        '''        
        _file_name = 'absence_requests.json'
        query = self._pday_obj.get_absence_requests
        self._data_obj.save_to_json(
            pday_query=query,
            data_dir=self._data_dir,
            title=_file_name
        )
        if update_sheets:
            self._data_obj.save_to_sheets(
                pday_query=query,
                google_client=self._google_obj,
                sheet_name='absence_requests'
            )
        df = self._return_dataframe(file_name=_file_name)
        return df

    def get_account_types(self, update_sheets=False) -> pd.DataFrame:
        '''
        A function to save data to a JSON file, and return a Pandas DataFrame
        in memory for further use.

        :param update_sheets: True if Google Sheets should be updated.
        :returns: A Pandas DataFrame
        '''
        _file_name = 'account_types.json'
        query = self._pday_obj.get_account_types
        self._data_obj.save_to_json(
            pday_query=query,
            data_dir=self._data_dir,
            title=_file_name
        )
        if update_sheets:
            self._data_obj.save_to_sheets(
                pday_query=query,
                google_client=self._google_obj,
                sheet_name='account_types'
            )
        df = self._return_dataframe(file_name=_file_name)
        return df

    def get_all_shifts(self, update_sheets=False) -> pd.DataFrame:
        '''
        A function to save data to a JSON file, and return a Pandas DataFrame
        in memory for further use.

        :param update_sheets: True if Google Sheets should be updated.
        :returns: A Pandas DataFrame
        '''
        _file_name = 'all_shifts.json'
        query = self._pday_obj.get_all_shifts
        self._data_obj.save_to_json(
            pday_query=query,
            data_dir=self._data_dir,
            title=_file_name
        )
        if update_sheets:
            self._data_obj.save_to_sheets(
                pday_query=query,
                google_client=self._google_obj,
                sheet_name='all_shifts'
            )
        df = self._return_dataframe(file_name=_file_name)
        return df

    def get_departments(self, update_sheets=False) -> pd.DataFrame:
        '''
        A function to save data to a JSON file, and return a Pandas DataFrame
        in memory for further use.

        :param update_sheets: True if Google Sheets should be updated.
        :returns: A Pandas DataFrame
        '''
        _file_name = 'departments_list.json'
        query = self._pday_obj.get_departments
        self._data_obj.save_to_json(
            pday_query=query,
            data_dir=self._data_dir,
            title=_file_name
        )
        if update_sheets:
            self._data_obj.save_to_sheets(
                pday_query=query,
                google_client=self._google_obj,
                sheet_name='departments_list'
            )
        df = self._return_dataframe(file_name=_file_name)
        return df

    def get_employee_groups(self, update_sheets=False) -> pd.DataFrame:
        '''
        A function to save data to a JSON file, and return a Pandas DataFrame
        in memory for further use.

        :param update_sheets: True if Google Sheets should be updated.
        :returns: A Pandas DataFrame
        '''
        _file_name = 'employee_groups.json'
        query = self._pday_obj.get_employee_groups
        self._data_obj.save_to_json(
            pday_query=query,
            data_dir=self._data_dir,
            title=_file_name
        )
        if update_sheets:
            self._data_obj.save_to_sheets(
                pday_query=query,
                google_client=self._google_obj,
                sheet_name='employee_groups'
            )
        df = self._return_dataframe(file_name=_file_name)
        return df

    def get_employees(self, update_sheets=False) -> pd.DataFrame:
        '''
        A function to save data to a JSON file, and return a Pandas DataFrame
        in memory for further use.

        :param update_sheets: True if Google Sheets should be updated.
        :returns: A Pandas DataFrame
        '''
        _file_name = 'employees_list.json'
        query = self._pday_obj.get_employees
        self._data_obj.save_to_json(
            pday_query=query,
            data_dir=self._data_dir,
            title=_file_name
        )
        if update_sheets:
            self._data_obj.save_to_sheets(
                pday_query=query,
                google_client=self._google_obj,
                sheet_name='employees_list'
            )
        df = self._return_dataframe(file_name=_file_name)
        return df

    def get_shift_types(self, update_sheets=False) -> pd.DataFrame:
        '''
        A function to save data to a JSON file, and return a Pandas DataFrame
        in memory for further use.

        :param update_sheets: True if Google Sheets should be updated.
        :returns: A Pandas DataFrame
        '''
        _file_name = 'shift_types.json'
        query = self._pday_obj.get_shift_types
        self._data_obj.save_to_json(
            pday_query=query,
            data_dir=self._data_dir,
            title=_file_name
        )
        if update_sheets:
            self._data_obj.save_to_sheets(
                pday_query=query,
                google_client=self._google_obj,
                sheet_name='shift_types'
            )
        df = self._return_dataframe(file_name=_file_name)
        return df

    def get_leave_accounts(self, update_sheets=False) -> pd.DataFrame:
        '''
        A function to save data to a JSON file, and return a Pandas DataFrame
        in memory for further use.

        :param update_sheets: True if Google Sheets should be updated.
        :returns: A Pandas DataFrame
        '''
        _file_name = 'leave_accounts.csv'
        with open(self._data_dir / _file_name) as f:
            df = pd.read_csv(f)
        return df

    def update_all(self, update_sheets=False) -> None:
        '''
        A function to update all data and save locally.

        :param update_sheets: True if Google Sheets should be updated.
        '''        
        self.get_absence_accounts(update_sheets=update_sheets)
        self.get_absence_requests(update_sheets=update_sheets)
        self.get_account_types(update_sheets=update_sheets)
        self.get_all_shifts(update_sheets=update_sheets)
        self.get_departments(update_sheets=update_sheets)
        self.get_employee_groups(update_sheets=update_sheets)
        self.get_employees(update_sheets=update_sheets)
        self.get_shift_types(update_sheets=update_sheets)
