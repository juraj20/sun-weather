#importy
from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import requests
import customtkinter as ctk
import pytz

from geopy.geocoders import ArcGIS
from plyer import notification
from timezonefinder import TimezoneFinder
from threading import Thread, Event

#premenne
background = "#b0e2ff"  
paint_font = "#000000"
setting_font = ("arial",12)
wind_font = ("arial",10)
description_font = ("arial",16,"bold")
bg_color_descr = "#383ED5"
bg_weather = "#D9D9D9"
bg_hour_box = "#403D3D"
threadFlag = True

def deg_to_text(deg):
        return ["⬆ North", "⬈ NorthEast", "⮕ East", "⬊ SouthEast", "⬇ South", "⬋ SouthWest", "⬅ West", "⬉ NorthWest"][round(deg/45)%8]

def getCodeWeather(weathercode):
    weatherCode = ""
    
    if ((weathercode == 0) or (weathercode == 1)):
        weatherCode = "Clear"
    elif weathercode == 2:
        weatherCode = "Partly Cloudy"
    elif weathercode == 3:
        weatherCode = "Overcast"
    elif ((weathercode == 45) or (weathercode == 48)):
        weatherCode = "Fog"
    elif weathercode >= 51 and weathercode <= 55:
        weatherCode = "Drizzle"
    elif ((weathercode == 56) or (weathercode == 57)):
        weatherCode = "Freezing Drizzle"    
    elif ((weathercode == 61) or (weathercode == 63)):
        weatherCode = "Rain"
    elif weathercode == 65:
        weatherCode = "Heavy Rain"
    elif ((weathercode == 66) or (weathercode == 67)):
        weatherCode = "Freezing Rain"
    elif ((weathercode == 85) or (weathercode == 86) or (weathercode >= 71 and weathercode <= 77)):
        weatherCode = "Snow"
    elif weathercode >= 80 and weathercode <= 82:
        weatherCode = "Rain Shower"
    elif weathercode >= 95 and weathercode <=99:
        weatherCode = "Thunderstorm"
    else:
        weatherCode = "Error weather code"
        
    return weatherCode

def getLocation():
    try:
        city=search_textfield.get()
        geolocator = ArcGIS(user_agent="sun_weather")
        location = geolocator.geocode(city,timeout=7)
        #print(location.address)
        latitude = location.latitude
        longitude = location.longitude
        # print((location.latitude, location.longitude))
    
    except Exception as e:
        print("Nenájdená lokácia: ", e)

    
    return latitude,longitude

def getData(latitude, longitude):
    try:
        api= "https://api.open-meteo.com/v1/forecast?latitude=" + str(latitude)+ "&longitude=" + str(longitude)+"&current=temperature_2m,relative_humidity_2m,weather_code,pressure_msl,wind_speed_10m,wind_direction_10m&minutely_15=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m&hourly=temperature_2m,relative_humidity_2m,weather_code,pressure_msl,wind_speed_10m,wind_direction_10m,is_day&daily=sunrise,sunset&timezone=auto&forecast_days=3&models=best_match,ecmwf_ifs025,icon_eu,meteofrance_arpege_europe"
        print(latitude,longitude)
        json_data = requests.get(api,verify = True).json()
        
    except Exception as e:
        print("Vyskytla sa chyba: ", e)
    
    return json_data
    
def actualTime():
    latitude,longitude = getLocation()
    tf = TimezoneFinder()
    pom = tf.timezone_at(lng = longitude, lat = latitude)
    time_zone=pytz.timezone(pom)
    # Získajte aktuálny čas v tejto časovej zóne
    local_time = datetime.now(time_zone)
    time_string = local_time.strftime("%d %B,\n %A, \n %H:%M")
    time_clock.config(text=time_string)

    

def box_hour_city(latitude,longitude):

    tf = TimezoneFinder()
    pom = tf.timezone_at(lng=longitude, lat=latitude)
    time_zone=pytz.timezone(pom)
    local_time = datetime.now(time_zone)
    first_hour = local_time.replace(minute=0)
    cas= int(first_hour.strftime('%H'))+1
    
    if local_time.minute > 0 or local_time.second > 0 or local_time.microsecond > 0:
        first_hour += timedelta(hours=1)
        second_hour= first_hour + timedelta(hours=1)
        third_hour= first_hour + timedelta(hours=2)
        four_hour= first_hour + timedelta(hours=3)
        fiveth_hour= first_hour + timedelta(hours=4)
    
    first_hour=first_hour.strftime('%H:%M')    
    box_hour0.config(text=first_hour)
    
    second_hour=second_hour.strftime('%H:%M')
    box_hour1.config(text=second_hour)
    
    third_hour=third_hour.strftime('%H:%M')
    box_hour2.config(text=third_hour)
    
    four_hour=four_hour.strftime('%H:%M')
    box_hour3.config(text=four_hour)
    
    fiveth_hour=fiveth_hour.strftime('%H:%M')
    box_hour4.config(text=fiveth_hour)
    
    return cas

def box_minuten_city(latitude,longitude):

    tf = TimezoneFinder()
    pom = tf.timezone_at(lng=longitude, lat=latitude)
    time_zone=pytz.timezone(pom)

    local_time = datetime.now(time_zone)
    
    # Zaokrúhlite čas na najbližších 15 minút
    zaokruhlene_minuty = (local_time.minute // 15) * 15
    first_minuten = local_time.replace(minute=zaokruhlene_minuty, second=0, microsecond=0)

    if local_time > first_minuten:
        first_minuten += timedelta(minutes=15)
        second_minuten= first_minuten + timedelta(minutes=15)
        third_minuten= first_minuten + timedelta(minutes=30)
        four_minuten= first_minuten + timedelta(minutes=45)
        fiveth_minuten= first_minuten + timedelta(minutes=60)
    
    hour= int(first_minuten.strftime('%H'))
    minute=int(first_minuten.strftime('%M'))
    
    vyrataj_hodnotu=0
    if (minute == 0):
        vyrataj_hodnotu=0
    elif(minute == 15):
        vyrataj_hodnotu=1
    elif(minute == 30):
        vyrataj_hodnotu=2
    elif(minute == 45):
        vyrataj_hodnotu=3
    else:
        print("nepodarilo sa najst spravnu hodnotu")
    
    hodnota=(hour*4)+vyrataj_hodnotu  
    print("printni hodnotu")
    print(hodnota)    
        
    
    first_minuten=first_minuten.strftime('%H:%M')
    box_hour0.config(text=first_minuten)
    
    second_minuten=second_minuten.strftime('%H:%M')
    box_hour1.config(text=second_minuten)
    
    third_minuten=third_minuten.strftime('%H:%M')
    box_hour2.config(text=third_minuten)
    
    four_minuten=four_minuten.strftime('%H:%M')
    box_hour3.config(text=four_minuten)
    
    fiveth_minuten=fiveth_minuten.strftime('%H:%M')
    box_hour4.config(text=fiveth_minuten)
    
    return hodnota


def getCurrent(json_data):

    weatherCode = json_data['current']['weather_code']
    temp = float(json_data['current']['temperature_2m'])
    pressure = json_data['current']['pressure_msl']
    humidity = json_data['current']['relative_humidity_2m']
    wind = json_data['current']['wind_speed_10m']
    wind_direction = json_data['current']['wind_direction_10m']
    sunrise = str(json_data['daily']['sunrise_best_match'][0])
    sunset = str(json_data ['daily']['sunset_best_match'][0])
    time_sunrise = sunrise[11:]
    time_sunset = sunset[11:]
    
    temp_text.config(text = (temp,"°C"))
    weatherCode_text.config(text = (getCodeWeather(weatherCode)))
    humidity_text.config(text = (humidity, "%"))
    pressure_text.config(text = (pressure, "hPa"))
    wind_text.config(text = (wind, "km/h"))
    radius_wind_text.config(text = (deg_to_text(wind_direction)))
    sunrise_text.config(text = (time_sunrise))
    sunset_text.config(text = (time_sunset))
    
    image_actual = (Image.open(f"WeatherImg/{getCodeWeather(weatherCode)}.png"))
    resise_img0 = image_actual.resize((120,120))
    actual_photo = ImageTk.PhotoImage(resise_img0)
    actual_img.config(image = actual_photo)
    actual_img.image = actual_photo
    
def getCurrentImage(json_data):

    weatherCode = json_data['current']['weather_code']
    
    return weatherCode

def getWeather_BestMatch_Hour(json_data,latitude,longitude):

    urcity_index = box_hour_city(latitude,longitude)
    
    first_hour_img = json_data['hourly']['weather_code_best_match'][urcity_index]
    first_hour_temp=json_data['hourly']['temperature_2m_best_match'] [urcity_index]
    first_hour_wind = json_data['hourly']['wind_speed_10m_best_match'][urcity_index]
    
    second_hour_img = json_data ['hourly']['weather_code_best_match'][urcity_index+1]
    second_hour_temp = json_data['hourly']['temperature_2m_best_match'][urcity_index+1]
    second_hour_wind = json_data['hourly']['wind_speed_10m_best_match'][urcity_index+1]
    
    third_hour_img = json_data['hourly']['weather_code_best_match'][urcity_index+2]
    third_hour_temp = json_data['hourly']['temperature_2m_best_match'][urcity_index+2]
    third_hour_wind = json_data['hourly']['wind_speed_10m_best_match'][urcity_index+2]
    
    fourth_hour_img = json_data['hourly']['weather_code_best_match'][urcity_index+3]
    fourth_hour_temp = json_data['hourly']['temperature_2m_best_match'][urcity_index+3]
    fourth_hour_wind = json_data['hourly']['wind_speed_10m_best_match'][urcity_index+3]
    
    fiveth_hour_img = json_data['hourly']['weather_code_best_match'][urcity_index+4]
    fiveth_hour_temp = json_data['hourly']['temperature_2m_best_match'][urcity_index+4]
    fiveth_hour_wind = json_data['hourly']['wind_speed_10m_best_match'][urcity_index+4]
    
    image_first = (Image.open(f"WeatherImg/{getCodeWeather(first_hour_img)}.png"))
    resise_img1 = image_first.resize((70,70))
    first_photo = ImageTk.PhotoImage(resise_img1)
    first_img.config(image = first_photo)
    first_img.image = first_photo
    first_hour_temp_text.config(text=(first_hour_temp,"°C"))
    first_hour_wind_text.config(text=(first_hour_wind, "km/h"))
    
    image_second = (Image.open(f"WeatherImg/{getCodeWeather(second_hour_img)}.png"))
    resise_img2 = image_second.resize((70,70))
    second_photo = ImageTk.PhotoImage(resise_img2)
    second_img.config(image = second_photo)
    second_img.image = second_photo
    second_hour_temp_text.config(text=(second_hour_temp,"°C"))
    second_hour_wind_text.config(text=(second_hour_wind, "km/h"))
    
    image_third = (Image.open(f"WeatherImg/{getCodeWeather(third_hour_img)}.png"))
    resise_img3 = image_third.resize((70,70))
    third_photo = ImageTk.PhotoImage(resise_img3)
    third_img.config(image = third_photo)
    third_img.image = third_photo
    third_hour_temp_text.config(text=(third_hour_temp,"°C"))
    third_hour_wind_text.config(text=(third_hour_wind, "km/h"))

    
    image_fourth = (Image.open(f"WeatherImg/{getCodeWeather(fourth_hour_img)}.png"))
    resise_img4 = image_fourth.resize((70,70))
    fourth_photo = ImageTk.PhotoImage(resise_img4)
    fourth_img.config(image = fourth_photo)
    fourth_img.image = fourth_photo
    fourth_hour_temp_text.config(text=(fourth_hour_temp,"°C"))
    fourth_hour_wind_text.config(text=(fourth_hour_wind, "km/h"))

    
    image_fiveth = (Image.open(f"WeatherImg/{getCodeWeather(fiveth_hour_img)}.png"))
    resise_img5 = image_fiveth.resize((70,70))
    fiveth_photo = ImageTk.PhotoImage(resise_img5)
    fiveth_img.config(image = fiveth_photo)
    fiveth_img.image = fiveth_photo
    fiveth_hour_temp_text.config(text=(fiveth_hour_temp,"°C"))
    fiveth_hour_wind_text.config(text=(fiveth_hour_wind, "km/h"))
    

def getWeather_Ecmwf_Hour(json_data,latitude,longitude):

    urcity_index = box_hour_city(latitude,longitude)
    
    first_hour_img = json_data ['hourly']['weather_code_ecmwf_ifs025'][urcity_index]
    first_hour_temp=json_data ['hourly']['temperature_2m_ecmwf_ifs025'] [urcity_index]
    first_hour_wind = json_data ['hourly']['wind_speed_10m_ecmwf_ifs025'][urcity_index]
    
    second_hour_img = json_data ['hourly']['weather_code_ecmwf_ifs025'][urcity_index+1]
    second_hour_temp = json_data ['hourly']['temperature_2m_ecmwf_ifs025'][urcity_index+1]
    second_hour_wind = json_data ['hourly']['wind_speed_10m_ecmwf_ifs025'][urcity_index+1]
    
    third_hour_img = json_data ['hourly']['weather_code_ecmwf_ifs025'][urcity_index+2]
    third_hour_temp = json_data ['hourly']['temperature_2m_ecmwf_ifs025'][urcity_index+2]
    third_hour_wind = json_data ['hourly']['wind_speed_10m_ecmwf_ifs025'][urcity_index+2]
    
    fourth_hour_img = json_data ['hourly']['weather_code_ecmwf_ifs025'][urcity_index+3]
    fourth_hour_temp = json_data ['hourly']['temperature_2m_ecmwf_ifs025'][urcity_index+3]
    fourth_hour_wind = json_data ['hourly']['wind_speed_10m_ecmwf_ifs025'][urcity_index+3]
    
    fiveth_hour_img = json_data ['hourly']['weather_code_ecmwf_ifs025'][urcity_index+4]
    fiveth_hour_temp = json_data ['hourly']['temperature_2m_ecmwf_ifs025'][urcity_index+4]
    fiveth_hour_wind = json_data ['hourly']['wind_speed_10m_ecmwf_ifs025'][urcity_index+4]
    
    image_first = (Image.open(f"WeatherImg/{getCodeWeather(first_hour_img)}.png"))
    resise_img1 = image_first.resize((70,70))
    first_photo = ImageTk.PhotoImage(resise_img1)
    first_img.config(image = first_photo)
    first_img.image = first_photo
    first_hour_temp_text.config(text=(first_hour_temp,"°C"))
    first_hour_wind_text.config(text=(first_hour_wind, "km/h"))
    
    image_second = (Image.open(f"WeatherImg/{getCodeWeather(second_hour_img)}.png"))
    resise_img2 = image_second.resize((70,70))
    second_photo = ImageTk.PhotoImage(resise_img2)
    second_img.config(image = second_photo)
    second_img.image = second_photo
    second_hour_temp_text.config(text=(second_hour_temp,"°C"))
    second_hour_wind_text.config(text=(second_hour_wind, "km/h"))
    
    image_third = (Image.open(f"WeatherImg/{getCodeWeather(third_hour_img)}.png"))
    resise_img3 = image_third.resize((70,70))
    third_photo = ImageTk.PhotoImage(resise_img3)
    third_img.config(image = third_photo)
    third_img.image = third_photo
    third_hour_temp_text.config(text=(third_hour_temp,"°C"))
    third_hour_wind_text.config(text=(third_hour_wind, "km/h"))

    image_fourth = (Image.open(f"WeatherImg/{getCodeWeather(fourth_hour_img)}.png"))
    resise_img4 = image_fourth.resize((70,70))
    fourth_photo = ImageTk.PhotoImage(resise_img4)
    fourth_img.config(image = fourth_photo)
    fourth_img.image = fourth_photo
    fourth_hour_temp_text.config(text=(fourth_hour_temp,"°C"))
    fourth_hour_wind_text.config(text=(fourth_hour_wind, "km/h"))
    
    image_fiveth = (Image.open(f"WeatherImg/{getCodeWeather(fiveth_hour_img)}.png"))
    resise_img5 = image_fiveth.resize((70,70))
    fiveth_photo = ImageTk.PhotoImage(resise_img5)
    fiveth_img.config(image = fiveth_photo)
    fiveth_img.image = fiveth_photo
    fiveth_hour_temp_text.config(text=(fiveth_hour_temp,"°C"))
    fiveth_hour_wind_text.config(text=(fiveth_hour_wind, "km/h"))

def getWeather_Icon_Hour(json_data,latitude,longitude):
    
    urcity_index = box_hour_city(latitude,longitude)
    
    first_hour_img = json_data ['hourly']['weather_code_icon_eu'] [urcity_index]
    first_hour_temp=json_data ['hourly']['temperature_2m_icon_eu'] [urcity_index]
    first_hour_wind = json_data ['hourly']['wind_speed_10m_icon_eu'][urcity_index]
    
    second_hour_img = json_data ['hourly']['weather_code_icon_eu'][urcity_index+1]
    second_hour_temp = json_data ['hourly']['temperature_2m_icon_eu'][urcity_index+1]
    second_hour_wind = json_data ['hourly']['wind_speed_10m_icon_eu'][urcity_index+1]
    
    third_hour_img = json_data ['hourly']['weather_code_icon_eu'][urcity_index+2]
    third_hour_temp = json_data ['hourly']['temperature_2m_icon_eu'][urcity_index+2]
    third_hour_wind = json_data ['hourly']['wind_speed_10m_icon_eu'][urcity_index+2]
    
    fourth_hour_img = json_data ['hourly']['weather_code_icon_eu'][urcity_index+3]
    fourth_hour_temp = json_data ['hourly']['temperature_2m_icon_eu'][urcity_index+3]
    fourth_hour_wind = json_data ['hourly']['wind_speed_10m_icon_eu'][urcity_index+3]
    
    fiveth_hour_img = json_data ['hourly']['weather_code_icon_eu'][urcity_index+4]
    fiveth_hour_temp = json_data ['hourly']['temperature_2m_icon_eu'][urcity_index+4]
    fiveth_hour_wind = json_data ['hourly']['wind_speed_10m_icon_eu'][urcity_index+4]
    
    
    image_first = (Image.open(f"WeatherImg/{getCodeWeather(first_hour_img)}.png"))
    resise_img1 = image_first.resize((70,70))
    first_photo = ImageTk.PhotoImage(resise_img1)
    first_img.config(image = first_photo)
    first_img.image = first_photo
    first_hour_temp_text.config(text=(first_hour_temp,"°C"))
    first_hour_wind_text.config(text=(first_hour_wind, "km/h"))
    
    image_second = (Image.open(f"WeatherImg/{getCodeWeather(second_hour_img)}.png"))
    resise_img2 = image_second.resize((70,70))
    second_photo = ImageTk.PhotoImage(resise_img2)
    second_img.config(image = second_photo)
    second_img.image = second_photo
    second_hour_temp_text.config(text=(second_hour_temp,"°C"))
    second_hour_wind_text.config(text=(second_hour_wind, "km/h"))
    
    image_third = (Image.open(f"WeatherImg/{getCodeWeather(third_hour_img)}.png"))
    resise_img3 = image_third.resize((70,70))
    third_photo = ImageTk.PhotoImage(resise_img3)
    third_img.config(image = third_photo)
    third_img.image = third_photo
    third_hour_temp_text.config(text=(third_hour_temp,"°C"))
    third_hour_wind_text.config(text=(third_hour_wind, "km/h"))

    image_fourth = (Image.open(f"WeatherImg/{getCodeWeather(fourth_hour_img)}.png"))
    resise_img4 = image_fourth.resize((70,70))
    fourth_photo = ImageTk.PhotoImage(resise_img4)
    fourth_img.config(image = fourth_photo)
    fourth_img.image = fourth_photo
    fourth_hour_temp_text.config(text=(fourth_hour_temp,"°C"))
    fourth_hour_wind_text.config(text=(fourth_hour_wind, "km/h"))

    image_fiveth = (Image.open(f"WeatherImg/{getCodeWeather(fiveth_hour_img)}.png"))
    resise_img5 = image_fiveth.resize((70,70))
    fiveth_photo = ImageTk.PhotoImage(resise_img5)
    fiveth_img.config(image = fiveth_photo)
    fiveth_img.image = fiveth_photo
    fiveth_hour_temp_text.config(text=(fiveth_hour_temp,"°C"))
    fiveth_hour_wind_text.config(text=(fiveth_hour_wind, "km/h"))
    
def getWeather_MeteoFrance_Europe_Hour(json_data,latitude,longitude):
    urcity_index = box_hour_city(latitude,longitude)

    first_hour_img = json_data ['hourly']['weather_code_meteofrance_arpege_europe'][urcity_index]
    first_hour_temp=json_data ['hourly']['temperature_2m_meteofrance_arpege_europe'] [urcity_index]
    first_hour_wind = json_data ['hourly']['wind_speed_10m_meteofrance_arpege_europe'][urcity_index]
  
    second_hour_img = json_data ['hourly']['weather_code_meteofrance_arpege_europe'][urcity_index+1]
    second_hour_temp = json_data ['hourly']['temperature_2m_meteofrance_arpege_europe'][urcity_index+1]
    second_hour_wind = json_data ['hourly']['wind_speed_10m_meteofrance_arpege_europe'][urcity_index+1]
    
    third_hour_img = json_data ['hourly']['weather_code_meteofrance_arpege_europe'][urcity_index+2]
    third_hour_temp = json_data ['hourly']['temperature_2m_meteofrance_arpege_europe'][urcity_index+2]
    third_hour_wind = json_data ['hourly']['wind_speed_10m_meteofrance_arpege_europe'][urcity_index+2]
    
    fourth_hour_img = json_data ['hourly']['weather_code_meteofrance_arpege_europe'][urcity_index+3]
    fourth_hour_temp = json_data ['hourly']['temperature_2m_meteofrance_arpege_europe'][urcity_index+3]
    fourth_hour_wind = json_data ['hourly']['wind_speed_10m_meteofrance_arpege_europe'][urcity_index+3]
    
    fiveth_hour_img = json_data ['hourly']['weather_code_meteofrance_arpege_europe'][urcity_index+4]
    fiveth_hour_temp = json_data ['hourly']['temperature_2m_meteofrance_arpege_europe'][urcity_index+4]
    fiveth_hour_wind = json_data ['hourly']['wind_speed_10m_meteofrance_arpege_europe'][urcity_index+4]
    
    image_first = (Image.open(f"WeatherImg/{getCodeWeather(first_hour_img)}.png"))
    resise_img1 = image_first.resize((70,70))
    first_photo = ImageTk.PhotoImage(resise_img1)
    first_img.config(image = first_photo)
    first_img.image = first_photo
    first_hour_temp_text.config(text=(first_hour_temp,"°C"))
    first_hour_wind_text.config(text=(first_hour_wind, "km/h"))
    
    image_second = (Image.open(f"WeatherImg/{getCodeWeather(second_hour_img)}.png"))
    resise_img2 = image_second.resize((70,70))
    second_photo = ImageTk.PhotoImage(resise_img2)
    second_img.config(image = second_photo)
    second_img.image = second_photo
    second_hour_temp_text.config(text=(second_hour_temp,"°C"))
    second_hour_wind_text.config(text=(second_hour_wind, "km/h"))
    
    image_third = (Image.open(f"WeatherImg/{getCodeWeather(third_hour_img)}.png"))
    resise_img3 = image_third.resize((70,70))
    third_photo = ImageTk.PhotoImage(resise_img3)
    third_img.config(image = third_photo)
    third_img.image = third_photo
    third_hour_temp_text.config(text=(third_hour_temp,"°C"))
    third_hour_wind_text.config(text=(third_hour_wind, "km/h"))
    
    image_fourth = (Image.open(f"WeatherImg/{getCodeWeather(fourth_hour_img)}.png"))
    resise_img4 = image_fourth.resize((70,70))
    fourth_photo = ImageTk.PhotoImage(resise_img4)
    fourth_img.config(image = fourth_photo)
    fourth_img.image = fourth_photo
    fourth_hour_temp_text.config(text=(fourth_hour_temp,"°C"))
    fourth_hour_wind_text.config(text=(fourth_hour_wind, "km/h"))

    image_fiveth = (Image.open(f"WeatherImg/{getCodeWeather(fiveth_hour_img)}.png"))
    resise_img5 = image_fiveth.resize((70,70))
    fiveth_photo = ImageTk.PhotoImage(resise_img5)
    fiveth_img.config(image = fiveth_photo)
    fiveth_img.image = fiveth_photo
    fiveth_hour_temp_text.config(text=(fiveth_hour_temp,"°C"))
    fiveth_hour_wind_text.config(text=(fiveth_hour_wind, "km/h"))
    
def getWeather_BestMatch_Minutely_15(json_data,latitude,longitude):
    urcity_index = box_minuten_city(latitude,longitude)
    
    first_hour_img = json_data ['minutely_15']['weather_code_best_match'][urcity_index]
    first_hour_temp=json_data ['minutely_15']['temperature_2m_best_match'] [urcity_index]
    first_hour_wind = json_data ['minutely_15']['wind_speed_10m_best_match'][urcity_index]
    
    second_hour_img = json_data ['minutely_15']['weather_code_best_match'][urcity_index+1]
    second_hour_temp = json_data ['minutely_15']['temperature_2m_best_match'][urcity_index+1]
    second_hour_wind = json_data ['minutely_15']['wind_speed_10m_best_match'][urcity_index+1]
    
    third_hour_img = json_data ['minutely_15']['weather_code_best_match'][urcity_index+2]
    third_hour_temp = json_data ['minutely_15']['temperature_2m_best_match'][urcity_index+2]
    third_hour_wind = json_data ['minutely_15']['wind_speed_10m_best_match'][urcity_index+2]
    
    fourth_hour_img = json_data ['minutely_15']['weather_code_best_match'][urcity_index+3]
    fourth_hour_temp = json_data ['minutely_15']['temperature_2m_best_match'][urcity_index+3]
    fourth_hour_wind = json_data ['minutely_15']['wind_speed_10m_best_match'][urcity_index+3]
    
    fiveth_hour_img = json_data ['minutely_15']['weather_code_best_match'][urcity_index+4]
    fiveth_hour_temp = json_data ['minutely_15']['temperature_2m_best_match'][urcity_index+4]
    fiveth_hour_wind = json_data ['minutely_15']['wind_speed_10m_best_match'][urcity_index+4]
    
    image_first = (Image.open(f"WeatherImg/{getCodeWeather(first_hour_img)}.png"))
    resise_img1 = image_first.resize((70,70))
    first_photo = ImageTk.PhotoImage(resise_img1)
    first_img.config(image = first_photo)
    first_img.image = first_photo
    first_hour_temp_text.config(text=(first_hour_temp,"°C"))
    first_hour_wind_text.config(text=(first_hour_wind, "km/h"))
    
    image_second = (Image.open(f"WeatherImg/{getCodeWeather(second_hour_img)}.png"))
    resise_img2 = image_second.resize((70,70))
    second_photo = ImageTk.PhotoImage(resise_img2)
    second_img.config(image = second_photo)
    second_img.image = second_photo
    second_hour_temp_text.config(text=(second_hour_temp,"°C"))
    second_hour_wind_text.config(text=(second_hour_wind, "km/h"))
    
    image_third = (Image.open(f"WeatherImg/{getCodeWeather(third_hour_img)}.png"))
    resise_img3 = image_third.resize((70,70))
    third_photo = ImageTk.PhotoImage(resise_img3)
    third_img.config(image = third_photo)
    third_img.image = third_photo
    third_hour_temp_text.config(text=(third_hour_temp,"°C"))
    third_hour_wind_text.config(text=(third_hour_wind, "km/h"))
    
    image_fourth = (Image.open(f"WeatherImg/{getCodeWeather(fourth_hour_img)}.png"))
    resise_img4 = image_fourth.resize((70,70))
    fourth_photo = ImageTk.PhotoImage(resise_img4)
    fourth_img.config(image = fourth_photo)
    fourth_img.image = fourth_photo
    fourth_hour_temp_text.config(text=(fourth_hour_temp,"°C"))
    fourth_hour_wind_text.config(text=(fourth_hour_wind, "km/h"))

    image_fiveth = (Image.open(f"WeatherImg/{getCodeWeather(fiveth_hour_img)}.png"))
    resise_img5 = image_fiveth.resize((70,70))
    fiveth_photo = ImageTk.PhotoImage(resise_img5)
    fiveth_img.config(image = fiveth_photo)
    fiveth_img.image = fiveth_photo
    fiveth_hour_temp_text.config(text=(fiveth_hour_temp,"°C"))
    fiveth_hour_wind_text.config(text=(fiveth_hour_wind, "km/h"))
    
def getWeather_Ecmwf_Minutely_15(json_data,latitude,longitude):
    urcity_index = box_minuten_city(latitude,longitude)

    first_hour_img = json_data ['minutely_15']['weather_code_ecmwf_ifs025'][urcity_index]
    first_hour_temp=json_data ['minutely_15']['temperature_2m_ecmwf_ifs025'] [urcity_index]
    first_hour_wind = json_data ['minutely_15']['wind_speed_10m_ecmwf_ifs025'][urcity_index]
    
    second_hour_img = json_data ['minutely_15']['weather_code_ecmwf_ifs025'][urcity_index+1]
    second_hour_temp = json_data ['minutely_15']['temperature_2m_ecmwf_ifs025'][urcity_index+1]
    second_hour_wind = json_data ['minutely_15']['wind_speed_10m_ecmwf_ifs025'][urcity_index+1]
    
    third_hour_img = json_data ['minutely_15']['weather_code_ecmwf_ifs025'][urcity_index+2]
    third_hour_temp = json_data ['minutely_15']['temperature_2m_ecmwf_ifs025'][urcity_index+2]
    third_hour_wind = json_data ['minutely_15']['wind_speed_10m_ecmwf_ifs025'][urcity_index+2]
    
    fourth_hour_img = json_data ['minutely_15']['weather_code_ecmwf_ifs025'][urcity_index+3]
    fourth_hour_temp = json_data ['minutely_15']['temperature_2m_ecmwf_ifs025'][urcity_index+3]
    fourth_hour_wind = json_data ['minutely_15']['wind_speed_10m_ecmwf_ifs025'][urcity_index+3]
    
    fiveth_hour_img = json_data ['minutely_15']['weather_code_ecmwf_ifs025'][urcity_index+4]
    fiveth_hour_temp = json_data ['minutely_15']['temperature_2m_ecmwf_ifs025'][urcity_index+4]
    fiveth_hour_wind = json_data ['minutely_15']['wind_speed_10m_ecmwf_ifs025'][urcity_index+4]
    
    image_first = (Image.open(f"WeatherImg/{getCodeWeather(first_hour_img)}.png"))
    resise_img1 = image_first.resize((70,70))
    first_photo = ImageTk.PhotoImage(resise_img1)
    first_img.config(image = first_photo)
    first_img.image = first_photo
    first_hour_temp_text.config(text=(first_hour_temp,"°C"))
    first_hour_wind_text.config(text=(first_hour_wind, "km/h"))
    
    image_second = (Image.open(f"WeatherImg/{getCodeWeather(second_hour_img)}.png"))
    resise_img2 = image_second.resize((70,70))
    second_photo = ImageTk.PhotoImage(resise_img2)
    second_img.config(image = second_photo)
    second_img.image = second_photo
    second_hour_temp_text.config(text=(second_hour_temp,"°C"))
    second_hour_wind_text.config(text=(second_hour_wind, "km/h"))
    
    image_third = (Image.open(f"WeatherImg/{getCodeWeather(third_hour_img)}.png"))
    resise_img3 = image_third.resize((70,70))
    third_photo = ImageTk.PhotoImage(resise_img3)
    third_img.config(image = third_photo)
    third_img.image = third_photo
    third_hour_temp_text.config(text=(third_hour_temp,"°C"))
    third_hour_wind_text.config(text=(third_hour_wind, "km/h"))
    
    image_fourth = (Image.open(f"WeatherImg/{getCodeWeather(fourth_hour_img)}.png"))
    resise_img4 = image_fourth.resize((70,70))
    fourth_photo = ImageTk.PhotoImage(resise_img4)
    fourth_img.config(image = fourth_photo)
    fourth_img.image = fourth_photo
    fourth_hour_temp_text.config(text=(fourth_hour_temp,"°C"))
    fourth_hour_wind_text.config(text=(fourth_hour_wind, "km/h"))

    image_fiveth = (Image.open(f"WeatherImg/{getCodeWeather(fiveth_hour_img)}.png"))
    resise_img5 = image_fiveth.resize((70,70))
    fiveth_photo = ImageTk.PhotoImage(resise_img5)
    fiveth_img.config(image = fiveth_photo)
    fiveth_img.image = fiveth_photo
    fiveth_hour_temp_text.config(text=(fiveth_hour_temp,"°C"))
    fiveth_hour_wind_text.config(text=(fiveth_hour_wind, "km/h"))

def getWeather_Icon_Minutely_15(json_data,latitude,longitude):
    urcity_index = box_minuten_city(latitude,longitude)

    first_hour_img = json_data ['minutely_15']['weather_code_icon_eu'][urcity_index]
    first_hour_temp=json_data ['minutely_15']['temperature_2m_icon_eu'] [urcity_index]
    first_hour_wind = json_data ['minutely_15']['wind_speed_10m_icon_eu'][urcity_index]
    
    second_hour_img = json_data ['minutely_15']['weather_code_icon_eu'][urcity_index+1]
    second_hour_temp = json_data ['minutely_15']['temperature_2m_icon_eu'][urcity_index+1]
    second_hour_wind = json_data ['minutely_15']['wind_speed_10m_icon_eu'][urcity_index+1]
    
    third_hour_img = json_data ['minutely_15']['weather_code_icon_eu'][urcity_index+2]
    third_hour_temp = json_data ['minutely_15']['temperature_2m_icon_eu'][urcity_index+2]
    third_hour_wind = json_data ['minutely_15']['wind_speed_10m_icon_eu'][urcity_index+2]
    
    fourth_hour_img = json_data ['minutely_15']['weather_code_icon_eu'][urcity_index+3]
    fourth_hour_temp = json_data ['minutely_15']['temperature_2m_icon_eu'][urcity_index+3]
    fourth_hour_wind = json_data ['minutely_15']['wind_speed_10m_icon_eu'][urcity_index+3]
    
    fiveth_hour_img = json_data ['minutely_15']['weather_code_icon_eu'][urcity_index+4]
    fiveth_hour_temp = json_data ['minutely_15']['temperature_2m_icon_eu'][urcity_index+4]
    fiveth_hour_wind = json_data ['minutely_15']['wind_speed_10m_icon_eu'][urcity_index+4]
    
    image_first = (Image.open(f"WeatherImg/{getCodeWeather(first_hour_img)}.png"))
    resise_img1 = image_first.resize((70,70))
    first_photo = ImageTk.PhotoImage(resise_img1)
    first_img.config(image = first_photo)
    first_img.image = first_photo
    first_hour_temp_text.config(text=(first_hour_temp,"°C"))
    first_hour_wind_text.config(text=(first_hour_wind, "km/h"))
    
    image_second = (Image.open(f"WeatherImg/{getCodeWeather(second_hour_img)}.png"))
    resise_img2 = image_second.resize((70,70))
    second_photo = ImageTk.PhotoImage(resise_img2)
    second_img.config(image = second_photo)
    second_img.image = second_photo
    second_hour_temp_text.config(text=(second_hour_temp,"°C"))
    second_hour_wind_text.config(text=(second_hour_wind, "km/h"))
    
    image_third = (Image.open(f"WeatherImg/{getCodeWeather(third_hour_img)}.png"))
    resise_img3 = image_third.resize((70,70))
    third_photo = ImageTk.PhotoImage(resise_img3)
    third_img.config(image = third_photo)
    third_img.image = third_photo
    third_hour_temp_text.config(text=(third_hour_temp,"°C"))
    third_hour_wind_text.config(text=(third_hour_wind, "km/h"))
    
    image_fourth = (Image.open(f"WeatherImg/{getCodeWeather(fourth_hour_img)}.png"))
    resise_img4 = image_fourth.resize((70,70))
    fourth_photo = ImageTk.PhotoImage(resise_img4)
    fourth_img.config(image = fourth_photo)
    fourth_img.image = fourth_photo
    fourth_hour_temp_text.config(text=(fourth_hour_temp,"°C"))
    fourth_hour_wind_text.config(text=(fourth_hour_wind, "km/h"))

    image_fiveth = (Image.open(f"WeatherImg/{getCodeWeather(fiveth_hour_img)}.png"))
    resise_img5 = image_fiveth.resize((70,70))
    fiveth_photo = ImageTk.PhotoImage(resise_img5)
    fiveth_img.config(image = fiveth_photo)
    fiveth_img.image = fiveth_photo
    fiveth_hour_temp_text.config(text=(fiveth_hour_temp,"°C"))
    fiveth_hour_wind_text.config(text=(fiveth_hour_wind, "km/h"))
    
def getWeather_MeteoFrance_Europe_Minutely_15(json_data,latitude,longitude):
    urcity_index = box_minuten_city(latitude,longitude)

    first_hour_img = json_data ['minutely_15']['weather_code_meteofrance_arpege_europe'][urcity_index]
    first_hour_temp=json_data ['minutely_15']['temperature_2m_meteofrance_arpege_europe'] [urcity_index]
    first_hour_wind = json_data ['minutely_15']['wind_speed_10m_meteofrance_arpege_europe'][urcity_index]
    
    second_hour_img = json_data ['minutely_15']['weather_code_meteofrance_arpege_europe'][urcity_index+1]
    second_hour_temp = json_data ['minutely_15']['temperature_2m_meteofrance_arpege_europe'][urcity_index+1]
    second_hour_wind = json_data ['minutely_15']['wind_speed_10m_meteofrance_arpege_europe'][urcity_index+1]
    
    third_hour_img = json_data ['minutely_15']['weather_code_meteofrance_arpege_europe'][urcity_index+2]
    third_hour_temp = json_data ['minutely_15']['temperature_2m_meteofrance_arpege_europe'][urcity_index+2]
    third_hour_wind = json_data ['minutely_15']['wind_speed_10m_meteofrance_arpege_europe'][urcity_index+2]
    
    fourth_hour_img = json_data ['minutely_15']['weather_code_meteofrance_arpege_europe'][urcity_index+3]
    fourth_hour_temp = json_data ['minutely_15']['temperature_2m_meteofrance_arpege_europe'][urcity_index+3]
    fourth_hour_wind = json_data ['minutely_15']['wind_speed_10m_meteofrance_arpege_europe'][urcity_index+3]
    
    fiveth_hour_img = json_data ['minutely_15']['weather_code_meteofrance_arpege_europe'][urcity_index+4]
    fiveth_hour_temp = json_data ['minutely_15']['temperature_2m_meteofrance_arpege_europe'][urcity_index+4]
    fiveth_hour_wind = json_data ['minutely_15']['wind_speed_10m_meteofrance_arpege_europe'][urcity_index+4]
    
    image_first = (Image.open(f"WeatherImg/{getCodeWeather(first_hour_img)}.png"))
    resise_img1 = image_first.resize((70,70))
    first_photo = ImageTk.PhotoImage(resise_img1)
    first_img.config(image = first_photo)
    first_img.image = first_photo
    first_hour_temp_text.config(text=(first_hour_temp,"°C"))
    first_hour_wind_text.config(text=(first_hour_wind, "km/h"))
    
    image_second = (Image.open(f"WeatherImg/{getCodeWeather(second_hour_img)}.png"))
    resise_img2 = image_second.resize((70,70))
    second_photo = ImageTk.PhotoImage(resise_img2)
    second_img.config(image = second_photo)
    second_img.image = second_photo
    second_hour_temp_text.config(text=(second_hour_temp,"°C"))
    second_hour_wind_text.config(text=(second_hour_wind, "km/h"))
    
    image_third = (Image.open(f"WeatherImg/{getCodeWeather(third_hour_img)}.png"))
    resise_img3 = image_third.resize((70,70))
    third_photo = ImageTk.PhotoImage(resise_img3)
    third_img.config(image = third_photo)
    third_img.image = third_photo
    third_hour_temp_text.config(text=(third_hour_temp,"°C"))
    third_hour_wind_text.config(text=(third_hour_wind, "km/h"))
    
    image_fourth = (Image.open(f"WeatherImg/{getCodeWeather(fourth_hour_img)}.png"))
    resise_img4 = image_fourth.resize((70,70))
    fourth_photo = ImageTk.PhotoImage(resise_img4)
    fourth_img.config(image = fourth_photo)
    fourth_img.image = fourth_photo
    fourth_hour_temp_text.config(text=(fourth_hour_temp,"°C"))
    fourth_hour_wind_text.config(text=(fourth_hour_wind, "km/h"))

    image_fiveth = (Image.open(f"WeatherImg/{getCodeWeather(fiveth_hour_img)}.png"))
    resise_img5 = image_fiveth.resize((70,70))
    fiveth_photo = ImageTk.PhotoImage(resise_img5)
    fiveth_img.config(image = fiveth_photo)
    fiveth_img.image = fiveth_photo
    fiveth_hour_temp_text.config(text=(fiveth_hour_temp,"°C"))
    fiveth_hour_wind_text.config(text=(fiveth_hour_wind, "km/h"))

def getImage_BestMatch_Hour(json_data,latitude,longitude):
    urcity_index = box_hour_city(latitude,longitude)
    first_hour_img = json_data['hourly']['weather_code_best_match'][urcity_index]
    first_hour_img = getCodeWeather(first_hour_img)
    
    return first_hour_img

def getImage_Ecmwf_Hour(json_data,latitude,longitude):
    urcity_index = box_hour_city(latitude,longitude)
    print("urcity index " + str(urcity_index))
    
    first_hour_img = json_data['hourly']['weather_code_ecmwf_ifs025'][urcity_index]
    print("vypis mi first hour" + str(first_hour_img))
    first_hour_img = getCodeWeather(first_hour_img)
    return first_hour_img

def getImage_Icon_Hour(json_data,latitude,longitude):
    urcity_index = box_hour_city(latitude,longitude)
    # print(f"Urcity index: {urcity_index}")
    
    first_hour_img = json_data['hourly']['weather_code_icon_eu'][urcity_index]
    first_hour_img = getCodeWeather(first_hour_img)
    # print(f"First hour img: {first_hour_img}")
    return first_hour_img

def getImage_MeteoFrance_Hour(json_data,latitude,longitude):
    urcity_index = box_hour_city(latitude,longitude)
    
    first_hour_img = json_data['hourly']['weather_code_meteofrance_arpege_europe'][urcity_index]
    first_hour_img = getCodeWeather(first_hour_img)
    return first_hour_img


def getImage_BestMatch_Minutely_15(json_data,latitude,longitude):
    urcity_index = box_minuten_city(latitude,longitude)
    
    first_hour_img = json_data['minutely_15']['weather_code_best_match'][urcity_index]
    first_hour_img = getCodeWeather(first_hour_img)
    return first_hour_img

def getImage_Ecmwf_Minutely_15(json_data,latitude,longitude):
    urcity_index = box_minuten_city(latitude,longitude)
    
    first_hour_img = json_data['minutely_15']['weather_code_ecmwf_ifs025'][urcity_index]
    first_hour_img = getCodeWeather(first_hour_img)
    return first_hour_img

def getImage_Icon_Minutely_15(json_data,latitude,longitude):
    urcity_index = box_minuten_city(latitude,longitude)
    
    first_hour_img = json_data['minutely_15']['weather_code_icon_eu'][urcity_index]
    first_hour_img = getCodeWeather(first_hour_img)
    return first_hour_img

def getImage_MeteoFrance_Minutely_15(json_data,latitude,longitude):
    urcity_index = box_minuten_city(latitude,longitude)
    
    first_hour_img = json_data['minutely_15']['weather_code_meteofrance_arpege_europe'][urcity_index]
    first_hour_img = getCodeWeather(first_hour_img)
    return first_hour_img

def notify(weatherCode, first_hour_img):
    notification_title = "warning"
    notification_message = "dôjde k zmene počasia"
    
    if (weatherCode != first_hour_img):
        
        notification.notify(
            title = notification_title,
            message = notification_message,
            app_icon = "Images/logo3.ico",
            # timeout = 20,
            toast = False
        )
    else:
        print("nedôjde k žiadnej zmene")    
def btn():
    vybrana_hodnota(event=E)

def vybrana_hodnota(event):     
    
    vyber = selection_model.get()
    model =str(vyber) 
    actualTime()
    latitude,longitude=getLocation()
    json_data=getData(latitude,longitude)
    getCurrent(json_data)
    if (model == "Best Weather Hour"):
        getWeather_BestMatch_Hour(json_data,latitude,longitude)
    elif (model == "ECMWF Hour"):
        getWeather_Ecmwf_Hour(json_data,latitude,longitude)
    elif (model == "Icon Hour"):
        getWeather_Icon_Hour(json_data,latitude,longitude)
    elif (model == "MeteoFrance Hour"):
        getWeather_MeteoFrance_Europe_Hour(json_data,latitude,longitude)
    elif (model == "Best Weather 15 minutes"):
        getWeather_BestMatch_Minutely_15(json_data,latitude,longitude)
    elif (model == "ECMWF 15 minutes"):
        getWeather_Ecmwf_Minutely_15(json_data,latitude,longitude)
    elif (model == "Icon 15 minutes"):
        getWeather_Icon_Minutely_15(json_data,latitude,longitude)   
    elif (model == "MeteoFrance 15 minutes"):
        getWeather_MeteoFrance_Europe_Minutely_15(json_data,latitude,longitude) 
    else:
        print("Vybral si nespravnu hodnotu")
    myThrade2 = Thread(target=thread_fcia)
    myThrade2.start()

        
def thread_fcia():
    while threadFlag:
        currentImageCode = 0
        firstImageCode = 0
        
        vyber = selection_model.get()
        model =str(vyber) 
        actualTime()
        latitude,longitude=getLocation()
        json_data=getData(latitude,longitude)
        currentImageCode = getCurrentImage(json_data)
        currentImageCode = getCodeWeather(currentImageCode)
        
        if (model == "Best Weather Hour"):
            firstImageCode = getImage_BestMatch_Hour(json_data,latitude,longitude)  
            print(f"Weathercode current: {currentImageCode}, first image: {firstImageCode}")  
       
        elif (model == "ECMWF Hour"):
            firstImageCode = getImage_Ecmwf_Hour(json_data,latitude,longitude)
            print(f"Weathercode current: {currentImageCode}, first image: {firstImageCode}")
        
        elif (model == "Icon Hour"):
            firstImageCode = getImage_Icon_Hour(json_data,latitude,longitude)
            print(f"Weathercode current: {currentImageCode}, first image: {firstImageCode}")
        
        elif (model== "MeteoFrance Hour"):
            firstImageCode = getImage_MeteoFrance_Hour(json_data,latitude,longitude)
            print(f"Weathercode current: {currentImageCode}, first image: {firstImageCode}")
        
        elif (model == "Best Weather 15 minutes"):
            firstImageCode = getImage_BestMatch_Minutely_15(json_data,latitude,longitude)
            print(f"Weathercode current: {currentImageCode}, first image: {firstImageCode}")
        
        elif (model == "ECMWF 15 minutes"):
            firstImageCode = getImage_Ecmwf_Minutely_15(json_data,latitude,longitude)
            print(f"Weathercode current: {currentImageCode}, first image: {firstImageCode}")
        
        elif (model == "Icon 15 minutes"):
            firstImageCode = getImage_Icon_Minutely_15(json_data,latitude,longitude)   
            print(f"Weathercode current: {currentImageCode}, first image: {firstImageCode}")
        
        elif (model == "MeteoFrance 15 minutes"):
            firstImageCode = getImage_MeteoFrance_Minutely_15(json_data,latitude,longitude)  
            print(f"Weathercode current: {currentImageCode}, first image: {firstImageCode}")
        else:
            print("Vybral si nespravnu hodnotu")
        
        # print(f"Weathercode current: {currentImageCode}, first image: {firstImageCode}")
        
        notify(currentImageCode, firstImageCode)
        
        print("Run...")
        time.sleep(60) 

window = Tk()
window.title("Sun Weather")
window.geometry("450x515+1080+200")
window.configure(bg = background)
window.resizable(False,False)

#image icon
image_icon = PhotoImage(file = "Images/logo3.png")
window.iconphoto(False, image_icon)

#search
search_img = PhotoImage(file = "Images/search7.png")
search = Label(window, image = search_img, bg=background).place(x=130,y=10)
search_textfield=tk.Entry(window, justify="center", font=("poppins",14,"bold"), background="#403D3D", border=0, fg="#ffffff")
search_textfield.place(x=140,y=15)
search_textfield.focus()

search_btn=PhotoImage(file="Images/btn_search.png")
search2= Button(window, image=search_btn, border=0, borderwidth=0, command=btn).place(x=320, y=10)
window.bind('<Return>', lambda event: vybrana_hodnota(event=E))

combo_box=Label(window, text = "Weather model :",  
        font = setting_font, bg=background).place(x=30,y=55)
  
n = StringVar() 
selection_model = ttk.Combobox(window, width = 20,  
                            textvariable = n) 
  
# Adding combobox drop down list
models_list = ['Best Weather Hour',  
                'ECMWF Hour', 
                'Icon Hour', 
                'MeteoFrance Hour',
                'Best Weather 15 minutes',
                'ECMWF 15 minutes',
                'Icon 15 minutes',
                'MeteoFrance 15 minutes']

selection_model['values'] = models_list 
  
selection_model.place(x=30,y=75)
selection_model.current(models_list.index('Best Weather Hour'))
selection_model.configure(state="readonly")

# Shows a default value 
selection_model.current(0)  
getModel=selection_model.bind("<<ComboboxSelected>>", vybrana_hodnota)

#time
time_clock=Label(window, font=setting_font, fg=paint_font, bg=background)
time_clock.place(x=10,y=120)

#actual weather
actual_weather=PhotoImage(file="Images/obr_pocasia.png")
Label(window, image=actual_weather,bg=background).place(x=105,y=110)

actual_weather_frame = ctk.CTkFrame(master=window, width=120, height=120, corner_radius=12, border_width=4, bg_color=bg_weather)
actual_weather_frame.place(x=120,y=125) 
actual_img=Label(actual_weather_frame, border=0, bg=bg_weather, fg="#ffffff")
actual_img.pack()

#popis
weatherCode_img=PhotoImage(file="Images/popis.png")
Label(window, image=weatherCode_img, bg=background).place(x=260,y=50)
# vlhkost
vlhkost_img1=Image.open('Images/humidity.png')
vlhkost_resise=vlhkost_img1.resize((40, 40))
vlhkost_img=ImageTk.PhotoImage(vlhkost_resise)
vlhkost=Label(window, image=vlhkost_img, bg=bg_color_descr, fg=background)
vlhkost.place(x=270,y=60)
# tlak
tlak_img1=Image.open('Images/preasure.png')
tlak_resise=tlak_img1.resize((40, 40))
tlak_img=ImageTk.PhotoImage(tlak_resise)
tlak=Label(window, image=tlak_img, bg=bg_color_descr, fg=background)
tlak.place(x=270,y=110)
# rychlost vetra
rychlost_vetra_img1=Image.open('Images/wind.png')
rychlost_vetra_resise=rychlost_vetra_img1.resize((40, 40))
rychlost_vetra_img=ImageTk.PhotoImage(rychlost_vetra_resise)
rychlost_vetra=Label(window, image=rychlost_vetra_img, bg=bg_color_descr, fg=background)
rychlost_vetra.place(x=270,y=160)
# smer vetra
smer_vetra_img1=Image.open('Images/wind.png')
smer_vetra_resise=smer_vetra_img1.resize((40, 40))
smer_vetra_img=ImageTk.PhotoImage(smer_vetra_resise)
smer_vetra=Label(window, image=smer_vetra_img, bg=bg_color_descr, fg=background)
smer_vetra.place(x=270,y=210)
# vychod slnka
vychod_slnka_img1=Image.open('Images/sunrise3.png')
vychod_slnka_resise=vychod_slnka_img1.resize((40, 40))
vychod_slnka_img=ImageTk.PhotoImage(vychod_slnka_resise)
vychod_slnka=Label(window, image=vychod_slnka_img, bg=bg_color_descr, fg=background)
vychod_slnka.place(x=270,y=260)
# zapad slnka
zapad_slnka_img1=Image.open('Images/sunset3.png')
zapad_slnka_resise=zapad_slnka_img1.resize((40, 40))
zapad_slnka_img=ImageTk.PhotoImage(zapad_slnka_resise)
zapad_slnka=Label(window, image=zapad_slnka_img, bg=bg_color_descr, fg=background)
zapad_slnka.place(x=270,y=310)

weatherCode_text=Label(text="popis",font=description_font, border=0, bg=background)
weatherCode_text.place(x=100,y=290)

temp_text=Label(text="teplota",font=description_font, border=0, bg=background)
temp_text.place(x=15,y=220)

humidity_text=Label(text="humidity",font=description_font, border= 0, bg=bg_color_descr,fg="#ffffff")
humidity_text.place(x=320,y=65)

pressure_text=Label(text="pressure",font=description_font, border=0, bg=bg_color_descr,fg="#ffffff")
pressure_text.place(x=320,y=115)

wind_text=Label(text="wind",font=description_font,border=0, bg=bg_color_descr, fg="#ffffff")
wind_text.place(x=320,y=165)

radius_wind_text=Label(text="rad_wind",font=description_font, border=0, bg=bg_color_descr,fg="#ffffff")
radius_wind_text.place(x=320,y=215)

sunrise_text=Label(text="sunrise",font=description_font, border=0, bg=bg_color_descr,fg="#ffffff")
sunrise_text.place(x=320,y=265)

sunset_text=Label(text="sunset",font=description_font,border=0, bg=bg_color_descr,fg="#ffffff")
sunset_text.place(x=320,y=315)

#hour prediction

big_hour_box=PhotoImage(file="Images/hour_prediction.png")
Label(window, image=big_hour_box, bg=background).place(x=5,y=366)
# hour box
hour_box=PhotoImage(file="Images/hour_box3.png")
Label(window,image=hour_box,border=0,background=bg_hour_box).place(x=20,y=395) 
Label(window,image=hour_box,border=0,background=bg_hour_box).place(x=105,y=395)
Label(window,image=hour_box,border=0,background=bg_hour_box).place(x=190,y=395)
Label(window,image=hour_box,border=0,background=bg_hour_box).place(x=275,y=395)
Label(window,image=hour_box,border=0,background=bg_hour_box).place(x=360,y=395)

first_frame = ctk.CTkFrame(master=window, width=100, height=100, border_width=0, bg_color="#403D3D")
first_frame.place(x=23,y=397) 
first_img=Label(first_frame, border=0, bg = bg_weather)
first_img.pack()

second_frame = ctk.CTkFrame(master=window,width=100,height=100, border_width=0, bg_color="#403D3D")
second_frame.place(x=108,y=397)
second_img=Label(second_frame, border=0, bg=bg_weather)
second_img.pack()

third_frame = ctk.CTkFrame(master=window,width=100,height=100, border_width=0, bg_color="#403D3D")
third_frame.place(x=193,y=397)
third_img=Label(third_frame,border=0, bg=bg_weather)
third_img.pack()

fourth_frame = ctk.CTkFrame(master=window,width=100,height=100, border_width=0, bg_color="#403D3D")
fourth_frame.place(x=278,y=397)
fourth_img=Label(fourth_frame,border=0, bg=bg_weather)
fourth_img.pack()

fiveth_frame = ctk.CTkFrame(master=window,width=100,height=100, border_width=0, bg_color="#403D3D")
fiveth_frame.place(x=363,y=397)
fiveth_img = Label(fiveth_frame, border = 0, bg=bg_weather)
fiveth_img.pack()

#time hour box
#first
box_hour0 = Label(window, font = setting_font, border = 0, bg = "#403D3D",fg = "#ffffff")
box_hour0.place(x = 20, y = 373)

#second
box_hour1 = Label(window,font = setting_font, border = 0, bg = "#403D3D",fg = "#ffffff")
box_hour1.place(x = 105, y = 373)

#third
box_hour2 = Label(window, font = setting_font, border = 0, bg = "#403D3D", fg = "#ffffff")
box_hour2.place(x = 190, y = 373)

#fouth
box_hour3 = Label(window, font = setting_font, border = 0, bg = "#403D3D", fg = "#ffffff")
box_hour3.place(x = 275, y=373)
 
#fiveth
box_hour4 = Label(window, font = setting_font, border = 0, bg = "#403D3D", fg = "#ffffff")
box_hour4.place(x = 360, y=373)

first_hour_temp_text=Label(first_frame, font=setting_font, border=0, bg=bg_weather, activebackground=bg_weather)
first_hour_temp_text.pack()
first_hour_wind_text=Label(first_frame, font=wind_font, border=1, bg = bg_weather)
first_hour_wind_text.pack()

second_hour_temp_text=Label(second_frame, font=setting_font, border=0, bg=bg_weather, activebackground=bg_weather)
second_hour_temp_text.pack()
second_hour_wind_text=Label(second_frame, font=wind_font, border=1, bg=bg_weather)
second_hour_wind_text.pack()

third_hour_temp_text=Label(third_frame, font=setting_font, border=0, bg=bg_weather, activebackground=bg_weather)
third_hour_temp_text.pack()
third_hour_wind_text=Label(third_frame, font=wind_font, border=1, bg=bg_weather)
third_hour_wind_text.pack()

fourth_hour_temp_text=Label(fourth_frame, font=setting_font, border=0, bg=bg_weather, activebackground=bg_weather)
fourth_hour_temp_text.pack()
fourth_hour_wind_text=Label(fourth_frame, font=wind_font, border=1, bg=bg_weather)
fourth_hour_wind_text.pack()

fiveth_hour_temp_text=Label(fiveth_frame, font=setting_font, border=0, bg=bg_weather, activebackground=bg_weather)
fiveth_hour_temp_text.pack()
fiveth_hour_wind_text=Label(fiveth_frame, font=wind_font, border=1, bg=bg_weather)
fiveth_hour_wind_text.pack()

def on_closing():
    global threadFlag
    threadFlag = False
    print("Dovidenia!!!")
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
#run
window.mainloop()


