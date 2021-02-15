import requests
from datetime import datetime
import smtplib
import time

MY_LAT = -33.868820
MY_LONG = 151.209290
MY_EMAIL = "your_email@gmail.com"
PASSWORD = "your_password"


def is_iss_position():
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    iss_latitude = float(data_iss["iss_position"]["latitude"])
    iss_longitude = float(data_iss["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_longitude <= MY_LAT+5 and MY_LONG-5 >= iss_latitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now_hour = datetime.now().hour
    if sunset-1 <= time_now_hour <= sunrise+1:
        return True


while True:
    time.sleep(60)
    if is_iss_position() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f"Subject:Look up at sky👆\n\nCheck out the flying ISS over your head!!!."
            )




