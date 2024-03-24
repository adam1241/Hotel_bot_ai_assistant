# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []



from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
import csv


class ActionCheckWeather(Action):

    def name(self)-> Text:
        return "action_get_weather"
    
    def run(self, dispatcher, tracker, domain):
        api_key = 'Your API Key'
        loc = tracker.get_slot('location')
        current = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(loc, api_key)).json()
        print(current)
        country = current['sys']['country']
        city = current['name']
        condition = current['weather'][0]['main'    ]
        temperature_c = current['main']['temp']
        humidity = current['main']['humidity']
        wind_mph = current['wind']['speed']
        response = """It is currently {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.""".format(condition, city, temperature_c, humidity, wind_mph)
        dispatcher.utter_message(response)
        return [SlotSet('location', loc)]
    

def read_csv_file(name,email):
    filename="Clients.csv"
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            Name = row["name"]
            Email = row["email"]
            if name == Name and Email == email :
                spa = row["spa"] == "True"
                luggage = row["luggage"] == "True"
                cib = row["cib"] == "True"
                bill = float(row["bill"])
                loyalty = row["loyalty"] == "True"
                payment = row["payment"] == "True"
                payment_method = row["payment_method"]
                room_booked = row["room_booked"]
                time_room = row["time_room"]
                extra_bed = row["extra_bed"] == "True"
                
                data.append({
                    "name": Name,
                    "email": Email,
                    "spa": spa,
                    "luggage": luggage,
                    "cib": cib,
                    "bill": bill,
                    "loyalty": loyalty,
                    "payment": payment,
                    "payment_method": payment_method,
                    "room_booked": room_booked,
                    "time_room": time_room,
                    "extra_bed": extra_bed
                })
                return data
            
    return None
def provide_name(name,email):
    data= read_csv_file(name,email)
    if data == None:
        return "you are a new client ,welcome to our hotel ! if you are already a client please ask me to repeat collecting your info"
    else:
        return "welcome back sir, how can i help you?"