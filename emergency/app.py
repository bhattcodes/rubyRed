from flask import Flask, render_template, request, redirect, url_for
import requests
import webbrowser
import polyline
import folium
import pandas as pd

app = Flask(__name__)

# Function to get the nearest hospital
def get_nearest_hospital(lat, long):
    api_url = f"https://overpass-api.de/api/interpreter?data=[out:json];(node['amenity'='hospital'](around:1000,{lat},{long}););out;"
    response = requests.get(api_url)
    data = response.json()
    data_refined = data.get("elements", [])

    # Calculate distance for each hospital and sort the list by distance
    hospitals_with_distance = []
    for hospital in data_refined:
        hospital_name = hospital.get("tags", {}).get("name", "Unknown Hospital")
        hospital_lat = hospital.get("lat")
        hospital_lon = hospital.get("lon")
        distance, _ = calculate_distance(lat, long, hospital_lat, hospital_lon)
        if distance is not None:
            hospitals_with_distance.append({"name": hospital_name, "distance": distance, "latitude": hospital_lat, "longitude": hospital_lon})

    # Sort hospitals by distance
    sorted_hospitals = sorted(hospitals_with_distance, key=lambda x: float(x["distance"].split()[0]))

    return sorted_hospitals

# Function to calculate distance between two locations using the OSRM API
def calculate_distance(lat1, lon1, lat2, lon2):
    osrm_api_url = "http://router.project-osrm.org/route/v1/driving/"
    coordinates = f"{lon1},{lat1};{lon2},{lat2}"
    response = requests.get(osrm_api_url + coordinates)

    try:
        data = response.json()
        distance = data['routes'][0]['distance']
        distance_km = distance / 1000  # Convert meters to kilometers

        # Extract the route geometry as a polyline
        route_geometry = data['routes'][0]['geometry']
        route_coordinates = polyline.decode(route_geometry)

        # Convert route coordinates to DataFrame
        route_df = pd.DataFrame(route_coordinates, columns=["latitude", "longitude"])

        return f"{distance_km:.2f} km", route_df
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Agreement Page
@app.route('/')
def agreement():
    return render_template('agreement.html')

# Options Page
@app.route('/options')
def options():
    return render_template('options.html')

# Medical Assistance
@app.route('/medical_assistance', methods=['GET', 'POST'])
def medical_assistance():
    if request.method == 'POST':
        location_input = request.form.get('location_input')
        if location_input:
            lat, long = map(float, location_input.split(','))
            sorted_hospitals = get_nearest_hospital(lat, long)
            if sorted_hospitals:
                return render_template('medical_assistance_results.html', hospitals=sorted_hospitals)
    return render_template('medical_assistance.html')

@app.route('/proceed', methods=['POST'])
def proceed():
    agreement_agreed = request.form.get('agreement_agreed')
    if agreement_agreed:
        # Process the agreement here
        # Redirect to the next page or perform any other action
        return redirect(url_for('options'))  # Redirect to the "Options" page
    else:
        return "Please acknowledge the agreement before proceeding."

@app.route('/insecure_assistance', methods=['GET', 'POST'])
def insecure_assistance():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        phone_number = request.form.get('phone_number')
        emergency_contact = request.form.get('emergency_contact')
        location = request.form.get('location')

        if 'call_emergency' in request.form:
            if emergency_contact:
                # Replace 'tel:' with an appropriate protocol for calling in your location
                # This example uses 'tel:' for simplicity
                call_url = f'tel:{emergency_contact}'
                webbrowser.open(call_url)
            else:
                return "Please provide an emergency contact number before calling."

    return render_template('insecure_assistance.html')

# Others
@app.route('/others', methods=['GET', 'POST'])
def others():
    if request.method == 'POST':
        # Handle others assistance form submission here
        pass
    return render_template('others.html')

if __name__ == "__main__":
    app.run(debug=True)
