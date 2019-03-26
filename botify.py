import argparse, os, sys, sqlite3, shutil, requests, json
from pprint import pprint
from flask import Flask, request, jsonify

#specify this
bot_web_url = r"Your https url (bot's web endpoint)" 
python2_path = r'C:\Python27\python.exe'
#

bot_name, table_url, telegram_token, sql_file, sqlite_database, existing = None, None, None, None, None, None


def make_databases(sql_file, table_url, bot_directory, sqlite_database):
    os.system(r'sqlitebiter url "{}"'.format(table_url))
    shutil.move('out.sqlite', bot_directory)
    os.rename(os.path.join(bot_directory, 'out.sqlite'), sqlite_database)
    con = sqlite3.connect('{}'.format(sqlite_database))
    with open(sql_file, 'w') as f:
        for line in con.iterdump():
            f.write('{}\n'.format(line))
    print('Congrat! Databases ready.')

def get_reply(db, query, database, vocab=r'ln2sql/lang/english.csv'):
    os.system(r"""{} ln2sql/ln2sql.py -d {} -l {} -j output.json -i "{}" -s {}""".format(python2_path, db, vocab, query, database))
    reply = []
    with open('reply.txt', 'r') as rf:
        reply.append(str(rf.read()))
    return reply[0]
    
def print_help_message():
    print('Usage:')
    print('Specify "bot_web_url" in botify.py, then run program')
    print(r'"$python botify.py <bot name(only letters and digits)> <your web page> <telegram unique token>"')
    print(r'or "$python botify.py -e <bot name>"  to launch existing bot')
    print('Example: "python botify.py Heroes3bot http://heroes.thelazy.net/wiki/List_of_creatures 855401787:AAHjueP4Ih-MF5WjL0NW-ISoN28qK5Vw4B8"')

def bind_web_url():
    def get_url(method):
        return "https://api.telegram.org/bot{}/{}".format(telegram_token, method)
    r = requests.get(get_url("setWebhook"), data={"url": bot_web_url})
    r = requests.get(get_url("getWebhookInfo"))
    pprint(r.status_code)
    pprint(r.json())

def main():
    sys.argv = 'botify.py Heroes3bot http://heroes.thelazy.net/wiki/List_of_creatures \
    855401787:AAHjueP4Ih-MF5WjL0NW-ISoN28qK5Vw4B8'
    args=sys.argv.split()
    if (len(args) == 3) and args[1] == '-e':
        existing = True
        bot_name = args[2]
    elif (len(args) == 4):
        bot_name = args[1]
        table_url = args[2]
        telegram_token = args[3]
        existing = False
    elif args[1] == '-h' or 'h' or '-help' or 'help':
        print_help_message()
    else:
        print_help_message()
        sys.exit()
    if existing == (None or False) and ((table_url is None) or (bot_name is None) or (telegram_token is None)):
        print_help_message()
        sys.exit()
    
    tg_url = 'https://api.telegram.org/bot' + str(telegram_token) + '/'
    bot_directory = os.path.join(os.path.abspath(os.path.curdir), bot_name)
    os.mkdir(bot_directory)

    if existing == False:
        sql_file = os.path.join(bot_directory, bot_name + '.sql')
        sqlite_database = os.path.join(bot_directory, bot_name + '.sqlite')
        print(sqlite_database)
        make_databases(sql_file, table_url, bot_directory, sqlite_database)
        with open('{}/temp.json'.format(bot_directory), 'w') as df:
            vars = bot_name, table_url, telegram_token, sql_file, sqlite_database
            df.write(json.dumps(vars))
      
    if existing == True:
        with open('{}/temp.json'.format(bot_directory), 'r') as df:
            bot_name, table_url, telegram_token, sql_file, sqlite_database = json.loads(df.read())
    

    app = Flask(__name__)

    def send_message(chat_id, text='empty query'):
        url = tg_url + 'sendMessage'
        answer = {'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'}
        r = requests.post(url, json=answer)
        return r.json()

    @app.route('/', methods=['POST', 'GET'])
    def index():
        if request.method == 'POST':
            r = request.get_json()
            chat_id = r['message']['chat']['id']
            message = str(r['message']['text'])
            answer = get_reply(sql_file, message, sqlite_database)
            send_message(chat_id, answer)
        return 'Bot is online.'

    try:
        app.run()
        bind_web_url()
    except Exception as e:
        print(str(e))
      
if __name__ == '__main__':
    main()