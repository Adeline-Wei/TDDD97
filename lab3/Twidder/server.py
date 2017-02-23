__author__ = 'linwe991'

from Twidder import app
import random
from flask import Flask, jsonify, request
from Twidder import database_helper

app = Flask(__name__)




@app.route("/sign_in", methods=['POST'])
def sign_in():
    ''' Return; A text string containing a randomly generated access token if the authentication is successful. '''
    email = request.form['email']
    password = request.form['password']
    result = database_helper.find_user(email, password=password, status='LOGIN')
    if result:
        letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        token = ""
        for i in range(0, 36):
            token += letters[random.randint(0, 61)]
        database_helper.add_sign_in_user(result[0],email,token)
        return jsonify({"status": 200, "token": token})
    else:
        return jsonify({"status": 404})




@app.route("/sign_up", methods=['POST'])
def sign_up():
    ''' Return: - '''
    my_data = request.get_json()
    # email = request.form['email']
    # password = request.form['password']
    # firstname = request.form['firstname']
    # familyname = request.form['familyname']
    # gender = request.form['gender']
    # city = request.form['city']
    # country = request.form['country']
    result = database_helper.add_user(my_data['email'], my_data['password'], my_data['firstname'], my_data['familyname'], my_data['gender'], my_data['city'], my_data['country'])
    if result:
        return jsonify({"status": 200})
    else:
        return jsonify({"status": 404})
#
#
@app.route("/sign_out", methods=['POST'])
def sign_out():
    ''' Return: - '''
    token = request.form['token']
    result = database_helper.remove_sign_in_user(token)
    if result:
        return jsonify({"status": 200})
    else:
        return jsonify({"status": 400})
#
#
@app.route("/change_password", methods=['POST'])
def change_password():
    token = request.form['token']
    old_pw = request.form['old_pw']
    new_pw = request.form['new_pw']
    result = database_helper.change_password(token, old_pw, new_pw)
    database_helper.close()
    if result:
        return jsonify({"status": 200})
    else:
        return jsonify({"status": 400})
#
#
@app.route("/get_user_data_by_token")
def get_user_data_by_token():
    token = request.args.get('token')   # Get the token from the URL
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
        return jsonify(result=result)
    else:
        return jsonify({"status": 400})

#
#
@app.route("/get_user_messages_by_token")
def get_user_messages_by_token():
    token = request.args.get('token')   # Get the token from the URL
    result, messages = database_helper.find_user_message(token)
    if result:
        return jsonify(result=result,messages=messages)
    else:
        return jsonify({"status": 400})
#
#
@app.route("/get_user_messages_by_email")
def get_user_messages_by_email():
    token = request.args.get('token')   # Get the token from the URL
    email = request.args.get('email')   # Get the token from the URL
    result, messages = database_helper.find_user_message(token=token,email=email)
    if result:
        return jsonify(result=result,messages=messages)
    else:
        return jsonify({"status": 400})
#
#
@app.route("/post_message", methods=['POST'])
def post_message():
    token = request.form['token']
    message = request.form['message']
    email = request.form['email']
    result = database_helper.add_message(token, message, email)
    if result:
        return jsonify(result=result)
    else:
        return jsonify({"status": 400})



DATABASE = 'database.db'

@app.route("/")
def index():
    # return jsonify()
    return app.send_static_file('client.html')

def init_database():
    with app.app_context():
        database_helper.init_db(DATABASE)

if __name__ == "__main__":
    init_database()
    app.run(debug=True, port=5002)