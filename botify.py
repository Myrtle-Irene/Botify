import argparse, os, sys, sqlite3, shutil, requests, json, getopt
from flask import Flask
from flask import request
from flask import jsonify
from pprint import pprint
from db_query import get_reply


bot_web_url = "<your-https-url>"
tg_url = 'https://api.telegram.org/bot' + telegram_token + '/'

def make_databases(table_url, bot_directory):
    os.system(r'sqlitebiter url "{}"'.format(table_url))
    shutil.move('out.sqlite', bot_directory)
    os.rename(os.path.join(bot_directory, 'out.sqlite'), sqlite_database)
    con = sqlite3.connect('{}'.format(sqlite_database))  
    with open(sql_file, 'w') as f:
        for line in con.iterdump():
            f.write('{}\n'.format(line))
    print('Congrat! Databases ready.')

def print_help_message():
    print('Usage:')
    print(r'"$python botify.py -u <your web page>  -n <bot name(only letters and digits)>  -t <telegram unique token>"')
    print(r'or "$python botify.py -e True"  to launch existing bot')

def bind_web_url():
    r = requests.get(get_url("setWebhook"), data={"url": bot_web_url})
    r = requests.get(get_url("getWebhookInfo"))
    pprint(r.status_code)
    pprint(r.json())

    def get_url(method):
        return "https://api.telegram.org/bot{}/{}".format(telegram_token, method)


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
    return '<h1>request: GET.\n bot is working.</h1>'


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:n:t:e:h:")
        bot_name, table_url, telegram_token, existing = None, None, None, False
    except getopt.GetoptError:
        print_help_message()
        sys.exit()

    for i in range(0, len(opts)):
        if opts[i][0] == "-u":
            table_url = opts[i][1]
        elif opts[i][0] == "-n":
            bot_name = opts[i][1]
        elif opts[i][0] == "-t":
            telegram_token = opts[i][1]
        elif opts[i][0] == "-e":
            existing = opts[i][1]
        else:
            print_help_message()
            sys.exit()

    if existing == (None or False) and ((table_url is None) or (bot_name is None) or (telegram_token is None)):
        print_help_message()
        sys.exit()
    
    bot_directory = os.path.join(os.path.abspath(os.path.curdir), bot_name)
    if existing == False:
        sql_file = os.path.join(bot_directory, bot_name + '.sql')
        sqlite_database = os.path.join(bot_directory, bot_name + '.sqlite')
        make_databases(table_url, bot_directory)
        bind_web_url()
        with open('{}/temp.json'.format(bot_directory), 'w') as df:
            vars = bot_name, table_url, telegram_token, sql_file, sqlite_database
            df.write(json.dumps(vars))
      
    if existing == True:
        with open('{}/temp.json'.format(bot_directory), 'r') as df:
            bot_name, table_url, telegram_token, sql_file, sqlite_database = json.loads(df.read())
        bind_web_url()

    try:
        app.run()
    except Exception as e:
        print(str(e))
    
if __name__ == '__main__':
    main()
