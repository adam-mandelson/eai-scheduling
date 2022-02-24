#!/usr/bin/env python3

'''
Script to update all pday data.
'''

from pday.update import PDayUpdate
from pday.query import PDayQuery
from pday.data import Data
from pday.utils import auth_dir, data_dir
from time import gmtime, strftime


PDayUpdate(
    pday_obj=PDayQuery(
        auth_dir=auth_dir()),
    data_obj=Data(),
    data_dir=data_dir()
    ).update_all()

with open('./pday/last_update.txt', 'w') as f:
    f.write(strftime('%d %b %Y %H:%M +0000', gmtime()))
    f.close()
