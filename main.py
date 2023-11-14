import requests
from datetime import datetime
import smtplib
import time

# constants
MY_EMAIL = "" # change to your email
MY_PASSWORD = ""  # set to generated app password from 2 step-verification settings
# https://www.latlong.net/
MY_LAT = 42.975740  # Your latitude
MY_LONG = -81.318295  # Your longitude


# function to check if iss is close to your location
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # check if your position is within +5 or -5 degrees of the ISS position.
    if (MY_LAT - 5) <= iss_latitude <= (MY_LAT + 5) and (MY_LONG - 5) <= iss_longitude <= (MY_LONG + 5):
        return True


# function to check if it is currently daytime or nighttime
def is_nighttime():

    # parameters to pass in with get request for sunrise/sunset data
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    # extract data from response
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # get hold of current hour
    time_now = datetime.now().hour

    # check if current time is past sunset and before sunrise (nighttime)
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    # run loop every 60 seconds
    time.sleep(60)
    # if iss is close and it is dark outside
    if is_iss_overhead() and is_nighttime():
        # send email notification to look up
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:LOOK UP!\n\nThe ISS is above you in the sky"
            )
