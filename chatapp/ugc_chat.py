import datetime
import redis
import pytz
import time, json

redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)


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
interval = 2*60


for question in questions:
    ist = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.datetime.now(ist)
    timestamp_ist = int(current_time_ist.timestamp())

    data = {"message":  str (question["text"]), "userid" : "0"  } 
    # data = {"message": "What's your favorite outdoor activity and why?" , "userid" : "0"  } 
    redis_db.set(timestamp_ist,  json.dumps(data) )

    # print("Message:", question["text"])
    time.sleep(interval)
