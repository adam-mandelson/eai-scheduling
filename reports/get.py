#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime as dt

import pandas as pd

from pday.utils import data_dir, reports_dir
from reports.reports import ReportsQuery

DATA_PATH = data_dir()
REPORTS_DIR = reports_dir()


def parse_args():
    parser = argparse.ArgumentParser(
        description='This module generates monthly reports, '
                    'or an entire yearly report.',
        epilog='Outputs a python dictionary at the moment.')
    current_year_month = dt.strftime(dt.today(), '%Y %m')
    parser.add_argument('-id', '--input_date', type=str,
                        nargs='?',
                        help='the date to produce the report '
                        'for. please enter as "YYYY mm".')
    return parser.parse_args()


def load_df():
    df_dict = {}
    for file in os.listdir(DATA_PATH):
        file_path = DATA_PATH / file
        try:
            with open(file_path) as f:
                json_struct = json.load(f)
                df = pd.json_normalize(json_struct)
                df_name = file[:-5]
        except json.JSONDecodeError:
            with open(file_path) as f:
                df = pd.read_csv(f)
                df_name = file[:-4]
        df_dict[df_name] = df
    return df_dict


if __name__ == '__main__':
    args = parse_args()
    query_obj = ReportsQuery(df_dict=load_df())
    # Get monthly report
    monthly_report = query_obj.monthly_report()
    # For each name, export to individual csv and full staff csv
    for name in monthly_report.keys():
        file_path = name.replace(' ', '_').lower() + '.csv'
        df = monthly_report[name].iloc[1:, :]
        with open(REPORTS_DIR / file_path, 'w') as f:
            df.to_csv(f, line_terminator='\n')
        df_full = monthly_report[name]
        with open(REPORTS_DIR / 'full_report.csv', 'a') as f:
            df_full.to_csv(f, mode='a', header=False, line_terminator='\n')
