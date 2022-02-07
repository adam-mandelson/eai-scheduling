'''
Creates an object to access Google Sheets.

More info on the Google Sheets API is available at:
    https://developers.google.com/sheets/api
'''


import json
from pathlib import Path
from time import gmtime, strftime

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class SheetsClient(object):

    def __init__(self, auth_dir: Path) -> None:
        '''
        Instantiatiate Sheets object for running queries or inserting info

        :param auth_dir: location of the service_account.json file.
        '''
        self._auth_dir = auth_dir
        sheet_id_path = self._auth_dir / 'sheets.json'
        with open(sheet_id_path) as sheets:
            sheet_id = json.load(sheets)['sheet_id']
        self._sheet_id = sheet_id
        self._check_service()

    def _authenticate(self) -> None:
        '''
        Authenticate with service account.
        '''
        service_account_path = self._auth_dir / "service_account.json"
        self._creds = Credentials.from_service_account_file(
            service_account_path
            )
        self._service = build('sheets', 'v4', credentials=self._creds)

    def _get_sheet(self):
        '''
        Get a sheet object.
        '''
        self._authenticate()
        return self._service.spreadsheets()

    def _check_time(self, log_type: str) -> list[list[str]]:
        '''
        Return time for logs.

        :param log_type: Info for the "Notes" column to show what
                         kind of service was logged.
        :returns: 2-D list with the time for entry into google sheets.
        '''
        log_time = [
            [log_type,
             strftime('%d %b %Y %H:%M +0000', gmtime())]
        ]
        return log_time

    def _log(self, log_type: str) -> None:
        '''
        Insert a log on the Logs sheet

        :param log_type: Info for the "Notes" column to show what kind of
                         service was logged. Passed to the _get_check_time()
                         function.
        '''
        sheet = self._get_sheet()
        range_ = 'logs!A:Z'
        value_ = self._check_time(log_type=log_type)
        sheet.values().append(
            spreadsheetId=self._sheet_id,
            range=range_,
            body={
                "majorDimension": "ROWS",
                "values": value_
            },
            valueInputOption="USER_ENTERED"
        ).execute()
        print(f'\nAdded record to logs at {value_[0][1]}')

    def append(self, range: str, values) -> None:
        '''
        Add values to a spreadsheet after the last data.

        :param range: The sheet and range to enter the data into.
        :param values: The values to be entered into the spreadsheet,
                       in a two-dimensional list. Most functions will
                       take care of this.
        '''
        sheet_ = self._get_sheet()
        range_ = range
        values_ = values
        # headers
        sheet_.values().append(
            spreadsheetId=self._sheet_id,
            range=range_,
            body={
                "majorDimension": "ROWS",
                "values": values_
            },
            valueInputOption="USER_ENTERED"
        ).execute()
        self._log(f'Appended values at {range}')
        print(f'Appended values at {range}')

    def update(self, range: str, values) -> None:
        '''
        Add values to a spreadsheet by overwriting existing values.

        :param range: The sheet and range to enter the data into.
        :param values: The values to be entered into the spreadsheet,
                       in a two-dimensional list. Most functions will
                       take care of this.
        '''
        sheet_ = self._get_sheet()
        range_ = range
        values_ = values
        # headers
        sheet_.values().update(
            spreadsheetId=self._sheet_id,
            range=range_,
            body={
                "majorDimension": "ROWS",
                "values": values_
            },
            valueInputOption="USER_ENTERED"
        ).execute()
        self._log(f'Updated values at {range}')
        print(f'Updated values at {range}')

    def _check_service(self) -> None:
        '''
        Check that sheets service is working and updates home page with log.

        Runs every time the SheetsClient is instantiated.
        '''
        sheet = self._get_sheet()
        test_result = sheet.values().get(
            spreadsheetId=self._sheet_id,
            range='logs!A1').execute()
        test_value = test_result.get('values', [])
        print(test_value[0][0])
        # Insert time into logs page to show page was checked
        self._log(log_type='Service_check')
