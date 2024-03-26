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
import re
from datetime import datetime

import requests
import csv

class CheckName(Action):
    def name(self) -> Text:
        return "check_name_email"

    def read_csv_file(self, name: Text, email: Text) -> List[Dict[Text, Any]]:
        filename = "Clients.csv"
        data = []
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row["name"] == name and row["email"] == email:
                    data.append({
                        "name": row["name"],
                        "email": row["email"],
                        "spa": row["spa"] == "True",
                        "luggage": row["luggage"] == "True",
                        "cib": row["cib"] == "True",
                        "bill": float(row["bill"]),
                        "loyalty": row["loyalty"] == "True",
                        "payment": row["payment"] == "True",
                        "payment_method": row["payment_method"],
                        "room_booked": row["room_booked"],
                        "time_room": row["time_room"],
                        "extra_bed": row["extra_bed"] == "True"
                    })
        return data
    def addClient(self, name,email, room_booked, time_room,extra_bed) :
        # Append the new booking to the Clients.csv file
        with open("Clients.csv", "a", newline="") as file:
            writer = csv.writer(file)
            print("i am adding a row")
            writer.writerow([name, email, "False", "False", "False", "", "False", "True", "credit card", "false", time_room, "false"])

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        data = self.read_csv_file(name, email)
        room_booked=tracker.get_slot("date")
        time_room=tracker.get_slot("time_room")
        extra_bed=tracker.get_slot("extra_bed")
        if not data:
            self.addClient(name,email, room_booked, time_room,extra_bed) 
            dispatcher.utter_message("You are a new client, welcome to our hotel! If you are already a client, please ask me to repeat collecting your info.")
        else:
            dispatcher.utter_message("Welcome back sir, how can I help you?")
        return []

        
class ActionResponseToDate(Action):

    def name(self)-> Text:
        return "action_response_to_date"
    
    def extract_dates(self,text) :
        # Regular expression to match dates in the format YYYY/MM/DD
        date_regex = r"(\d{4}([/.-])\d{1,2}([/.-])\d{1,2})"
        matches = re.findall(date_regex, text)
        dates = []
        for match in matches:
            try:
                separator = match[1]
                # Determine the correct date format based on the separator
                if separator == "-":
                    date_format = "%Y-%m-%d"
                elif separator == ".":
                    date_format = "%Y.%m.%d"
                elif separator == "/":
                    date_format = "%Y/%m/%d"
                else:
                    date_format = "%Y-%m-%d"
                date_obj = datetime.strptime(match[0], date_format).date()
                dates.append(date_obj)
            except ValueError:
                pass 
        if dates : 
            dates.sort()
        return dates
    
    def extract_rooms(self,in_date,out_date) :
        available_rooms = []
        with open('rooms.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for line in csv_reader:
                dates = line[1].split(',')
                available = True
                for date_str in dates:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    print(date)
                    if in_date <= date <= out_date:
                        available = False
                        break  # Once a date within range is found, move to the next room
                if available :
                    available_rooms.append({"id" : line[0], "Type" : line[2], "View type" : line[5], "Price" : line[4], "Capacity" : line[3]})
        return available_rooms
            
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_response = tracker.latest_message.get("text")
        dates = self.extract_dates(user_response)
        message = ""
        if len(dates) == 0 :
            message = "Please provide two correct dates in the format YYYY-MM-DD or YYYY/MM/DD"
        elif len(dates) == 1 :
            message = "You provided only one date, please provide two correct dates in the format YYYY-MM-DD or YYYY/MM/DD"
        elif len(dates) == 2 :
            rooms = self.extract_rooms(dates[0],dates[1])
            message = f"Here are the available rooms from {dates[0]} to {dates[1]}: {rooms}"
        else : 
            message = "Too many dates provided"

        dispatcher.utter_message(message)
        return [SlotSet("matches", message)]






class AddToClients(Action):
    def name(self) -> Text:
        return "action_add_to_clients"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        room_booked = tracker.get_slot("room_booked")
        time_room = tracker.get_slot("time_room")
        extra_bed = tracker.get_slot("extra_bed")

        # Append the new booking to the Clients.csv file
        with open("Clients.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, email, "False", "False", "False", "", "False", "True", "credit card", room_booked, time_room, "false"])

        dispatcher.utter_message("Your booking has been successfully added to our records.")

        return []
