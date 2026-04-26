# Weather App v2
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "cbc19a60736bbd7b47deb3825bd3cca5"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    if request.method == "POST":
        city = request.form.get("city")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "icon": data["weather"][0]["icon"]
            }
        else:
            error = "City not found! Please try again."
    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
