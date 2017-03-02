__author__ = 'linwe991'

import random
from flask import Flask, jsonify, request
from Twidder import database_helper
from gevent.wsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from Twidder import app
import json

app = Flask(__name__)


active_connections = dict()

@app.route("/sign_in", methods=['POST'])
def sign_in():
    data = request.get_json()
    result = database_helper.find_user(data['email'], password=data['password'], status='LOGIN')
    if result:
        letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        token = ""
        for i in range(0, 36):
            token += letters[random.randint(0, 61)]
        database_helper.add_sign_in_user(data['email'], token)
        return jsonify({"status": 200, "token": token})
    else:
        return jsonify({"status": 400})




@app.route("/sign_up", methods=['POST'])
def sign_up():
    data = request.get_json()
    result = database_helper.add_user(data['email'], data['password'], data['firstname'], data['familyname'], data['gender'], data['city'], data['country'])

    if result:
        return jsonify({"status": 200})
    else:
        return jsonify({"status": 404})
#
#
@app.route("/sign_out")
def sign_out():
    token = request.args.get('token')
    result = database_helper.remove_sign_in_user(token)
    if result:
        return jsonify({"status": 200})
    else:
        return jsonify({"status": 400})
#
#
@app.route("/change_password", methods=['POST'])
def change_password():
    data = request.get_json()
    result = database_helper.change_password(data['token'], data['old_pw'], data['new_pw'])
    if result:
        return jsonify({"status": 200})
    else:
        return jsonify({"status": 400})
#
#
@app.route("/get_user_data_by_token")
def get_user_data_by_token():
    token = request.args.get('token')
    result = database_helper.find_sign_in_user(token)
    if result:
        return jsonify({"data":{"email":result[0],"firstname":result[1],"familyname":result[2],"gender":result[3],"city":result[4],"country":result[5]}, "status": 200})
    else:
        return jsonify({"status": 400})
#
#
@app.route("/get_user_data_by_email")
def get_user_data_by_email():
    token = request.args.get('token')   # Get the token from the URL
    email = request.args.get('email')   # Get the token from the URL
    result = database_helper.find_sign_in_user(token)   # Make sure the current user has logged in
    if result:
        result = database_helper.find_user(email)
        if result:
            return jsonify({"status": 200, "result": result})
        else:
            return jsonify({"status": 400})
    else:
        return jsonify({"status": 400})

#
#
@app.route("/get_user_messages_by_token")
def get_user_messages_by_token():
    token = request.args.get('token')   # Get the token from the URL
    print('current_user[UP]:', token)
    result, messages = database_helper.find_user_message(token)
    if result:
        return jsonify(result=result, messages=messages)
    else:
        return jsonify({"status": 400})
#
#
@app.route("/get_user_messages_by_email")
def get_user_messages_by_email():
    token = request.args.get('token')
    email = request.args.get('email')
    result, messages = database_helper.find_user_message(token=token,search_email=email)
    if result:
        return jsonify(result=result,messages=messages)
    else:
        return jsonify({"status": 400})
#
#
@app.route("/post_message", methods=['POST'])
def post_message():
    data = request.get_json()
    result = database_helper.add_message(data['token'], data['message'], data['email'])
    if result:
        return jsonify(result=result)
    else:
        return jsonify({"status": 400})


@app.route('/send_notification')
def send_notification():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            message = ws.receive()
            message = json.loads(message)
            if message['signal'] == 'NOTIFY_LOGIN':
                try:
                    active_connections[message['data']].send('BYE')
                    active_connections[message['data']] = ws
                except KeyError:
                    active_connections[message['data']] = ws
                for active_connection in active_connections.keys():
                        active_connections[active_connection].send('NEW_LOGIN')
            elif message['signal'] == 'NOTIFY_LOGOUT':
                print(active_connections)
                del active_connections[message['data']]
                print(active_connections)
                for active_connection in active_connections.keys():
                        active_connections[active_connection].send('NEW_LOGOUT')
            elif message['signal'] == 'NOTIFY_POST':
                active_connections[message['data']].send('NEW_POST')
            else:
                pass
    return


@app.route('/add_viewed_time')
def add_viewed_time():
    viewed_email = request.args.get('viewed_email')
    result = database_helper.add_viewed_time(viewed_email)
    return jsonify(result=result)


@app.route('/show_chart')
def show_chart():
    email = request.args.get('email')
    num_cur_onlines, num_posts, num_views = database_helper.show_chart(email)
    return jsonify({'num_cur_onlines': num_cur_onlines, 'num_posts': num_posts, 'num_views': num_views})


DATABASE = 'database.db'

@app.route("/")
def index():
    return app.send_static_file('client.html')

def init_database():
    with app.app_context():
        database_helper.init_db(DATABASE)

if __name__ == "__main__":
    init_database()
    http_server = WSGIServer(('', 5001), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
