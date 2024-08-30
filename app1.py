from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')  # HTML şablonunu döndür

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    api_key = 'f7372e9e86f5251932d2c1babdbcc07b'  # OpenWeatherMap API anahtarı
    # https://api.openweathermap.org/data/2.5/weather?q={city}&appid=fb5acd8df88134644cbe08ebdca7ca80&units=metric 
    # http://api.openweathermap.org/data/2.5/weather?q=London&appid=fb5acd8df88134644cbe08ebdca7ca80&units=metric postman kontrol  linki
    
    # URL'ler
    weather_url = 'http://api.openweathermap.org/data/2.5/weather'
    forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
    
    # Parametreler
    params = {
        'appid': api_key,
        'units': 'metric'
    }
    
    # Şehir adı veya koordinatlar ekleniyor
    if city:
        params['q'] = city
    elif lat and lon:
        params['lat'] = lat
        params['lon'] = lon
    else:
        return jsonify({'error': 'City or coordinates are required'}), 400

    try:
        # Hava durumu verisini al
        weather_response = requests.get(weather_url, params=params)
        weather_response.raise_for_status()  # Hata durumunda istisna fırlatır
        weather_data = weather_response.json()
      

    
        #json formatındaki apiden bilgileri parse ediypruz buraya
        # Gün doğumunu ve batımını al
        sunrise = weather_data['sys'].get('sunrise')
        sunset = weather_data['sys'].get('sunset')

        # Hissedilen sıcaklık, nem, minimum ve maksimum sıcaklıkları al
       
       
        feels_like = weather_data['main'].get('feels_like')
        humidity = weather_data['main'].get('humidity')
        temp_min = weather_data['main'].get('temp_min')
        temp_max = weather_data['main'].get('temp_max')
        wind_speed = weather_data['wind'].get('speed')  # Wind speed
        # 5 günlük hava tahmini verisini al
        forecast_response = requests.get(forecast_url, params=params)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        # Günlük tahminleri ayıkla
        forecasts = []
        for item in forecast_data['list']:
            if item['dt_txt'].endswith('12:00:00'):  # Yalnızca günlük tahminleri al
                forecasts.append({
                    'date': item['dt_txt'].split(' ')[0],
                    'temp': item['main']['temp'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    
                
                })

        # Yanıt verisi yapılandırılıyor
        weather_data = {
           'temp': weather_data['main'].get('temp'),
            'description': weather_data['weather'][0].get('description'),
            'icon': weather_data['weather'][0].get('icon'),
            'city': weather_data['name'],
            'forecasts': forecasts,
            'sunrise': sunrise,
            'sunset': sunset,
            'humidity': humidity,
            'feels_like': feels_like,
            'temp_min': temp_min,
            'temp_max': temp_max,
            'wind_speed': wind_speed  # Wind speed eklendi
           
        }
        return jsonify(weather_data)
    
    except requests.HTTPError as http_err:
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        return jsonify({'error': f'An error occurred: {err}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
