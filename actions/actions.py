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


class ActionResponseToDate(Action):

    def name(self)-> Text:
        return "action_response_to_date"
    
    def extract_dates(text) :
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
    
    def extract_rooms(in_date,out_date) :
        pass
            
        
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_response = tracker.latest_message.get("text")
        dates = self.extract_dates(user_response)
        rooms = None
        message = ""
        if len(dates) == 0 :
            message = "Please provide two correct dates in the format YYYY-MM-DD or YYYY/MM/DD"
        elif len(dates) == 1 :
            message = "You provided only one date, please provide two correct dates in the format YYYY-MM-DD or YYYY/MM/DD"
        elif len(dates) == 2 :
            message = "Here are the available rooms from {dates[0]} to {dates[1]}: {rooms}"
        else : 
            message = "Too many dates provided"

        dispatcher.utter_message(message)
        return []