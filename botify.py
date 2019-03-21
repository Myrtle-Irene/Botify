from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
from db_query import get_sql

token = 'telegram_token'
URL = 'https://api.telegram.org/bot' + token + '/'
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
        answer = '<h2>answer</h2>'
        send_message(chat_id, answer)
        return jsonify(r)
    return '<h1>request: GET.\n bot is working.</h1>'


if __name__ == '__main__':
    app.run()
