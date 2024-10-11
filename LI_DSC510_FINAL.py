# DSC 510
# Programming Assignment Week 12
# Rang Li
# 5/29/2023

# Change#:2
# Change(s) Made: temperature symbol added
# Date of Change: 5/2/2023
# Author: Rang Li
# Change Approved by: N/A
# Date Moved to Production: N/A


import datetime as dt
import requests
import re


# geolookup by zipcode
def geo_ziplookup(zipcode):
    api_key = "8c05197c728ef80a1528d4af64e53d1a"
    geobase_url = "http://api.openweathermap.org/geo/1.0/zip?zip="
    geo_url = geobase_url + zipcode + ",US&appid=" + api_key
    response1 = request(geo_url)
    data1 = response1.json()
    lat = data1['lat']
    lon = data1['lon']
    return lat, lon


# geo lookup by cityname
def geo_citylookup(cityname):
    api_key = "8c05197c728ef80a1528d4af64e53d1a"
    geobase_url = "http://api.openweathermap.org/geo/1.0/direct?q="
    geo_url = geobase_url + cityname + "," + "US&limit=1&appid=" + api_key
    response2 = request(geo_url)
    if not response2.json():
        print("Invalid input.")
        exit()
    data2 = response2.json()
    for data in data2:
        lat = data['lat']
        lon = data['lon']
        return lat, lon


# access weather data
def weather_data(x, y):
    api_key = "8c05197c728ef80a1528d4af64e53d1a"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    url = base_url + "lat=" + str(x) + "&lon=" + str(y) + "&appid=" + api_key
    response = request(url)
    data = response.json()
    return data


# url request error handling
def request(url):
    try:
        response = requests.get(url)
    except requests.exceptions.HTTPError as err:
        print("An error has occurred with making an connection.")
        print("The following exception has been raised, ", err)
    except requests.exceptions.ConnectionError as err:
        print("An error has occurred with making the connection.", err)
    return response


# k to c
def kelvin_to_celsius(kelvin):
    celsius = round(kelvin - 273.15, 2)
    return celsius


# k to f
def kelvin_to_fahrenheit(kelvin):
    fahrenheit = round(1.8*(kelvin-273) + 32, 1)
    return fahrenheit


def main():
    # zipcode lookup error handling
    pattern = '^[0-9]{5}(-[0-9]{4})?$'
    api_key = "8c05197c728ef80a1528d4af64e53d1a"
    # welcome
    option = input("\nWelcome to our weather program! Enter 'Y' to start or "
                   "'N' to end. ").lower()
    while True:
        if option == "y":
            user_input = input("\nPlease enter your zipcode or city and "
                               "state(separated by ','): ")
            # create a dict for weather data output
            result = dict()
            # user input
            try:
                int(user_input)
                matched = re.match(pattern, user_input)
                if matched:
                    lat, lon = geo_ziplookup(user_input)
                else:
                    print("Invalid zipcode.")
                    break
            except ValueError:
                if("," in user_input):
                    lat, lon = geo_citylookup(user_input)
                else:
                    print("please separate city and state by ',': ")
                    exit()
            # user choice for temperature display
            user_choice = input("\nDo you want it display in Celsius, "
                                "Fahrenheit or Kelvin? Type 'C' for Celsius, "
                                "'F' for Fahrenheit, or 'K' for Kelvin. ").lower()
            # access weather data
            weather = weather_data(lat, lon)
            # print(weather)
            temp_kelvin = weather['main']['temp']
            feels_like_kelvin = weather['main']['feels_like']
            temp_min_kelvin = weather['main']['temp_min']
            temp_max_kelvin = weather['main']['temp_max']
            sunrise_time = dt.datetime.utcfromtimestamp(weather['sys']['sunrise']
                                                        + weather['timezone'])
            sunrise_time = sunrise_time.strftime("%m/%d/%Y, %H:%M:%S")
            sunset_time = dt.datetime.utcfromtimestamp(weather['sys']['sunset']
                                                       + weather['timezone'])
            sunset_time = sunset_time.strftime("%m/%d/%Y, %H:%M:%S")
            # display weather output by user choice
            if user_choice == "c":
                temp = f"{kelvin_to_celsius(temp_kelvin)}(\u2103)"
                feels_like = f"{kelvin_to_celsius(feels_like_kelvin)}(\u2103)"
                temp_min = f"{kelvin_to_celsius(temp_min_kelvin)}(\u2103)"
                temp_max = f"{kelvin_to_celsius(temp_max_kelvin)}(\u2103)"
            elif user_choice == "f":
                temp = f"{kelvin_to_fahrenheit(temp_kelvin)}(\u2109)"
                feels_like = f"{kelvin_to_fahrenheit(feels_like_kelvin)}(\u2109)"
                temp_min = f"{kelvin_to_fahrenheit(temp_min_kelvin)}(\u2109)"
                temp_max = f"{kelvin_to_fahrenheit(temp_max_kelvin)}(\u2109)"
            elif user_choice == "k":
                temp = weather['main']['temp']
                feels_like = weather['main']['feels_like']
                temp_min = weather['main']['temp_min']
                temp_max = weather['main']['temp_max']
            else:
                print("Please enter 'C' for Celsius, 'F' for Fahrenheit., "
                      "or 'K' for Kelvin. ").lower()
    # put info into a dict
            result['Location'] = weather['name']
            result['Temperature'] = temp
            result['Feels like'] = feels_like
            result['Temp_Min'] = temp_min
            result['Temp_Max'] = temp_max
            result['Sunrise Time'] = sunrise_time
            result['Sunset Time'] = sunset_time
            result['Clouds'] = weather['clouds']['all']
            result['Pressure'] = weather['main']['pressure']
            result['Humidity'] = weather['main']['humidity']
            # print(result)
            for key, value in result.items():
                print(f'\n{key: <20}{value}')
            option2 = input("\nDo you want to continue? Type 'Y' to continue 'N' to end. ").lower()
            if option2 == "y":
                continue
            elif option2 == "n":
                print("\nThank you for using our weather program.\n")
                break
            else:
                print("\nInvalid input.Do you want to continue? Type 'Y' to "
                      "continue 'N' to end.").lower()
                continue
        elif option == "n":
            print("\nThank you for using our weather program.\n")
            break
        else:
            print("\nInvalid input. Please enter 'Y' to start, "
                  "'N' to end.\n").lower()
            continue


if __name__ == "__main__":
    main()