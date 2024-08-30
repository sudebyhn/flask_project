document.addEventListener('DOMContentLoaded', () => {
    // "searchBtn" ve "locationBtn" butonlarını HTML'den seç
    const searchBtn = document.getElementById('searchBtn');
    const locationBtn = document.getElementById('locationBtn');

    // Tarayıcı konum hizmetlerini destekliyorsa, kullanıcının mevcut konumunu al
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const lat = position.coords.latitude; // Kullanıcının enlem bilgisi
            const lon = position.coords.longitude; // Kullanıcının boylam bilgisi
            fetchWeatherData(null, lat, lon); // Konum bilgilerini kullanarak hava durumu verisini al
        }, error => {
            console.error('Geolocation error:', error); // Konum alma hatasını konsola yazdır
        });
    } else {
        alert('Geolocation is not supported by this browser.'); // Tarayıcı konum hizmetlerini desteklemiyorsa kullanıcıya uyarı göster
    }

    // "locationBtn" butonuna tıklama olayını dinle
    if (locationBtn) {
        locationBtn.addEventListener('click', () => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(position => {
                    const lat = position.coords.latitude; // Kullanıcının enlem bilgisi
                    const lon = position.coords.longitude; // Kullanıcının boylam bilgisi
                    fetchWeatherData(null, lat, lon); // Konum bilgilerini kullanarak hava durumu verisini al
                }, error => {
                    console.error('Geolocation error:', error); // Konum alma hatasını konsola yazdır
                });
            } else {
                alert('Geolocation is not supported by this browser.'); // Tarayıcı konum hizmetlerini desteklemiyorsa kullanıcıya uyarı göster
            }
        });
    }

    // "searchBtn" butonuna tıklama olayını dinle
    if (searchBtn) {
        searchBtn.addEventListener('click', () => {
            const city = document.getElementById('city_input').value; // Şehir adı giriş alanından al
            fetchWeatherData(city); // Şehir adı ile hava durumu verisini al
        });
    }

    // Hava durumu verilerini almak için bir fonksiyon
    function fetchWeatherData(city, lat = null, lon = null) {
        let url = '/weather?'; // API URL'sini oluştur
        if (city) {
            url += `city=${city}`; // Şehir adı varsa URL'ye ekle
        } else if (lat && lon) {
            url += `lat=${lat}&lon=${lon}`; // Enlem ve boylam varsa URL'ye ekle
        } else {
            console.error('City or coordinates are required'); // Şehir adı veya koordinatlar sağlanmamışsa hata mesajı göster
            return;
        }

        // Hava durumu verilerini almak için fetch API'sini kullan
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`); // HTTP hatası varsa hata fırlat
                }
                return response.json(); // Yanıtı JSON formatında döndür
            })
            .then(data => {
                console.log(data); // API yanıtını konsola yazdır

                if (data.error) {
                    console.error('API error:', data.error); // API hatası varsa konsola yazdır
                    return;
                }

                // Hava durumu bilgilerini DOM'a yerleştir
                const tempElement = document.getElementById('temp');
                const descElement = document.getElementById('description');
                const iconElement = document.getElementById('icon');
                const dateElement = document.getElementById('date');
                const cityElement = document.getElementById('city');
                const city1Element = document.getElementById('city1');


                const humidityElement = document.getElementById('humidity');
                const windSpeedElement = document.getElementById('wind-speed'); // Wind speed son eklendi


                if (tempElement && descElement && iconElement && dateElement && cityElement && humidityElement && city1Element) {
                    tempElement.innerHTML = `${data.temp}&deg;C`; // Sıcaklık bilgisi
                    descElement.textContent = data.description; // Hava durumu açıklaması
                    iconElement.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`; // Hava durumu ikonu
                    dateElement.textContent = 'Today'; // Tarih bilgisi
                    cityElement.textContent = data.city; // Şehir adı
                    city1Element.textContent = data.city; // city1Element için şehir adı


                    humidityElement.textContent = `Humidity: ${data.humidity}%`; 
                    // Nem oranı
                    windSpeedElement.textContent = `${data.wind_speed} m/s`; // Wind speed bilgisi

                } else {
                    console.error('One or more elements are missing in the DOM'); // Gerekli DOM elemanlarından biri eksikse hata mesajı göster
                }

                // 5 günlük hava tahmini verilerini DOM'a yerleştir
                const forecastContainer = document.querySelector('.day-forcast');
                if (forecastContainer) {
                    forecastContainer.innerHTML = ''; // Önceki tahminleri temizle
                    if (data.forecasts) {
                        data.forecasts.forEach(forecast => {
                            const forecastItem = document.createElement('div');
                            forecastItem.classList.add('forecast-item'); // Yeni bir tahmin kutusu oluştur
                            forecastItem.innerHTML = `
                                <div class="icon-wrapper">
                                    <img src="https://openweathermap.org/img/wn/${forecast.icon}@2x.png" alt="Forecast Icon">
                                    <span>${forecast.temp}&deg;C</span>
                                </div>
                                <p>${forecast.date}</p>
                                <p>${forecast.description}</p>
                            `;
                            forecastContainer.appendChild(forecastItem); // Tahmin kutusunu konteynıra ekle
                        });
                    }
                } else {
                    console.error('day-forcast not found'); // Hava tahmini konteynırı bulunamazsa hata mesajı göster
                }

                // Güneşin doğuş ve batış saatlerini güncelle
                const sunriseElement = document.getElementById('sunrise');
                const sunsetElement = document.getElementById('sunset');
                if (sunriseElement && sunsetElement && data.sunrise && data.sunset) {
                    const sunriseDate = new Date(data.sunrise * 1000); // Güneşin doğuş saatini Unix zaman damgası
                    const sunsetDate = new Date(data.sunset * 1000); // Güneşin batış saatini Unix zaman damgası
                    sunriseElement.textContent = sunriseDate.toLocaleTimeString(); // Güneşin doğuş saatini yerel saat formatı
                    sunsetElement.textContent = sunsetDate.toLocaleTimeString(); // Güneşin batış saatini yerel saat formatı
                } else {
                    console.error('Sunrise or sunset element not found in the DOM'); // Güneşin doğuş veya batış saatleri bulunamazsa hata 
                }
            })
            .catch(error => console.error('Fetch error:', error)); // Fetch hatası varsa konsola yazdır
    }


    
    function updateCurrentWeather(data) {
        // Güncel hava durumu bilgilerini güncelle
        const tempElement = document.getElementById('temp');
        const descElement = document.getElementById('description');
        const iconElement = document.getElementById('icon');
        const dateElement = document.getElementById('date');
        const cityElement = document.getElementById('city');
        const city1Element = document.getElementById('city1');

        const humidityElement = document.getElementById('humidity');
        const sunriseElement = document.getElementById('sunrise');
        const sunsetElement = document.getElementById('sunset');
        const windSpeedElement = document.getElementById('wind-speed'); // Wind speed 

    
        if (tempElement && descElement && iconElement && dateElement && cityElement && humidityElement && sunriseElement && sunsetElement && city1Element) {
            tempElement.innerHTML = `${data.temp}&deg;C`;
            descElement.textContent = data.description;
            iconElement.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
            dateElement.textContent = 'Today';
            cityElement.textContent = data.city;
            city1Element.textContent = data.city; // city1Element için şehir adı

            humidityElement.textContent = `Humidity: ${data.humidity}%`;
            windSpeedElement.textContent = `Wind Speed: ${data.wind_speed} m/s`; // Wind speed bilgisi 

    
            const sunriseDate = new Date(data.sunrise * 1000);
            const sunsetDate = new Date(data.sunset * 1000);
            sunriseElement.textContent = sunriseDate.toLocaleTimeString();
            sunsetElement.textContent = sunsetDate.toLocaleTimeString();
        } else {
            console.error('One or more elements are missing in the DOM');
        }
    }
    
});
