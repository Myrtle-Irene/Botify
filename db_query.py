import os, sqlite3

def get_sql(db=r'ln2sql/database/city.sql', 
    query=r'how many city there are in which the employee name is similar to aman ?',
    vocab=r'ln2sql/lang/english.csv'):
    os.system(r'''C:\Python27\python.exe ln2sql/ln2sql.py -d {} -l {} -j output.json -i "{}"'''.format(db, vocab, query))

def fetch(query=r"SELECT * FROM heroes", db=r'heroes3/units.sqlite'):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows

heroes3 = (r'E:\Torrents\Coding\11\botify\heroes3\units.sql', r'Name of units with Cost less than 100')

get_sql(*heroes3)
print('------------------------------------')
#get_sql()