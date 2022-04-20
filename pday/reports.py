'''
Creates a ReportsQuery object that cleans and aggregates data.
'''

from datetime import datetime as dt
from multiprocessing.sharedctypes import Value
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from pday.data import Data
from pday.query import PDayQuery
from pday.update import PDayUpdate
from pday.utils import auth_dir, data_dir

DATA_PATH = data_dir()

pday_obj = PDayQuery(auth_dir=auth_dir())
data_obj = Data()
update_obj = PDayUpdate(pday_obj=pday_obj, data_obj=data_obj, data_dir=DATA_PATH)


class ReportsQuery(object):

    def __init__(self) -> None:
        '''
        Instantiatiate reports object.
        '''
        # Filter data by current year
        self._date_filters = [
                dt.now().year,
                dt.now().year + 1
            ]
        self._clean_and_merge()

    def _clean_and_merge(self) -> None:
        # Import JSON data
        df_all_shifts = update_obj.get_all_shifts()
        df_employees_list = update_obj.get_employees()
        df_shift_types = update_obj.get_shift_types()
        df_leave_accounts = update_obj.get_leave_accounts()

        # Clean df_all_shifts
        # Convert to DateTime if necessary
        if df_all_shifts['date'].dtypes.name != 'datetime64[ns]':
            df_all_shifts['date'] = pd.to_datetime(df_all_shifts['date'])
            df_all_shifts['startDateTime'] = pd.to_datetime(df_all_shifts['startDateTime'])
            df_all_shifts['endDateTime'] = pd.to_datetime(df_all_shifts['endDateTime'])
            df_all_shifts.loc[:, ('hours')] = df_all_shifts.loc[
                :, ('endDateTime')] - df_all_shifts.loc[:, ('startDateTime')]
        df_all_shifts = df_all_shifts[df_all_shifts['status'] != 'Open']

        # Clean employees_list
        try:
            df_employees_list['employeeName'] = df_employees_list['firstName'] + ' ' + df_employees_list['lastName']
            df_employees_list.drop(columns=['firstName', 'lastName'], inplace=True)
        except KeyError:
            pass
        df_employees_list = df_employees_list.rename(columns={'id': 'employeeId'})

        # Clean shift_types
        df_shift_types = df_shift_types.rename(columns={
            'id': 'shiftTypeId', 'name': 'shiftTypeName'
        })[df_shift_types['isActive'] == True]

        # Clean leave_accounts
        try:
            df_leave_accounts['employeeName'] = df_leave_accounts['First name'] + ' ' + df_leave_accounts['Last name']
        except KeyError:
            pass
        df_leave_accounts = df_leave_accounts.rename(columns={
            'Balance at period start': 'balance'
            })

        # Merge datasets
        df_merged = df_all_shifts.merge(
            df_employees_list[['employeeId', 'employeeName']],
            how='left', on='employeeId'
            )
        df_merged = df_merged.merge(
            df_shift_types[['shiftTypeId', 'shiftTypeName']],
            how='left', on='shiftTypeId'
            )
        self._merged_dataset = df_merged
        self._full_df = pd.DataFrame(df_employees_list['employeeName'])

    def _merge_reports(self, df: pd.DataFrame) -> None:
        self._report_df = self._report_df.merge(
            df, how='left', on='employeeName')

    def get_sick_days(self, df: pd.DataFrame):
        '''
        Return the number of sick days used per month

        :param df: TODO: add
        '''
        # Filter by sick days
        df = df[df['shiftTypeName'] == 'Sick leave']
        df = df.groupby(['employeeName']).count()['id']
        df = df.rename('sick_leave')
        self._merge_reports(df)

    def get_annual_leave_used(self, df: pd.DataFrame):
        df = df[df['shiftTypeName'] == 'Annual Leave']
        df = df.groupby(['employeeName']).count()['id']
        df = df.rename('annual_leave')
        self._merge_reports(df)
        # TODO: Compare these numbers against shifts

    def get_parental_leave_used(self, df: pd.DataFrame):
        df = df[df['shiftTypeName'] == 'Parental Leave']
        df = df.groupby(['employeeName']).count()['id']
        df = df.rename('parental_leave')
        self._merge_reports(df)

    def get_hours_worked(self, df: pd.DataFrame):
        df = df[
            (df['shiftTypeName'] != 'HOLIDAY') &
            (df['shiftTypeName'] != 'WORKED HOLIDAY') &
            (df['shiftTypeName'] != 'Sick leave') &
            (df['shiftTypeName'] != 'Weekend / Evening Supplement') &
            (df['shiftTypeName'] != 'Annual Leave')
            ]
        df = df.groupby(['employeeName'])['hours'].agg('sum')
        hours = df.apply(lambda x: x.components.hours)
        hours += df.apply(lambda x: x.components.days * 24)
        df = hours.rename('hours_worked')
        self._merge_reports(df)

    def get_hours_counted(self, df: pd.DataFrame):
        df = df.groupby(['employeeName'])['hours'].agg('sum')
        hours = df.apply(lambda x: x.components.hours)
        hours += df.apply(lambda x: x.components.days * 24)
        df = hours.rename('hours_counted')
        self._merge_reports(df)

    def get_shifts_worked(self, df: pd.DataFrame):
        df = df[
            (df['shiftTypeName'] != 'HOLIDAY') &
            (df['shiftTypeName'] != 'WORKED HOLIDAY') &
            (df['shiftTypeName'] != 'Sick leave') &
            (df['shiftTypeName'] != 'Weekend / Evening Supplement') &
            (df['shiftTypeName'] != 'Annual Leave')
            ]
        df = df.groupby(['employeeName']).count()['id']
        df = df.rename('shifts_worked')
        self._merge_reports(df)

    # TODO: Is shifts counted necessary?
    # def get_shifts_counted(self, df: pd.DataFrame):
    #     df = df.groupby(['employeeName']).count()['id']
    #     df = df.rename('shifts_counted')
    #     self._merge_reports(df)

    def get_shifts_wfh(self, df: pd.DataFrame):
        df = df[df['shiftTypeName'].str.contains('WFH', na=False)]
        df = df.groupby(['employeeName']).count()['id']
        df = df.rename('shifts_wfh')
        self._merge_reports(df)

    def compile_data(self, monthly_data: pd.DataFrame):
        employeeName = monthly_data['employeeName'].values.tolist()[0]
        self._report_df = self._full_df.loc[self._full_df['employeeName'] == employeeName]
        self.get_sick_days(df=monthly_data)
        self.get_annual_leave_used(df=monthly_data)
        self.get_parental_leave_used(df=monthly_data)
        self.get_hours_worked(df=monthly_data)
        self.get_hours_counted(df=monthly_data)
        self.get_shifts_worked(df=monthly_data)
        # self.get_shifts_counted(df=monthly_data)
        self.get_shifts_wfh(df=monthly_data)
        return self._report_df

    def _multindex(self, df: pd.DataFrame) -> pd.DataFrame:
        name = pd.Series(df.loc['employeeName', 'January']).repeat(8).reset_index(drop=True)
        old_idx = df.index.values[1:]
        tuples = list(zip(name, old_idx))
        idx = pd.MultiIndex.from_tuples(tuples, names=['employeeName', 'data_types'])
        df = df.iloc[1:, :]
        df.set_index(idx, inplace=True)
        return df

    def get_monthly_report(self) -> Dict:
        names_list = self._full_df['employeeName'].values.tolist()
        full_df = pd.DataFrame()
        for name in names_list:
            df = self._merged_dataset
            df = df.loc[df['employeeName'] == name]
            employee_df = pd.DataFrame(columns=[
                'January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December'
                ])
            for month in employee_df.columns.tolist():
                # Create and populate monthly dataframe
                start = dt.strptime(str(dt.now().year) + ' ' + month, '%Y %B')
                end = start + pd.DateOffset(months=1)
                monthly_df = df[(df['date'] >= start) &
                                (df['date'] < end)]

                busdays = np.busday_count(dt.strftime(start, '%Y-%m'), (dt.strftime(end, '%Y-%m')))
                # Get data
                if monthly_df.shape[0] == 0:
                    employee_df.loc['employeeName', month] = name
                    employee_df.loc['sick_leave', month] = 0
                    employee_df.loc['annual_leave', month] = 0
                    employee_df.loc['parental_leave', month] = 0
                    employee_df.loc['hours_worked', month] = 0
                    employee_df.loc['hours_counted', month] = 0
                    employee_df.loc['shifts_worked', month] = 0
                    # employee_df.loc['shifts_counted', month] = 0
                    employee_df.loc['shifts_wfh', month] = 0
                    employee_df.loc['hours_contracted', month] = busdays * 8
                else:
                    monthly_df = self.compile_data(monthly_data=monthly_df)

                    # Add expected days and hours
                    monthly_df['hours_contracted'] = busdays * 8

                    # Add data
                    employee_df[month] = monthly_df.T

            # Fillna with 0
            employee_df.fillna(0, inplace=True)
            # TODO: Get YTD

            # Add index level
            employee_df = self._multindex(employee_df)

            # Combine with full_report
            full_df = pd.concat([full_df, employee_df])
        return full_df
