#!/usr/bin/env python3

'''
Script to update all pday data.
'''

from time import gmtime, strftime

from pday.connect import connect
from pday.data import Data
from pday.db_update import DBUpdate
from pday.query import PDayQuery
from pday.reports import ReportsQuery
from pday.update import PDayUpdate
from pday.utils import auth_dir, data_dir

PDayUpdate(
    pday_obj=PDayQuery(
        auth_dir=auth_dir()),
    data_obj=Data(),
    data_dir=data_dir()
    ).update_all()

with open('./pday/last_update.txt', 'w') as f:
    f.write(strftime('%d %b %Y %H:%M +0000', gmtime()))
    f.close()

# Update database
df = ReportsQuery().get_monthly_report(no_save=True, only_full_report=True)
# pd.to_pickle(df, 'temp.pkl')
# df = pd.read_pickle('temp.pkl')
DBUpdate(data=df, db_connect=connect).add_reports()
