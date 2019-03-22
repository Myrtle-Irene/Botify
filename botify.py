import argparse, os, sqlite3, requests, json, getopt
from flask import Flask
from flask import request
from flask import jsonify
from db_query import get_sql


def make_databases(table_url, bot_name):
    os.system(r'sqlitebiter url "{}" -o {}'.format(sqlite_database))
    con = sqlite3.connect('{}'.format(sqlite_database))  
    with open(sql_file, 'w') as f:
        for line in con.iterdump():
            f.write('{}\n'.format(line))

def print_help_message():
    print('\n')
    print('Usage:')
    print('\tpython botify.py -url <your web page>  -name <bot name>  -token <telegram unique token>')
    print('or')
    print('\tpython botify.py -existing <True>')
    print('to launch existing bot')



app = Flask(__name__)
def send_message(chat_id, text='empty query'):
    url = URL + 'sendMessage'
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
        message = r['message']['text']
        send_message(chat_id, answer)
    return '<h1>request: GET.\n bot is working.</h1>'



def main():
    """
    try:
        opts, args = getopt.getopt(argv,"url:name:token:existing:help:")
        bot_name = None
        table_url = None
        telegram_token = None
        for i in range(0, len(opts)):
            if opts[i][0] == "-url":
                table_url = opts[i][1]
            elif opts[i][0] == "-name":
                bot_name = opts[i][1]
            elif opts[i][0] == "-token":
                 telegram_token = opts[i][1]
            elif opts[i][0] == "-existing":
                existing = opts[i][1]
            else:
                print_help_message()
                sys.exit()
        except getopt.GetoptError:
            print_help_message()
            sys.exit()

        if existing = False and ((table_url is None) or (bot_name is None) or (telegram_token is None)):
            print_help_message()
            sys.exit()
    """
    bot_name = 'bot name'
    table_url = 'google.com'
    telegram_token = '855401787:AAHjueP4Ih-MF5WjL0NW-ISoN28qK5Vw4B8'
    URL = 'https://api.telegram.org/bot' + telegram_token + '/'
    sql_file = os.path.join(os.path.abspath(os.path.curdir), bot_name + '.sql')
    sqlite_database = os.path.join(os.path.abspath(os.path.curdir), bot_name + '.sqlite')
    """
        with open('temp.json', 'w') as df:
            vars = bot_name, table_url, telegram_token, sql_file, sqlite_database
            df.write(json.dumps(vars))
      
        if existing == True:
            with open('temp.json', 'r') as df:
                bot_name, table_url, telegram_token, sql_file, sqlite_database = json.loads(df.read())
    """

    try:
        app.run()
    except Exception as e:
        print(str(e))
    
if __name__ == '__main__':
    main()
