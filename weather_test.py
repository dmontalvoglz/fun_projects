import requests

api_key = '8dd46b2a5c069351e28a65cac238ede4'

user_input = input("Enter a city: ")
weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&APPID={api_key}")

if weather_data.json()['cod'] == '404':
    print("No city found.")
else:
    weather = weather_data.json()['weather'][0]['main']
    temp = weather_data.json()['main']['temp']
    feels_like = weather_data.json()['main']['feels_like']

    print(f'The weather in {user_input} is: {weather}')
    print(f'The temperature in {user_input} is: {temp}')
    print(f'But feels like: {feels_like}')
