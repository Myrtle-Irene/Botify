import os, sqlite3

def get_reply(db=r'ln2sql/database/city.sql', 
    query=r'how many city there are in which the employee name is similar to aman ?', 
    database=r'E:\Torrents\Coding\11\botify\heroes3\units.sqlite',
    vocab=r'ln2sql/lang/english.csv'):
    return os.system(r'''C:\Python27\python.exe ln2sql/ln2sql.py -d {} -l {} -j output.json -i "{}" -s {}'''.format(db, vocab, query, database))


heroes3 = (r'E:\Torrents\Coding\11\botify\heroes3\units.sql', r'Name of units with Cost less than 100',)
get_reply(*heroes3)
print('------------------------------------')
#get_reply()
