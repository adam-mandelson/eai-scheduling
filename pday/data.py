'''
Creates a Data object to manipulate API calls
or output data in various formats.
'''

import json
from pathlib import Path
from typing import Callable

from pday.utils import json_to_listview


class Data(object):

    def __init__(self) -> None:
        '''
        Instantiate data object.
        '''

    @staticmethod
    def get(pday_query: Callable, params: str = None) -> None:
        '''
        Calls a query method from the PDayQuery object.

        :param pday_query: A query method on the PDayQuery object.
        :param params: Optional parameters like "Limit: 0".
        :returns: A list of dictionaries.
        '''
        if params:
            return pday_query(**params)
        else:
            return pday_query()

    @staticmethod
    def save_to_json(pday_query: Callable, data_dir: Path, title: str,
                     params: str = None) -> None:
        '''
        Calls a query method from the PdayQuery object.
        Saves the output to a json file.

        :param pday_query: A query method on the PDayQuery object.
        :param data_dir: Location to save pday json.
        :param title: Title of the json file.
        :param params: Optional parameters like "Limit: 0".
        '''
        if params:
            pday_json = pday_query(**params)
        else:
            pday_json = pday_query()
        json_path = data_dir / title
        with open(json_path, 'w') as json_file:
            json.dump(pday_json, json_file, indent=2, ensure_ascii=False)
        print(f'File "{title}" saved to {json_path}.')

    @staticmethod
    def save_to_sheets(pday_query: Callable, google_client, sheet_name: str,
                       params: str = None) -> None:
        '''
        Calls a query method from the PdayQuery object.
        Saves the output to Google Sheets.

        :param pday_query: A query method on the PDayQuery object.
        :param google_client: A Google Sheets object.
        :param sheet_name: Title of the Google sheet to populate.
        :param params: Optional parameters like "Limit: 0".
        '''
        if params:
            pday_json = pday_query(**params)
        else:
            pday_json = pday_query()
        pday_keys = pday_json[0].keys()
        list_view_data = json_to_listview(pday_json, pday_keys)
        google_client.update(range=sheet_name, values=list_view_data)
