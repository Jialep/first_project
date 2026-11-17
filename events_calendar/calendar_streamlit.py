import json
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
                core.add_event(calendar_data,date_key,event_name)
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
        try:
            day_events = core.get_events(calendar_data,date_key)
        except core.EmptyError as error:
            st.warning(error)
        st.write(f"Events on {date_key}:")
        for event in day_events:
            st.write(f"- {event}")


elif action == 'Delete event':
    selected_date= st.date_input("Choose a date to edit",value=None)
    if selected_date is None:
        st.info('Select a date to view events')
        st.stop()
    date_key=selected_date.strftime('%Y-%m-%d')
    try:
        events = core.get_events(calendar_data,date_key)
    except core.EmptyError as error:
        st.info(error)
        st.stop()
    with st.form('select_event_to_del'):
        selected_event= st.selectbox('Choose event to remove',events)
        submitted = st.form_submit_button('Continue')
    if submitted:
            try:
                event_index=events.index(selected_event)
                event_number=str(event_index+1)
                core.delete_helper(calendar_data,date_key,event_number)
            except (core.MissingError,
                    core.InvalidError,
                    core.EmptyError,
                    ValueError) as error:
                st.error(error)
            else:
                core.save_file(calendar_data)
                st.success(f"Deleted '{selected_event}' from {selected_date}.")
