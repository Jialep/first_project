import json
from pathlib import Path
from calendar_core import get_events
import streamlit as st


CALENDAR_FILE = Path(__file__).with_name("calendar.json")


def load_calendar() -> dict[str, list[str]]:
    try:
        with CALENDAR_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as error:
        st.error(f"Could not read {CALENDAR_FILE.name}: {error}")
        st.stop()

    if not isinstance(data, dict) or any(
        not isinstance(day, str)
        or not isinstance(events, list)
        or any(not isinstance(event, str) for event in events)
        for day, events in data.items()
    ):
        st.error(f"{CALENDAR_FILE.name} has an invalid format.")
        st.stop()

    return data


def save_calendar(events_by_date: dict[str, list[str]]) -> None:
    with CALENDAR_FILE.open("w", encoding="utf-8") as file:
        json.dump(events_by_date, file, indent=4)


calendar_data = load_calendar()

st.title("Daily schedule calendar")
st.subheader("Welcome! Add, view, or delete your calendar events.")

action = st.radio(
    "Choose an action:",
    ("Add event", "View events", "Delete event"),
    horizontal=True,
)

if action == "Add event":
    with st.form("add_event_form"):
        event_date = st.date_input("Event date")
        event_name = st.text_input("Event details")
        submitted = st.form_submit_button("Add event")

    if submitted:
        event_name = event_name.strip()
        if not event_name:
            st.error("Event details cannot be empty.")
        else:
            date_key = event_date.strftime("%Y-%m-%d")
            day_events = calendar_data.setdefault(date_key, [])
            if event_name in day_events:
                st.warning("This event already exists on that date.")
            else:
                day_events.append(event_name)
                save_calendar(calendar_data)
                st.success(f"Added '{event_name}' for {date_key}.")

elif action == "View events":
    with st.form("view_events_form"):
        event_date = st.date_input("Choose a date to view")
        submitted = st.form_submit_button("View events")

    if submitted:
        date_key = event_date.strftime("%Y-%m-%d")
        day_events = get_events(calendar_data,date_key)
        if day_events:
            st.write(f"Events on {date_key}:")
            for event in day_events:
                st.write(f"- {event}")
        else:
            st.info(f"No events found on {date_key}.")

else:
    dates_with_events = sorted(
        (day for day, events in calendar_data.items() if events),
        reverse=True,
    )

    if not dates_with_events:
        st.info("There are no events to delete.")
    else:
        selected_date = st.selectbox("Choose a date", dates_with_events)
        with st.form("delete_event_form"):
            selected_event = st.selectbox(
                "Choose the event to delete",
                calendar_data[selected_date],
            )
            submitted = st.form_submit_button("Delete event")

        if submitted:
            calendar_data[selected_date].remove(selected_event)
            save_calendar(calendar_data)
            st.success(f"Deleted '{selected_event}' from {selected_date}.")
