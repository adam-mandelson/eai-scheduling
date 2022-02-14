'''
Creates a Data object to manipulate scheduling data.
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
    def get(planday_query: Callable, params: str = None) -> None:
        '''
        Calls a query method from the PlandayQuery object.

        :param planday_query: A query method on the PlandayQuery object.
        :param params: Optional parameters like "Limit: 0".
        :returns: A list of dictionaries.
        '''
        if params:
            return planday_query(**params)
        else:
            return planday_query()

    @staticmethod
    def save_to_json(planday_query: Callable, data_dir: Path, title: str,
                     params: str = None) -> None:
        '''
        Calls a query method from the PlandayQuery object.
        Saves the output to a json file.

        :param planday_query: A query method on the PlandayQuery object.
        :param data_dir: Location to save Planday json.
        :param title: Title of the json file.
        :param params: Optional parameters like "Limit: 0".
        '''
        if params:
            planday_json = planday_query(**params)
        else:
            planday_json = planday_query()
        json_path = data_dir / title
        with open(json_path, 'w') as json_file:
            json.dump(planday_json, json_file, indent=2, ensure_ascii=False)
        print(f'File "{title}" saved to {json_path}.')

    @staticmethod
    def save_to_sheets(planday_query: Callable, google_client, sheet_name: str,
                       params: str = None) -> None:
        '''
        Calls a query method from the PlandayQuery object.
        Saves the output to Goolge Sheets.

        :param planday_query: A query method on the PlandayQuery object.
        :param google_client: A Google Sheets object.
        :param sheet_name: Title of the Google sheet to populate.
        :param params: Optional parameters like "Limit: 0".
        '''
        if params:
            planday_json = planday_query(**params)
        else:
            planday_json = planday_query()
        planday_keys = planday_json[0].keys()
        list_view_data = json_to_listview(planday_json, planday_keys)
        google_client.update(range=sheet_name, values=list_view_data)
