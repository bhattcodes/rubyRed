import sys
from flask import Flask, render_template, request, redirect, url_for
import requests
import webbrowser
import polyline
import folium
import pandas as pd
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

SENDER = 'noreply-depot@e-redbus.in'
SENDERNAME = 'noreply-depot@e-redbus.in'
USERNAME_SMTP = "noreply-depot@e-redbus.in"
PASSWORD_SMTP = "ZK*`h)5}LUP"
HOST = "smtp.gmail.com"
PORT = 587



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
def send_email(Subject, Body, Recipients_To, Recipients_Cc):
    try:
        SUBJECT = Subject
        BODY_HTML = '<html>' + Body + '</html>'
        RECIPIENT_TO = Recipients_To
        RECIPIENT_CC = Recipients_Cc
        RECIPIENT = RECIPIENT_CC.split(',') + [RECIPIENT_TO]
        print(RECIPIENT)
        # setting email content and recipients
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        #         print(msg['Subject'])
        #         print(msg['From'])
        msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
        msg['To'] = RECIPIENT_TO
        msg['Cc'] = RECIPIENT_CC
        # Record the MIME types
        html_body = MIMEText(BODY_HTML, 'html')
        
        # Attach html_body into message container.
        msg.attach(html_body)
        
#        for bu in ['REDBUS_SG','REDBUS_MY','REDBUS_ID','REDBUS_PE','REDBUS_CO']:
            
#            filename = "control_group_validation_{}.csv".format(bu)
#            try:
#                attachment = open(filename,'r')
#                part = MIMEBase('application', 'octet-stream')
#                part.set_payload((attachment).read())
#                encoders.encode_base64(part)
#                part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
#                msg.attach(part)
#            except FileFileNotFoundError:
#                pass

        # Try to send the message.
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    except Exception as e:
        print('Exception: SMTPEmailService.send_email\n', e, file=sys.stderr)
    else:
        print('Email sent to: ', Recipients_To, ', ', Recipients_Cc)

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

@app.route('/send_emergency_message', methods=['POST'])
def send_emergency_message():
    data = request.get_json()
    phone_number = data['phone_number']
    emergency_contact = data['emergency_contact']
    location = data['location']
    Body = f"Emergency: {location} {phone_number}. Please help!"

    # Implement code to send an SMS message with the location to the emergency contact here
    # You may need to use a service or GSM modem to send the SMS

    # For now, let's print the message for testing
    print("Sending SMS:", Body)

    # Return a response
    Subject = "Emergency !!!! Person needs help"
    Recipients_To = "shreyas.upadhy@redbus.com"
    Recipients_Cc = ""
    send_email(Subject, Body, Recipients_To, Recipients_Cc)
    return 'Emergency message sent.'

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

# Route to show hospital location on Google Maps
@app.route('/show_hospital_location', methods=['POST'])
def show_hospital_location():
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    
    # Construct the Google Maps URL using latitude and longitude
    google_maps_url = f"https://www.google.com/maps/place/{latitude},{longitude}"
    return redirect(google_maps_url)

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
    app.run(debug=True,port = 9090)
