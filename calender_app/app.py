
import streamlit as st
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from streamlit_calendar import calendar
from streamlit_modal import Modal

load_dotenv()

# --- Gemini API Setup ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# --- Streamlit App ---
st.title("Gemini Calendar Assistant for Farmers")

# --- Initialize Calendar Events and Modal ---
if 'events' not in st.session_state:
    st.session_state.events = []

modal = Modal("Event Details", key="event_details_modal")

# --- User Input ---
st.header("Get a Farming Plan")
st.write("Ask for a farming plan, and Gemini will help you.")
st.write("For example: 'What is a good plan for planting tomatoes in a 1-acre field?'")

prompt = st.text_input("Enter your farming question:")

if st.button("Get Plan"):
    st.session_state.prompt = prompt

if 'prompt' in st.session_state and st.session_state.prompt:
    # Create a more specific prompt for Gemini
    gemini_prompt = f"""
    As a farming expert, create a concise plan for the following task. Provide the output in a single, valid JSON object with two keys: 'heading' and 'plan'.
    The 'heading' should be a short, easy-to-understand title for the task (less than 5 words).
    The 'plan' should be a detailed, step-by-step plan.

    Example output format:
    {{
        "heading": "Tomato Planting Plan",
        "plan": "1. Prepare the soil by adding compost.\n2. Plant the tomato seedlings 2 feet apart.\n3. Water the seedlings regularly."
    }}

    Task: {st.session_state.prompt}
    """

    try:
        response = model.generate_content(gemini_prompt)
        # Clean the response to ensure it is a valid JSON string
        cleaned_response = response.text.strip().replace('\n', '').replace('```json', '').replace('```', '')
        plan_data = json.loads(cleaned_response)

        if isinstance(plan_data, dict) and 'heading' in plan_data and 'plan' in plan_data:
            st.session_state.plan_data = plan_data
            st.session_state.prompt = None  # Clear the prompt
        else:
            st.error("The AI response was not in the expected format. Please try again.")

    except json.JSONDecodeError:
        st.error("Sorry, I couldn't generate a valid plan. The AI response was not in the expected JSON format. Please try again.")
    except Exception as e:
        st.error(f"An error occurred while generating the plan: {e}")

if 'plan_data' in st.session_state:
    st.subheader("Generated Plan")
    st.write("**Heading:**")
    edited_heading = st.text_input("", st.session_state.plan_data['heading'])
    st.write("**Plan:**")
    edited_plan = st.text_area("", st.session_state.plan_data['plan'], height=200)

    event_date = st.date_input("Select a date for the event")

    if st.button("Add Event to Calendar"):
        event_start = f"{event_date}T09:00:00"
        event_end = f"{event_date}T10:00:00"
        event = {
            "title": edited_heading,
            "start": event_start,
            "end": event_end,
            "extendedProps": {
                "plan": edited_plan
            }
        }
        st.session_state.events.append(event)
        del st.session_state.plan_data  # Clear the plan data after adding the event

# --- Display Calendar ---
st.header("Your Farming Calendar")

calendar_options = {
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay",
    },
    "initialView": "dayGridMonth",
    "events": st.session_state.events,
    "editable": True,
    "selectable": True,
    "height": "800px",
    "eventClick": "function(info) { st.session_state.event_details_modal = true; st.session_state.selected_event = info.event.extendedProps.plan; }"
}

calendar = calendar(events=st.session_state.events, options=calendar_options)

if modal.is_open():
    with modal.container():
        st.subheader("Event Plan")
        st.write(st.session_state.get("selected_event", ""))
