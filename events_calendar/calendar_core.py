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
class MissingError(Exception):
    pass
class InvalidError(Exception):
    pass
class EmptyError(Exception):
    pass
#main_functions
def add_event(calendar_data,date_key,event_name):
    event_name=event_name.strip()
    if not event_name:
        raise EmptyError ("Event details cannot be empty. Please enter valid details.")
    if date_key in calendar_data:
        if event_name in calendar_data[date_key]:
            raise ValueError ("This event already exists on this date.")
        calendar_data[date_key]+=[event_name]
    else:
        calendar_data[date_key] = [event_name]

def delete_helper(calendar_data,input_date,selected):
    if input_date not in calendar_data:
        raise MissingError (f'No events found on {input_date}.')
    if not calendar_data[input_date]:
        raise EmptyError (f"No events found on {input_date}, Returning to main menu.")
    if not selected.isdigit():
        raise InvalidError ("Invalid input. Please enter a valid event number.")
    selected=int(selected)
    if selected < 1 or selected > len(calendar_data[input_date]):
        raise ValueError ("Invalid event number. Please enter a valid event number.")
    calendar_data[input_date].pop(selected-1)

#helper_functions
def get_events(calendar_data,date_key): #takes in dict and key
    if not calendar_data.get(date_key,[]):
        raise EmptyError (f"No events found on {date_key}, Returning to main menu.")
    return calendar_data.get(date_key,[]) #return value else [] if not key
def format_date(input_date):
    try:
        date=datetime.strptime(input_date, '%Y-%m-%d')
        formatted_date= date.strftime('%Y-%m-%d')
    except ValueError:
        raise ValueError ("Invalid date format. Please use YYYY-MM-DD.")
    return formatted_date

#file_loading_and_saving
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
    