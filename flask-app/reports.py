import pandas as pd
import json
import re

# df = ReportsQuery().get_monthly_report(only_full_report=True, no_save=True)
df = pd.read_pickle('temp.pkl')
# df = pd.read_pickle('./flask-app/temp.pkl')


def make_json(df):
    df.fillna('', inplace=True)
    df_dict = df.T.to_dict(orient='index')
    months = {k for k in df_dict.keys()}
    names = {k[0] for k in df_dict['December'].keys()}
    data_fields = {k[1] for k in df_dict['December'].keys()}
    new_dict = {}
    for name in names:
        new_dict[name] = {'employeeName': name}
        for data in data_fields:
            new_dict[name][data] = {}
            for month in months:
                # if month == 'January':
                new_dict[name][data][month] = df_dict[month][(name, data)]
                # new_dict[name][data].append(df_dict[month][(name, data)]
    return new_dict


reports = make_json(df)


# Handler for read (GET) employees
def read_all_reports():
    '''
    Responds to a request for /api/reports with complete list of people

    :return: json string of list of people
    '''

    return [reports[key] for key in sorted(reports.keys())]


def read_one_report(lname):
    # Get last names
    names_list = [re.sub(r'[\s\W]+', '_', k.split(maxsplit=1)[1]).lower() for k in reports.keys()]
    if lname in names_list:
        idx = names_list.index(lname)
    name_key = list(reports.keys())[idx]
    person = reports.get(name_key)
    return person
