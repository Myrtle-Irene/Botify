import os
import sqlite3

def make_db_from_table_url(url, file_path):
    os.system(r'sqlitebiter url "{}" -o {}'.format(url, file_path))

def get_db_schema_file(db_path, output_path):
    con = sqlite3.connect('{}'.format(db_path))

    with open(output_path, 'w') as f:
        for line in con.iterdump():
            f.write('{}\n'.format(line))