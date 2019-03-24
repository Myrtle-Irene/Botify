import os, sqlite3

def get_reply(db=r'heroes3\units.sql', 
    query=r'Name of units with Cost less than 100', 
    database=r'heroes3\units.sqlite',
    vocab=r'ln2sql/lang/english.csv'):
    os.system(r"""C:\Python27\python.exe ln2sql/ln2sql.py -d {} -l {} -j output.json -i "{}" -s {}""".format(db, vocab, query, database))
    reply = []
    with open('reply.txt', 'r') as rf:
        reply.append(str(rf.read()))
    return reply[0]