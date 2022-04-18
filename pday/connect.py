from io import StringIO

import psycopg2
import pandas as pd
from pday.config import config, psycopg2_exception
import json


def connect(table: str = 'pday', sql: str = None, data=None, has_json=False) -> None:
    conn = None
    try:
        params = config('database.ini')

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        with conn:
            cur = conn.cursor()

            cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
            cur.execute(sql)

        with conn:
            print('PostgreSQL database:')
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print(db_version)

        with conn:
            buffer = StringIO()
            # source['departments'] = source['departments'].apply(lambda x: ' '.join(str(i) for i in x))
            # source['employeeGroups'] = source['employeeGroups'].apply(lambda x: ' '.join(str(i) for i in x))
            if has_json:
                try:

                    for item in data:
                        data = [item[key] for key in item.keys()]
                        for i, v in enumerate(data):
                            if isinstance(v, dict):
                                data[i] = json.dumps(v)
                            elif isinstance(v, list):
                                data[i] = json.dumps(v)
                        insert_query = f'''INSERT INTO {table} VALUES (%s, %s, %s, %s, %s)'''
                        cur.execute(insert_query, tuple(data))
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as err:
                    psycopg2_exception(err)
            else:
                data.to_csv(buffer, header=False, index=True)
                buffer.seek(0)
                try:
                    cur.copy_from(buffer, table, sep=",")
                    cur.execute(f'SELECT COUNT(*) FROM {table}')
                    rows = cur.fetchone()
                    print(f"Data inserted into {table} successfully")
                    print(f"Inserted {rows} rows")
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as err:
                    psycopg2_exception(err)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        pass
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
