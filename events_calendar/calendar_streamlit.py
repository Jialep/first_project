import json
from pathlib import Path
import calendar_core as core
import streamlit as st


try:
    calendar_data = core.load_file()
except json.JSONDecodeError as error:
        st.error(f"Could not read {core.CALENDAR_FILE.name}: {error}")
        st.stop()
except ValueError as error:
        st.error(str(error))
        st.stop()


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
            try:
                core.add_event(calendar_data,date_key,day_events)
            except ValueError as error:
                st.warning(error)
            core.save_file(calendar_data)
            st.success(f"Added '{event_name}' for {date_key}.")

elif action == "View events":
    with st.form("view_events_form"):
        event_date = st.date_input("Choose a date to view")
        submitted = st.form_submit_button("View events")

    if submitted:
        date_key = event_date.strftime("%Y-%m-%d")
        day_events = core.get_events(calendar_data,date_key)
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
            core.save_file(calendar_data)
            st.success(f"Deleted '{selected_event}' from {selected_date}.")
