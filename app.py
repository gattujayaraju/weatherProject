from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
             data = response.json()
             celsius = data['main']['temp']
             fahrenheit = (celsius * 9/5) + 32  # Convert °C to °F
             weather_data = {
                 'city': data['name'],
                 'temperature_c': round(celsius, 2),
                 'temperature_f': round(fahrenheit, 2),
                 'humidity': data['main']['humidity'],
                 'wind': data['wind']['speed'],
                 'description': data['weather'][0]['description'].title(),
                 'icon': data['weather'][0]['icon']
                 }

            
        else:
            weather_data = {'error': 'City not found!'}
    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
