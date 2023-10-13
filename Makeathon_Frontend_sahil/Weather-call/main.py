from flask import Flask, request, jsonify
import requests

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This enables CORS for your entire app




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
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000, host='0.0.0.0')
