import requests
from suntime import Sun
from datetime import datetime
from geopy.geocoders import Nominatim

city_name = "New York"
geolocator = Nominatim(user_agent="MyApp")
location = geolocator.geocode(city_name)
sun = Sun(location.latitude, location.longitude)
sunrise = sun.get_local_sunrise_time().strftime('%H:%M')
sunset = sun.get_local_sunset_time().strftime('%H:%M')
time_now = datetime.now().strftime("%H:%M")
temperature, weather_description, weather_pic = 0, '', 'na'

day = False
if sunset > time_now > sunrise:
    day = True

api_key = "32210aca08b979b923f5fffba1b68231"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
complete_url = base_url + "appid=" + api_key + "&q=" + city_name
response = requests.get(complete_url)
x = response.json()

foggy = ['fog', 'haze', 'smoke', 'mist']
weather_uniq = ['freezing rain', 'tornado', 'drizzle', 'thunderstorm']
light_cloudy = ['few clouds', 'scattered clouds']
heavy_cloudy = ['broken clouds', 'overcast clouds']
snowy = ['light snow', 'snow', 'heavy snow']
shower_snow = ['light shower sleet', 'shower snow', 'light shower snow', 'shower sleet']
rainy_snow = ['sleet', 'rain and snow', 'heavy shower snow', 'light rain and snow']
showers = ['ragged shower rain', 'heavy intensity shower rain', 'light intensity shower rain', 'shower rain']
rain = ['light rain', 'moderate rain', 'heavy intensity rain', 'very heavy rain', 'extreme rain']

conditions = [
    (foggy, "foggy"),
    (light_cloudy, "light_cloudy"),
    (heavy_cloudy, "heavy_cloudy"),
    (foggy, "foggy"),
    (snowy, "snowy"),
    (shower_snow, "shower_snow"),
    (rainy_snow, "rainy_snow"),
    (showers, "showers"),
    (rain, "rain")
    ]

weather_pic_dict = {
    'freezing rain': '0',
    'showers': '1',
    'tornado': '2',
    'thunderstorm': '3',
    'rainy_snow': '4',
    'drizzle': '5',
    'rain': '6',
    'snowy': '7',
    'shower_snow': '8',
    'foggy': '9',
    'heavy_cloudy': '10',
    'cloudy_night': '11',
    'cloudy_day': '12',
    'clear_night': '13',
    'clear_day': '14', 
}

if x["cod"] != "404":
    y = x["main"]
    temperature = y["temp"]
    # current_pressure = y["pressure"]
    # current_humidiy = y["humidity"]
    z = x["weather"]
    weather_description = [z[0]["main"].lower().strip(), z[0]["description"].lower().strip()]

    temp = round(temperature * (9/5) - 459.67)

    if weather_description[0] == 'clear':
        if day == True:
            weather_pic = weather_pic_dict.get('clear_day')
        else:
            weather_pic = weather_pic_dict.get('clear_night')
    elif weather_description[0] in weather_uniq:
        weather_pic = weather_pic_dict.get(weather_description[0])
    elif weather_description[1] in weather_uniq:
        weather_pic = weather_pic_dict.get(weather_description[1])
    else:
        for i in conditions:
            if weather_description[1] in i[0]:
                if i[1] == "light_cloudy":
                    if day == True:
                        weather_pic = weather_pic_dict.get('cloudy_day')
                    else:
                        weather_pic = weather_pic_dict.get('cloudy_night')
                else:
                    weather_pic = weather_pic_dict.get(i[1])

my_file = open("C:\\Users\\Islam\\Documents\\Rainmeter\\Skins\\SysDash-1.1.0\\Weather\\weather.ini", "r")
lines = my_file.readlines()

lines[27] = f'Substitute="":"{weather_pic}"\n'
lines[33] = f'Substitute="":"{temp}"\n'
lines[39] = f'Substitute="":"{city_name}"\n'

my_file = open("C:\\Users\\Islam\\Documents\\Rainmeter\\Skins\\SysDash-1.1.0\\Weather\\weather.ini", "w")
my_file.writelines(lines)
my_file.close()