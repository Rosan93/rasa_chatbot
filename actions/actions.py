# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import os 
import pymongo

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


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

class QueryCollegeInfo(Action):

    def name(self) -> Text:
        return "query_college_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        slot_college_name = "NIST"
        tmp_slot_name = tracker.get_slot("college_name")
        print(f"Slot value: {tmp_slot_name}")
        college_info = self.get_college_info(college_name=slot_college_name)

        dispatcher.utter_message(text=str(college_info))

        return []

    @staticmethod
    def mongodb_connect(db_name, collection_name):
        try: 
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client[db_name]
            my_collection = db[collection_name]

            return my_collection
        
        except:
            print(f"Error During connection")

    def get_college_info(self, college_name):
        college_data = self.mongodb_connect(db_name="rasa_db", collection_name="college_info")
        
        college_info = list(college_data.find({"college_name": college_name}))
        
        return college_info

