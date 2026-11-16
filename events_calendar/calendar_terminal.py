"""
idea: ask for date and then ask for details of event
empty dict, 
"""
import calendar_core as core

rejection = ['no','not really','n','nah','nope','not at all','never','not now','not today','not this time']

try:
    calendar=core.load_file()
except ValueError as error:
    print(f'Could not load calendar: {error}')
    raise SystemExit(1)

def menu():
    print("1. Add Event")
    print("2. View Events")
    print("3. Delete Event")
    print("4. Exit")
    choices = [1, 2, 3, 4]
    choice = input("Select 1, 2, 3 or 4: ")
    while True:
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input, retry")
            choice = input("Select 1, 2, 3 or 4: ")
            continue
        if choice == 1:
            add_event()
            choice = input("Select 1, 2, 3 or 4: ")
        elif choice == 2:
            view_events()
            choice = input("Select 1, 2, 3 or 4: ")
        elif choice == 3:
            delete_event()
            choice = input("Select 1, 2, 3 or 4: ")
        elif choice == 4:
            print("Exiting program")
            return
        elif choice not in choices:
            print("Invalid input, retry")
            choice = input("Select 1, 2, 3 or 4: ")

def add_event():
    while True:
        input_date = input("Enter the date of the event (YYYY-MM-DD): ")
        try:
            input_date = core.format_date(input_date)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            continue
        input_event = input("Enter the details of the event: ").strip()
        if input_event == "":
            print("Event details cannot be empty. Please enter valid details.")
            continue
        if input_date in calendar:
            if input_event in calendar[input_date]:
                print("This event already exists on this date.")
                continue
            calendar[input_date] += [input_event]
        else:
            calendar[input_date] = [input_event]
        core.save_file(calendar)
        next_event = input("Add another event? (yes/no): ")
        if next_event.strip().lower() in rejection:
            print("Event(s) added successfully.")
            return

def view_events():
    while True:
        input_date = input("Enter the date to view events (YYYY-MM-DD): ")
        try:
            input_date = core.format_date(input_date)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            continue
        if input_date in calendar:
            events=core.get_events(calendar,input_date)
            if not events:
                print(f"No events found on {input_date}.")
            else:
                print(f"Events on {input_date}:")
                for event in events:
                    print(f"- {event}")
        else:
            print(f"No events found on {input_date}.")
        next_view = input("View events for another date? (yes/no): ")
        if next_view.strip().lower() in rejection:
            print("Finished viewing events.")
            return

def delete_event():
    while True:
        input_date = input("Enter the date of the event you wish to delete\n" \
        "(YYYY-MM-DD): ")
        try:
            input_date = core.format_date(input_date)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            continue
        if input_date not in calendar:
            print(f'No events found on {input_date}.')
            return
        if not calendar[input_date]:
            print(f"No events found on {input_date}.")
            print("Returning to main menu.")
            return
        print(f"Events on {input_date}:")
        for ind,event in enumerate(calendar[input_date], start=1):
            print(f"{ind}. {event}")
        try:
            del_event = int(input("Enter the number of the event you wish to delete:"))
        except ValueError:
            print("Invalid input. Please enter a valid event number.")
            continue
            
        if core.invalid_delete(del_event,calendar,input_date):
            print("Invalid event number. Please enter a valid event number.")
            continue
        core.pop_event(calendar,del_event,input_date)
        core.save_file(calendar)
        next_del = input('Delete another event? (yes/no): ')
        if next_del.strip().lower() in rejection:
            print("Event(s) deleted successfully.")
            return
        
if __name__=='__main__':
    menu()
