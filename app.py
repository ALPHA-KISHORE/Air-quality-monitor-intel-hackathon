from flask import Flask, render_template, request
import requests
import numpy as np
import dpctl
from sklearnex import patch_sklearn, config_context

# Patch sklearn to enable optimizations
patch_sklearn()

app = Flask(__name__)

# Your actual API key
API_KEY = '776b909054d194e0098441aa4eec7993f1d091af'

def get_air_quality_data(city):
    url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'ok':
        air_quality_data = {
            'city': data['data']['city']['name'].split('(')[0].strip(),  # Removes the Hindi part
            'aqi': data['data']['aqi'],
            'pollutants': {
                'Humidity': data['data']['iaqi'].get('h', {'v': 'N/A'})['v'],
                'Pressure': data['data']['iaqi'].get('p', {'v': 'N/A'})['v'],
                'PM2.5': data['data']['iaqi'].get('pm25', {'v': 'N/A'})['v'],
                'Temperature': data['data']['iaqi'].get('t', {'v': 'N/A'})['v'],
                'Wind Speed': data['data']['iaqi'].get('w', {'v': 'N/A'})['v'],
                'Wind Gust': data['data']['iaqi'].get('wg', {'v': 'N/A'})['v'],
            }
        }
    else:
        air_quality_data = None

    return air_quality_data

@app.route('/', methods=['GET', 'POST'])
def index():
    air_quality_data = None
    if request.method == 'POST':
        city = request.form['city']
        air_quality_data = get_air_quality_data(city)
    
    return render_template('index.html', air_quality_data=air_quality_data)

if __name__ == '__main__':
    app.run(debug=True)
