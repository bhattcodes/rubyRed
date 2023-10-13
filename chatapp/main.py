# from flask import Flask, render_template
# from flask_socketio import SocketIO
from flask import Flask, request, jsonify
import redis
import json
import datetime
import pytz

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your own secret key
# socketio = SocketIO(app)

redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def chat():
    # return render_template('chat.html')
    print("helllo /mainpage called")
    return "<h1>hi</h1>"

# @socketio.on('send_message')
# def handle_message(data):
#     message = data['message']
#     socketio.emit('message', {'message': message}, broadcast=True)

@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    array = ["11","12","13","14","15"]
    return jsonify(array)


# {"message": "Hello, sdfsdfsdfsdf!",
# "userid" : "54545445"}

@app.route('/add_message', methods=['POST'])
def add_message():
    data = request.json  # Assuming the request contains a JSON object

    if data and 'userid' in data:
        userid = data['userid']
        # current_datetime = datetime.now()

        ist = pytz.timezone('Asia/Kolkata')
        current_time_ist = datetime.datetime.now(ist)
        timestamp_ist = int(current_time_ist.timestamp())
        # formatted_time = current_time_ist.strftime('%Y-%m-%d %H:%M:%S %Z')


        # timestamp = int(current_datetime.timestamp())
        msg = data['message'] 
        message_key = timestamp_ist
        redis_db.set(timestamp_ist, json.dumps(data) )

        return jsonify({'status': 'Message added to Redis', 'time': message_key, 'userid': userid, 'message' : msg}), 201
    else:
        return jsonify({'error': 'Invalid JSON data'}), 400




@app.route('/read_messages', methods=['GET'])
def read_messages():
    print("read message called")
    keys_and_values = {}

    for key in redis_db.scan_iter("*"):
        value = redis_db.get(key)
        keys_and_values[key.decode('utf-8')] = value.decode('utf-8')

    sorted_data = dict( sorted(keys_and_values.items(), key=lambda item: int(item[0])) )

    return jsonify(sorted_data)

if __name__ == '__main__':
    app.run(port=5000)
