'''
Creates an object to clean data and update database.
'''

import json
import os
from pathlib import Path

import pandas as pd

from pday.utils import data_dir

DATA_DIR = data_dir()


class DBUpdate(object):

    def __init__(self, data: pd.DataFrame = None, db_connect=None) -> None:
        '''
        Instantiate object

        :param data: Pandas DataFrame from a PDayUpdate object and a PDayQuery method.
        :param db_connect: DB connect function
        '''
        self._data = data
        self._connect = db_connect
        # self._clean()

    def _clean(self) -> None:
        '''
        Cleans data
        '''
        for file in os.listdir(DATA_DIR):
            with open(DATA_DIR / file) as f:
                json_struct = json.load(f)
                df = pd.json_normalize(json_struct)
            df.columns = df.columns.str.replace(r'[\s\W]+', '_', regex=True)
            table_str = 'pday_' + file[:-5]
            # Absence accounts
            if file == 'absence_accounts.json':
                df.drop(columns=['salaryCodeCompanyPaid'], inplace=True)
                sql = f'''CREATE TABLE {table_str}(
                    id int primary key,
                    employeeId int,
                    typeId int,
                    status varchar (50),
                    name varchar (50),
                    validityPeriod_start varchar (25),
                    validityPeriod_end varchar (25),
                    constraint fk_employee
                        FOREIGN KEY(employeeId)
                            REFERENCES pday_employees_list(id)
                            ON DELETE CASCADE,
                    constraint fk_type
                        FOREIGN KEY(typeId)
                            REFERENCES pday_account_types(id)
                            ON DELETE CASCADE
                    )'''
                self._connect(table=table_str, sql=sql, data=df)
            elif file == 'absence_requests.json':
                data = json_struct
                sql = f'''CREATE TABLE {table_str}(
                    id int primary key,
                    employeeId int,
                    absencePeriod jsonb,
                    status varchar (50),
                    requestedAccounts jsonb,
                    constraint fk_employee
                        FOREIGN KEY(employeeId)
                            REFERENCES pday_employees_list(id)
                            ON DELETE CASCADE
                    )'''
                self._connect(table=table_str, sql=sql, data=data, has_json=True)
            elif file == 'account_types.json':
                sql = f'''CREATE TABLE {table_str}(
                    id int primary key,
                    name varchar (50),
                    description varchar (50),
                    absenceType varchar (50),
                    isDeleted varchar (15),
                    employeeTypes varchar (10),
                    spendingUnit_type varchar (10),
                    startBalance_value varchar (10),
                    startBalance_unit_type varchar (10),
                    accruingRate_value varchar (10),
                    accruingRate_unit_type varchar (50)
                    )'''
                self._connect(table=table_str, sql=sql, data=df)

    def add_reports(self) -> None:
        '''
        Adds reports data to PostgreSQL database.
        '''
        df = self._data
        df = df.reset_index().melt(id_vars=['employeeName', 'data_types']).rename(columns={'variable': 'period'})
        df['value'].fillna(0, inplace=True)
        df['value'] = df['value'].astype(int)
        table_str = 'pday_reports'
        sql = f'''CREATE TABLE {table_str}(
            id int primary key,
            employeename varchar(75) not null,
            datatypes varchar(25) not null,
            period varchar(50) not null,
            value integer
            )'''
        self._connect(table=table_str, sql=sql, data=df)
