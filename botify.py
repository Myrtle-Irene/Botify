import argparse, os, sqlite3, request, json
from flask import Flask
from flask import request
from flask import jsonify
from db_query import get_sql, fetch

parser = argparse.ArgumentParser(description='One-click bot creation from web data')
parser.add_argument('-existing', type=bool, help='turn on existing bot')
parser.add_argument('-url', help='web page containing table data')
parser.add_argument('-name', help='project name')
parser.add_argument('-token', help='telegram token of bot')
args = parser.parse_args()

if args.existing == True:
    with open('temp.json', 'r') as df:
        bot_name, table_url, telegram_token, sql_file, sqlite_database = json.loads(df.read())
else:
    bot_name = args.name
    table_url = args.url
    telegram_token = args.token
    sql_file = os.path.join(os.path.abspath(os.path.curdir), bot_name + '.sql')
    sqlite_database = os.path.join(os.path.abspath(os.path.curdir), bot_name + '.sqlite')
URL = 'https://api.telegram.org/bot' + token + '/'
with open('temp.json', 'w') as df:
    vars = bot_name, table_url, telegram_token, sql_file, sqlite_database
    df.write(json.dumps(vars))

def make_databases(table_url, bot_name):
    os.system(r'sqlitebiter url "{}" -o {}'.format(sqlite_database))
    con = sqlite3.connect('{}'.format(sqlite_database)  
    with open(sql_file, 'w') as f:
        for line in con.iterdump():
            f.write('{}\n'.format(line))


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
        sql_query = get_sql(sql_file, message)
        answer = fetch(sql_query, sqlite_database)
        send_message(chat_id, answer)
    return '<h1>request: GET.\n bot is working.</h1>'


if __name__ == '__main__':
    app.run()
