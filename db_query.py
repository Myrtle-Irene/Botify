import os, sqlite3

def get_sql(db=r'ln2sql/database/city.sql', 
    query=r'how many city there are in which the employee name is similar to aman ?',
    vocab=r'ln2sql/lang/english.csv'):
    os.system(r'''C:\Python27\python.exe ln2sql/ln2sql.py -d {} -l {} -j output.json -i "{}"'''.format(db, vocab, query))


heroes3 = (r'E:\Torrents\Coding\11\botify\heroes3\units.sql', r'Name of units with Cost less than 100')
#get_sql(*heroes3)
#print('------------------------------------')
#get_sql()