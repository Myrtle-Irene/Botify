import os

bot_name = "Heroes3bot"
bot_directory = os.path.join(os.path.abspath(os.path.curdir), bot_name)
sql_file = os.path.join(bot_directory, bot_name + '.sql')
sqlite_database = os.path.join(bot_directory, bot_name + '.sqlite')
python2_path = r'C:\Python27\python.exe'


def get_reply(db, query, database, vocab=r'ln2sql/lang/english.csv'):
    os.system(r"""{} ln2sql/ln2sql.py -d {} -l {} -j output.json -i "{}" -s {}""".format(python2_path, db, vocab, query, database))
    reply = []
    with open('reply.txt', 'r') as rf:
        reply.append(str(rf.read()))
    return reply[0]
    


query = 'Name of heroes with defense less than 3'
print(get_reply(sql_file, query, sqlite_database))