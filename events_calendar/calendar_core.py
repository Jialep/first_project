'''
purpose of this core is to refactor code, converting hard coded checks
into functions which can be accessed by every interface through importing
'''
#calendar_configuration_with_env_file
from datetime import datetime
import json
import os
from pathlib import Path
from dotenv import load_dotenv
PROJECT_ROOT = Path(__file__).resolve().parent.parent 
#moves file call up the repo, twice cus its in a file in a file
load_dotenv(PROJECT_ROOT / '.env') #loads env file
CALENDAR_FILE = (
    PROJECT_ROOT / os.environ['CALENDAR_FILE'] #retrieves configured file name from path call
).resolve()
#end_of_configuration

def get_events(calendar_data,date_key): #takes in dict and key
    return calendar_data.get(date_key,[]) #return value else [] if not key
def format_date(input_date):
    date=datetime.strptime(input_date, '%Y-%m-%d')
    formatted_date= date.strftime('%Y-%m-%d')
    return formatted_date
def invalid_delete(del_event,calendar_data,input_date):
    if del_event < 1 or del_event > len(calendar_data[input_date]):
        return True
    return False
def pop_event(calendar_data,del_event,input_date):
    calendar_data[input_date].pop(del_event-1)
    return
def save_file(data):
    with CALENDAR_FILE.open("w",encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    return
def load_file():
    try:
        with CALENDAR_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return {}
    if not isinstance(data, dict) or any(
        not isinstance(day, str)
        or not isinstance(events, list)
        or any(not isinstance(event, str) for event in events)
        for day, events in data.items()
        ):
        raise ValueError (f"{CALENDAR_FILE.name} has an invalid format.")
    return data
    