from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/') #route tanımladık route : url yolunu bir işlevle ilişkilendirme.
def index():
    return render_template('index.html')  # HTML şablonunu döndür

#API endpoint'ini tanımla
@app.route('/weather', methods=['GET']) # weather url yoluna HTTP get  istekleri işlenecek 
def get_weather():
    city = request.args.get('city') 
    lat = request.args.get('lat') #lat(enlem) bu satır request ile url parametrelerinden lat parametresini alır . EX: url si /weather?lat=51.5074&lon=-0.1278  GİBİ.
    lon = request.args.get('lon') #lot(boylam)
    
    api_key = 'f7372e9e86f5251932d2c1babdbcc07b'  # OpenWeatherMap API anahtarınızı buraya ekleyin
    # https://api.openweathermap.org/data/2.5/weather?q={city}&appid=fb5acd8df88134644cbe08ebdca7ca80&units=metric
    # http://api.openweathermap.org/data/2.5/weather?q=London&appid=fb5acd8df88134644cbe08ebdca7ca80&units=metric
    
    # URL'ler
    weather_url = 'http://api.openweathermap.org/data/2.5/weather' # Hava durumu verilerini almak için. url tanımladık
    forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
    
    # Parametreleri sözlüğe tanımladık
    params = {
        'appid': api_key, 
        'units': 'metric'
    }
    
    # API isteği için gerekli parametreleri içeren sözlüktür
    if city:
        params['q'] = city    
    elif lat and lon:   # lat ve lon varsa city yerine kullan hava durumunu almak için
        params['lat'] = lat
        params['lon'] = lon
    else:
        return jsonify({'error': 'City or coordinates are required'}), 400  #istek yapılamazsa hata döner

    try:
        # Hava durumu verisini al
        weather_response = requests.get(weather_url, params=params) #url ve parametrelerle APİ ye request gönderir ve Api den gelen yanıtı weather_responsed değişkenine kayıt eder
        weather_response.raise_for_status()  #  hata durumu kontrolü http isteği sırasında ,httperor gönderir
        weather_data = weather_response.json() # API yanıtını JSON formatından Python veri yapısına dönüştürür.

        # 5 günlük hava tahmini verisini al
        forecast_response = requests.get(forecast_url, params=params)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()    #parse ederiz json() methodu ile
        
        #JSON verisinde yer alan anahtarlar kullanılarak veriye erişilir
        sunrise = weather_data['sys'].get('sunrise')  #JSON yanıtında main anahtarının altındaki verileri al demek
        sunset = weather_data['sys'].get('sunset') #get()ifadesi olup olmadığını kontrol eder yoksa "none" döner
        feels_like = weather_data['main'].get('feels_like')
        humidity = weather_data['main'].get('humidity')
        temp_min = weather_data['main'].get('temp_min')
        temp_max = weather_data['main'].get('temp_max')
        wind_speed = weather_data['wind'].get('speed')  
        
        
       
        
        # Günlük tahminleri ayıkla
        forecasts = []  #boş liste oluşturdum günlük hava tahminlerini eklemek için
        for item in forecast_data['list']: #list anahtarına ait öğelerle döngü başlattık
            if item['dt_txt'].endswith('12:00:00'):  # gün ortasındaysa tahminler
                forecasts.append({  #sözlük olarak listeye(forecasts) ekle ve sözlük içerikleri;
                    'date': item['dt_txt'].split(' ')[0],
                    'temp': item['main']['temp'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    
        
                })

        # Yanıt verisi işleme json formatında
        weather_data = {    #APİ den alınan verileri kullanıcıya döndürücek şelide python sözlüğü oluşturur
           # API yanıtındaki doğrudan verileri alır
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
            'wind_speed': wind_speed 
     #API'den alınıp işlendikten sonra JSON yanıtına dahil edilicek veriler fakat istersek 'sunrise': weather_data['sys'].get('sunrise'),
    #'sunset': weather_data['sys'].get('sunset'),
    #'humidity': weather_data['main'].get('humidity'),
    #'feels_like': weather_data['main'].get('feels_like'),
    #'temp_min': weather_data['main'].get('temp_min'),
    #'temp_max': weather_data['main'].get('temp_max'),
    #'wind_speed': weather_data['wind'].get('speed')  şeklindede yukarda erişmeden direk yazabiliriz
       
        
        }
        return jsonify(weather_data)  # JSON formatında yanıt gönderilir
    
    except requests.HTTPError as http_err:
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        return jsonify({'error': f'An error occurred: {err}'}), 500

if __name__ == '__main__':
    app.run(debug=True)       #Flask uygulamasını başlatır,
                              #debug= true ile uygulama hata ayıklama modunda çalışır
