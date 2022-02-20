'''
Creates a ReportsQuery object that cleans 
'''

from datetime import datetime as dt
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from pday.data import Data
from pday.query import PDayQuery
from pday.update import PDayUpdate
from pday.utils import auth_dir, data_dir, reports_dir

DATA_PATH = data_dir()
REPORTS_DIR = reports_dir()

pday_obj = PDayQuery(auth_dir=auth_dir())
data_obj = Data()
update_obj = PDayUpdate(pday_obj=pday_obj, data_obj=data_obj, data_dir=DATA_PATH)


class ReportsQuery(object):

    def __init__(self, reports_dir: Path = None, employeeName: str = None) -> None:
        self._reports_dir = reports_dir
        self._date_filters = [
                dt.strptime('2022', '%Y'),
                dt.strptime('2023', '%Y')
            ]
        _df_all_shifts = update_obj.get_all_shifts()
        _df_employees_list = update_obj.get_employees()
        _df_shift_types = update_obj.get_shift_types()
        _df_leave_accounts = update_obj.get_leave_accounts()
        self._clean_all_shifts(df=_df_all_shifts)
        self._clean_employees_list(df=_df_employees_list)
        self._clean_shift_types(df=_df_shift_types)
        self._clean_leave_accounts(df=_df_leave_accounts)
        self._merge_datasets()
        if employeeName:
            self._employeeName = employeeName
            self._merged_dataset = self._merged_dataset[
                self._merged_dataset['employeeName'] == employeeName
            ]
        else:
            self._employeeName = None
        self._report_df = pd.DataFrame(self._employees_list['employeeName'])

    def _clean_all_shifts(self, df: pd.DataFrame) -> None:
        if df['date'].dtypes.name != 'datetime64[ns]':
            df['date'] = pd.to_datetime(df['date'])
            df['startDateTime'] = pd.to_datetime(df['startDateTime'])
            df['endDateTime'] = pd.to_datetime(df['endDateTime'])
            df.loc[:, ('hours')] = df.loc[
                :, ('endDateTime')] - df.loc[:, ('startDateTime')]
        df = df[
            (df['date'] >= self._date_filters[0]) &
            (df['date'] < self._date_filters[1])
            ]
        self._all_shifts = df[df['status'] != 'Open']

    def _clean_employees_list(self, df: pd.DataFrame) -> None:
        try:
            df['employeeName'] = df['firstName'] + ' ' + df['lastName']
            df.drop(columns=['firstName', 'lastName'], inplace=True)
        except KeyError:
            pass
        self._employees_list = df.rename(columns={'id': 'employeeId'})

    def _clean_shift_types(self, df: pd.DataFrame) -> None:
        self._shift_types = df.rename(columns={
            'id': 'shiftTypeId', 'name': 'shiftTypeName'
        })[df['isActive'] == True]

    def _clean_leave_accounts(self, df: pd.DataFrame) -> None:
        try:
            df['employeeName'] = df['First name'] + ' ' + df['Last name']
        except KeyError:
            pass
        self._leave_accounts = df.rename(columns={
            'Balance at period start': 'balance'
            })

    def _merge_datasets(self) -> None:
        shifts_df = self._all_shifts
        employees_df = self._employees_list
        shift_types_df = self._shift_types
        df = shifts_df.merge(
            employees_df[['employeeId', 'employeeName']],
            how='left', on='employeeId'
            )
        df = df.merge(
            shift_types_df[['shiftTypeId', 'shiftTypeName']],
            how='left', on='shiftTypeId'
            )
        self._merged_dataset = df

    def _merge_report(self, df: pd.DataFrame) -> None:
        self._report_df = self._report_df.merge(
            df, how='left', on='employeeName')

    def get_sick_days(self, df: pd.DataFrame = None):
        if df is None:
            df = self._merged_dataset[
                self._merged_dataset['shiftTypeName'] == 'Sick leave'
            ]
        else:
            df = df[df['shiftTypeName'] == 'Sick leave']
        if self._employeeName:
            dates = df['date'].dt.strftime('%Y-%m-%d').tolist()
            print(f'\n+++ Sick Days for {self._employeeName} +++')
            print(f'Number of shifts: {df.shape[0]}.')
            print(f'Dates of Sick Days: {dates}.')
            self._merge_report(df)
            return df
        else:
            df = df.groupby(['employeeName']).count()['id']
            df = df.rename('sick_leave')
            self._merge_report(df)

    def get_annual_leave_used(self, df: pd.DataFrame = None):
        if df is None:
            df = self._merged_dataset[
                self._merged_dataset['shiftTypeName'] == 'Annual Leave'
            ]
        else:
            df = df[df['shiftTypeName'] == 'Annual Leave']
        if self._employeeName:
            dates = df['date'].dt.strftime('%Y-%m-%d').tolist()
            print(f'\n+++ Annual Leave for {self._employeeName} +++')
            print(f'Number of days: {df.shape[0]}.')
            print(f'Dates of Annual Leave Days: {dates}.')
            self._merge_report(df)
            return df
        else:
            df = df.groupby(['employeeName']).count()['id']
            df = df.rename('annual_leave')
            self._merge_report(df)

    def get_hours_worked(self, df: pd.DataFrame = None):
        if df is None:
            df = self._merged_dataset
        df = df[
            (df['shiftTypeName'] != 'HOLIDAY') &
            (df['shiftTypeName'] != 'WORKED HOLIDAY') &
            (df['shiftTypeName'] != 'Sick leave') &
            (df['shiftTypeName'] != 'Weekend / Evening Supplement') &
            (df['shiftTypeName'] != 'Annual Leave')
            ]
        if self._employeeName:
            hours = df['hours'].sum().components.hours
            hours += df['hours'].sum().components.days * 24
            print(f'\n+++ Monthly Hours Worked for {self._employeeName} +++')
            print(f'Number of hours worked: {hours}.')
            self._merge_report(df)
            return df
        else:
            df = df.groupby(['employeeName'])['hours'].agg('sum')
            hours = df.apply(lambda x: x.components.hours)
            hours += df.apply(lambda x: x.components.days * 24)
            df = hours.rename('hours_worked')
            self._merge_report(df)

    def get_hours_counted(self, df: pd.DataFrame = None):
        if df is None:
            df = self._merged_dataset
        if self._employeeName:
            hours = df['hours'].sum().components.hours
            hours += df['hours'].sum().components.days * 24
            print(f'\n+++ Monthly Hours Counted for {self._employeeName} +++')
            print(f'Number of hours counted: {hours}.')
            self._merge_report(df)
            return df
        else:
            df = df.groupby(['employeeName'])['hours'].agg('sum')
            hours = df.apply(lambda x: x.components.hours)
            hours += df.apply(lambda x: x.components.days * 24)
            df = hours.rename('hours_counted')
            self._merge_report(df)

    def get_shifts_worked(self, df: pd.DataFrame = None):
        if df is None:
            df = self._merged_dataset
        df = df[
            (df['shiftTypeName'] != 'HOLIDAY') &
            (df['shiftTypeName'] != 'WORKED HOLIDAY') &
            (df['shiftTypeName'] != 'Sick leave') &
            (df['shiftTypeName'] != 'Weekend / Evening Supplement') &
            (df['shiftTypeName'] != 'Annual Leave')
            ]
        if self._employeeName:
            shifts = df.shape[0]
            print(f'\n+++ Monthly Shifts Worked for {self._employeeName} +++')
            print(f'Number of shifts worked: {shifts}.')
            self._merge_report(df)
            return df
        else:
            df = df.groupby(['employeeName']).count()['id']
            df = df.rename('shifts_worked')
            self._merge_report(df)

    def get_shifts_counted(self, df: pd.DataFrame = None):
        if df is None:
            df = self._merged_dataset
        if self._employeeName:
            shifts = df.shape[0]
            print(f'\n+++ Monthly Shifts Counted for {self._employeeName} +++')
            print(f'Number of shifts counted: {shifts}.')
            self._merge_report(df)
            return df
        else:
            df = df.groupby(['employeeName']).count()['id']
            df = df.rename('shifts_counted')
            self._merge_report(df)

    def get_shifts_wfh(self, df: pd.DataFrame = None):
        if df is None:
            df = self._merged_dataset
        df = df[df['shiftTypeName'].str.contains('WFH', na=False)]
        if self._employeeName:
            wfh = df.shape[0]
            print(f'\n+++ Monthly WFH Shifts for {self._employeeName} +++')
            print(f'Number of WFH shifts: {wfh}.')
            self._merge_report(df)
            return df
        else:
            df = df.groupby(['employeeName']).count()['id']
            df = df.rename('shifts_wfh')
            self._merge_report(df)

    def export_data(self, df: pd.DataFrame = None) -> pd.DataFrame:
        if df is None:
            df = self._merged_dataset
        else:
            name = df['employeeName'].iloc[:1]
            self._report_df = pd.DataFrame(name)
        self.get_sick_days(df=df)
        self.get_annual_leave_used(df=df)
        self.get_hours_worked(df=df)
        self.get_hours_counted(df=df)
        self.get_shifts_worked(df=df)
        self.get_shifts_counted(df=df)
        self.get_shifts_wfh(df=df)
        return self._report_df

    def _get_ytd_data(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            prev_month = dt.strftime(dt.now() - pd.DateOffset(months=1), '%B')
            df = df.loc[:, 'January':prev_month]
            df.loc[1:, ('ytd')] = df.loc[
                ~df.index.isin(['employeeName']), :].sum(axis=1)
            name_mask = self._leave_accounts['employeeName'] == df.loc[
                'employeeName', 'January'
                ]
            df.loc['hours_worked':'hours_counted', 'ytd_contracted'] = df.loc[
                'hours_contracted', ~df.columns.isin(['ytd'])
                ].sum()
            df.loc[:, ('under/over')] = df.loc[
                'hours_worked':'hours_counted', 'ytd'
                ] - df.loc['hours_worked':'hours_counted', 'ytd_contracted']
            df.loc['annual_leave', 'full_year_contracted'] = self._leave_accounts.loc[name_mask, 'balance'].values[0]
            work_days = (52*5) - 12 - df.loc['annual_leave', 'full_year_contracted']
            work_hours = work_days * 8
            df.loc['sick_leave', 'full_year_contracted'] = 10
            df.loc['shifts_worked':'shifts_counted', 'full_year_contracted'] = work_days
            df.loc['hours_worked':'hours_counted', 'full_year_contracted'] = work_hours
            return df.iloc[:, -4:]
        except IndexError as err:
            print(err)
            pass

    def _filter_monthly(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[
            (df['date'] >= self._date_filters[0]) &
            (df['date'] < self._date_filters[1])
            ]
        return self.export_data(df)

    def _multindex(self, df: pd.DataFrame) -> pd.DataFrame:
        name = pd.Series(df.loc['employeeName', 'January']).repeat(7).reset_index(drop=True)
        old_idx = df.index.values[1:-1]
        tuples = list(zip(name, old_idx))
        idx = pd.MultiIndex.from_tuples(tuples, names=['employeeName', 'data_types'])
        df = df.iloc[1:-1, :]
        df.set_index(idx, inplace=True)
        return df

    def get_monthly_report(self, only_full_report=False, no_save=False) -> Dict:
        names_list = self._report_df['employeeName'].values.tolist()
        # TODO: Temporary
        names_list = names_list[:-1]
        df_dict = {}
        full_df = pd.DataFrame()
        for name in names_list:
            print(f'\n+++ Working on {name}\'s report +++')
            df = self._merged_dataset
            df = df.loc[df['employeeName'] == name]
            employee_df = pd.DataFrame(columns=[
                'January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December'
                ])
            for month in employee_df.columns.tolist():
                start = dt.strptime(str(dt.now().year) + ' ' + month, '%Y %B')
                end = start + pd.DateOffset(months=1)
                busdays = np.busday_count(dt.strftime(start, '%Y-%m'), (dt.strftime(end, '%Y-%m')))
                self._date_filters = [start, end]
                month_df = self._filter_monthly(df=df)
                month_df['hours_contracted'] = busdays * 8
                try:
                    employee_df[month] = month_df.T
                except ValueError:
                    employee_df.loc['employeeName', month] = name
                    print('\n+++ WARNING +++')
                    print(f'{name.split()[0]}\'s report for the month of '
                          f'{month} is empty. Please check.')
                    pass
            employee_df.fillna(0, inplace=True)
            ytd_df = self._get_ytd_data(employee_df)
            employee_df = employee_df.join(ytd_df)
            # Add index level
            employee_df = self._multindex(employee_df)
            full_df = pd.concat([full_df, employee_df])
            df_dict[name] = employee_df.iloc[:-1, :]
            df_dict[name].fillna(0, inplace=True)
        if only_full_report & no_save:
            return full_df
        self._monthly_dict = df_dict
        if only_full_report:
            if no_save:
                return self._save_full_report(no_save=no_save)
        else:
            for name in df_dict.keys():
                self._save_indiv_report(name)
            self._save_full_report(no_save=no_save)
        return df_dict

    def _save_indiv_report(self, name: str) -> None:
        file_path = name.replace(' ', '_').lower() + '.csv'
        df = self._monthly_dict[name].iloc[1:, :]
        with open(self._reports_dir / file_path) as f:
            df.to_csv(f, line_terminator='\n')

    def _save_full_report(self, no_save=False):
        if no_save:
            df_dict = self._monthly_dict
            df = pd.DataFrame(columns=df_dict['Adam Mandelson'].columns)
            for name in df_dict.keys():
                df = df.append(df_dict[name])
            return df
        else:
            with open(self._reports_dir / 'full_report.csv', 'w') as f:
                df.to_csv(f, line_terminator='\n')
            return df
