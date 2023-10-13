# from flask import Flask, render_template
# from flask_socketio import SocketIO
import time
from flask import Flask, request, jsonify
import redis
import json
import datetime
import pytz
import psycopg2
import pandas.io.sql as psql
import requests
from flask_cors import CORS
import threading

app = Flask(__name__)
# app = Flask(__name__)
CORS(app)
userids_array = ["11","12","13","14","15"]

redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def chat():
    print("helllo /mainpage called")
    return "<h1>hi</h1>"


def clear_postgres():
    try:
        # Replace with your PostgreSQL connection details
        conn = psycopg2.connect(
           host="localhost",
            database="postgres",
            port=5433,
            user="postgres",
            password="postgres"
        )

        # Create a cursor
        cursor = conn.cursor()

        # Construct and execute the DELETE statement
        delete_query = "DELETE FROM perz;"  # Deletes all rows from all tables in the public schema
        cursor.execute(delete_query)

        # Commit the transaction
        conn.commit()

        print("All rows deleted from the 'perz' table.")

    except psycopg2.Error as e:
        print(f"Error: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()




def connect(query, insert_data=None):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            port=5433,
            user="postgres",
            password="postgres"
        )

        # Create a cursor
        cursor = conn.cursor()

        if insert_data:
            # If insert_data is provided, execute an INSERT query
            insert_query = "INSERT INTO perz (userid, message, perz_tags) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (insert_data['userid'], insert_data['message'], insert_data['perz_tags']))
            conn.commit()
        else:
            # If insert_data is not provided, execute the SELECT query
            dataframe = psql.read_sql(query, conn)
            return dataframe

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)

    finally:
        if conn:
            conn.close()
            print('Database connection closed.')


# insert_data = {
#     'userid': 'Some Value',
#     'message': '42',
#     'perz_tags': 'Another Value'
# }
# df = connect(None,insert_data)
# df2= connect("select * from perz", None)

def hit_chat_completions_api(content):
    # API endpoint URL
    api_url = "http://10.5.10.104:10101/openai/chat/completions"

    # JSON data to send in the POST request
    json_data = {
        "username": "sa_perz",
        "password": "redBus@365",
        "api": 1,
        "request": {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a summarisation analyst."
                },
                {
                    "role": "user",
                    "content": content
                },
                {
                    "role": "user",
                    "content": "keep in mind that the output should not be more than 3 words, your task is to Understand the context of above user messages and summarise journey experience of user in bus in 2 or 3 words related to bus"
                }
            ]
        }
    }

    try:
        # Send an HTTP POST request
        response = requests.post(api_url, json=json_data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse and print the response content (assuming it's in JSON format)
            response_data = response.json()
            # print("Response:", response_data)
            return response_data
        else:
            print("HTTP request failed with status code:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("Error:", e)





def get_user_messages_store_postgres(data):

    for userid in userids_array:

        target_userid = userid
        messages_by_userid = []

        for key, value in data.items():
            message_data = json.loads(value)
            if message_data.get("userid") == target_userid and message_data["message"] != "NEWUSER":
                messages_by_userid.append(message_data["message"])

        print("userid: "+userid+" = "+str(messages_by_userid))
        response_data = hit_chat_completions_api(str(messages_by_userid))
        content = response_data['response']['openAIResponse']['choices'][0]['message']['content']
        print(content)

        # push to postgres
        insert_data = {
            'userid': userid,
            'message': str(messages_by_userid),
            'perz_tags': str(content)
        }
        connect(None,insert_data)

@app.route('/start_new_session',methods=['GET'])
def start_session():
    redis_db.flushall()
    clear_postgres()
    ist = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.datetime.now(ist)
    timestamp_ist = int(current_time_ist.timestamp())
    # ugc_message()
    for userid in userids_array:
        timestamp_ist+=1      
        data = {"message": "NEWUSER", "userid" : str (userid) } 
        redis_db.set(timestamp_ist,  json.dumps(data) )

    return jsonify({'status': 'initialised successfully in Redis', 'time': timestamp_ist }), 201




def ugc_message():
    json_data = '''
    {
    "questions": [
        {
        "id": 1,
        "text": "What's your favorite travel destination?"
        },
        {
        "id": 2,
        "text": "Share a memorable experience from your last vacation."
        },
        {
        "id": 3,
        "text": "What's your go-to recipe for a quick and delicious meal?"
        },
        {
        "id": 4,
        "text": "Tell us about a book you recently read and loved."
        },
        {
        "id": 5,
        "text": "What's your favorite outdoor activity and why?"
        }
    ]
    }
    '''

    data_dict = json.loads(json_data)
    questions = data_dict["questions"]

    # Define the interval in seconds (5 minutes)
    interval = 5 * 60

    while True:
            ist = pytz.timezone('Asia/Kolkata')
            current_time_ist = datetime.datetime.now(ist)
            timestamp_ist = int(current_time_ist.timestamp())

            # data = {"message":  str (question["text"]), "userid" : "0"  } 
            data = {"message": "What's your favorite outdoor activity and why?" , "userid" : "0"  } 
            redis_db.set(timestamp_ist,  json.dumps(data) )

            # print("Message:", question["text"])
            time.sleep(interval)

ugc_thread = threading.Thread(target=ugc_message)

# Start the thread
ugc_thread.start()




@app.route('/clear_session',methods=['GET'])
def clear_session():
    print("here in clear session")

    keys_and_values = {}

    for key in redis_db.scan_iter("*"):
        value = redis_db.get(key)
        keys_and_values[key.decode('utf-8')] = value.decode('utf-8')
    get_user_messages_store_postgres(keys_and_values)

    # df= connect(" Insert into perz values (1,'hello','clean') ")
    # print(df)
    
    print("helllo /clear_session called")
    return "<h1>session cleared</h1>"




@app.route('/get_all_users', methods=['GET'])
def get_all_users():
   
    return jsonify(userids_array)


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
        keys_and_values[key.decode('utf-8')] = json.loads( value.decode('utf-8') )

    sorted_data = dict( sorted(keys_and_values.items(), key=lambda item: int(item[0])) )

    return jsonify(sorted_data)

@app.route('/get_weather', methods=['GET'])
def get_weather():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    api_key = 'e5259aa36264967fe4043de7e002ae6f'

    # Construct the URL with the API key, latitude, and longitude
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'

    # Send an HTTP GET request to the OpenWeatherMap API (with SSL certificate verification disabled)
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        weather_desc = data['weather'][0]['description']

        # Return the weather information as JSON
        return jsonify({"Temperature": temperature, "Weather Description": weather_desc})
    else:
        # Return an error response
        return jsonify({"error": "Unable to retrieve weather information"})



@app.route('/call_external_api', methods=['POST'])
def call_external_api():
    try:
        # Get the input text from the request headers
        input_text = request.headers.get('Input-Text')

        # Define the payload for the external API request
        payload = {
            "username": "sa_perz",
            "password": "redBus@365",
            "api": 1,
            "request": {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a Redbus Travel Assistant which can create itineraries and help the customer. You don't have access to personal data.You have to suggest buses from redbus if the user asks for any source or destination"
                    },
                    {
                        "role": "user",
                        "content": input_text  # Use the input text from the headers
                    }
                ]
            }
        }

        # Make a POST request to the external API
        response = requests.post('http://10.5.10.104:10101/openai/chat/completions', json=payload)

        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": "Unable to retrieve response from external API"})
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == '__main__':
    # ugc_message()
    app.run(port=5000)

