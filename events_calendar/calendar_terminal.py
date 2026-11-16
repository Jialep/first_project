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
    while True:
        choice = input("Select 1, 2, 3 or 4: ")
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input, retry")
            continue
        if choice == 1:
            add_event()
        elif choice == 2:
            view_events()
        elif choice == 3:
            delete_event()
        elif choice == 4:
            print("Exiting program")
            return
        elif choice not in choices:
            print("Invalid input, retry")

def add_event():
    while True:
        input_date = input("Enter the date of the event (YYYY-MM-DD): ")
        try:
            input_date = core.format_date(input_date)
        except ValueError as error:
            print(error)
            continue
        input_event = input("Enter the details of the event: ").strip()
        try:
            core.add_event(calendar,input_date,input_event)
        except (ValueError,core.EmptyError) as error:
            print(error)
            continue
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
            events=core.get_events(calendar,input_date)
        except ValueError as error:
            print(error)
            continue
        except core.EmptyError as error:
            print(error)
            return
        print(f"Events on {input_date}:")
        for event in events:
            print(f"- {event}")
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
            events=core.get_events(calendar,input_date)
        except ValueError as error:
            print(error)
            continue
        except core.EmptyError as error:
            print(error)
            return
        for ind,event in enumerate(events, start=1):
            print(f"{ind}. {event}")
        del_event=input(
            "Enter the number of the event you wish to delete:"
            )
        try:
            core.delete_helper(calendar,input_date,del_event)
        except (
            core.MissingError,core.InvalidError,core.EmptyError,ValueError
        )as error:
            print(error)
            continue
        core.save_file(calendar)
        next_del = input('Delete another event? (yes/no): ')
        if next_del.strip().lower() in rejection:
            print("Event(s) deleted successfully.")
            return
        
if __name__=='__main__':
    menu()
