
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

# --- Translations ---
translations = {
    "en": {
        "title": "Gemini Calendar Assistant for Farmers",
        "get_plan_header": "Get a Farming Plan",
        "get_plan_write": "Ask for a farming plan, and Gemini will help you.",
        "get_plan_example": "For example: 'What is a good plan for planting tomatoes in a 1-acre field?'",
        "enter_question": "Enter your farming question:",
        "get_plan_button": "Get Plan",
        "generated_plan_header": "Generated Plan",
        "heading_label": "Heading:",
        "plan_label": "Plan:",
        "select_date": "Select a date for the event",
        "select_start_time": "Select a start time for the event",
        "select_end_time": "Select an end time for the event",
        "add_event_button": "Add Event to Calendar",
        "calendar_header": "Your Farming Calendar",
        "event_plan_header": "Event Plan",
        "language_select": "Language"
    },
    "hi": {
        "title": "किसानों के लिए जेमिनी कैलेंडर सहायक",
        "get_plan_header": "खेती की योजना प्राप्त करें",
        "get_plan_write": "खेती की योजना के लिए पूछें, और जेमिनी आपकी मदद करेगा।",
        "get_plan_example": "उदाहरण के लिए: '1 एकड़ खेत में टमाटर लगाने की अच्छी योजना क्या है?'",
        "enter_question": "अपना खेती का प्रश्न दर्ज करें:",
        "get_plan_button": "योजना प्राप्त करें",
        "generated_plan_header": "उत्पन्न योजना",
        "heading_label": "शीर्षक:",
        "plan_label": "योजना:",
        "select_date": "घटना के लिए एक तारीख चुनें",
        "select_start_time": "घटना के लिए एक başlangıç saati seçin",
        "select_end_time": "घटना के लिए एक bitiş saati seçin",
        "add_event_button": "कैलेंडर में घटना जोड़ें",
        "calendar_header": "आपका खेती कैलेंडर",
        "event_plan_header": "घटना योजना",
        "language_select": "भाषा"
    },
    "mr": {
        "title": "शेतकऱ्यांसाठी जेमिनी दिनदर्शिका सहाय्यक",
        "get_plan_header": "शेतीची योजना मिळवा",
        "get_plan_write": "शेती योजनेसाठी विचारा, आणि जेमिनी तुम्हाला मदत करेल.",
        "get_plan_example": "उदाहरणार्थ: '१ एकर शेतात टोमॅटो लावण्याची चांगली योजना कोणती आहे?'",
        "enter_question": "तुमचा शेती प्रश्न प्रविष्ट करा:",
        "get_plan_button": "योजना मिळवा",
        "generated_plan_header": "तयार केलेली योजना",
        "heading_label": "शीर्षक:",
        "plan_label": "योजना:",
        "select_date": "कार्यक्रमासाठी एक तारीख निवडा",
        "select_start_time": "कार्यक्रमासाठी प्रारंभ वेळ निवडा",
        "select_end_time": "कार्यक्रमासाठी समाप्ती वेळ निवडा",
        "add_event_button": "दिनदर्शिकेत कार्यक्रम जोडा",
        "calendar_header": "तुमची शेती दिनदर्शिका",
        "event_plan_header": "कार्यक्रमाची योजना",
        "language_select": "भाषा"
    }
}

# --- Streamlit App ---
st.set_page_config(layout="wide")

# --- Language Selection ---
if 'lang' not in st.session_state:
    st.session_state.lang = "en"

st.sidebar.title(translations[st.session_state.lang]["language_select"])
lang_options = {"English": "en", "हिन्दी": "hi", "मराठी": "mr"}
selected_lang_display = st.sidebar.selectbox("", list(lang_options.keys()))
st.session_state.lang = lang_options[selected_lang_display]

st.title(translations[st.session_state.lang]["title"])

# --- Initialize Calendar Events and Modal ---
if 'events' not in st.session_state:
    st.session_state.events = []

modal = Modal(translations[st.session_state.lang]["event_plan_header"], key="event_details_modal")

# --- User Input ---
st.header(translations[st.session_state.lang]["get_plan_header"])
st.write(translations[st.session_state.lang]["get_plan_write"])
st.write(translations[st.session_state.lang]["get_plan_example"])

prompt = st.text_input(translations[st.session_state.lang]["enter_question"])

if st.button(translations[st.session_state.lang]["get_plan_button"]):
    st.session_state.prompt = prompt

if 'prompt' in st.session_state and st.session_state.prompt:
    # Create a more specific prompt for Gemini
    gemini_prompt = f"""
    As a farming expert, create a concise plan for the following task. Provide the output in a single, valid JSON object.
    The plan should be in {st.session_state.lang} language.
    The JSON object should have two keys: 'heading' and 'plan'.
    The 'heading' should be a short, easy-to-understand title for the task (less than 5 words).
    The 'plan' should be a list of steps, where each step is an object with the following keys: 'step_number', 'title', and 'description'.

    Example output format:
    {{
        "heading": "Tomato Planting Plan",
        "plan": [
            {{
                "step_number": 1,
                "title": "Soil Preparation",
                "description": "Prepare the soil by adding compost and tilling to a depth of 6 inches."
            }},
            {{
                "step_number": 2,
                "title": "Planting Seedlings",
                "description": "Plant the tomato seedlings 2 feet apart in rows, ensuring the root ball is covered."
            }},
            {{
                "step_number": 3,
                "title": "Watering",
                "description": "Water the seedlings regularly, keeping the soil moist but not waterlogged."
            }}
        ]
    }}

    Task: {st.session_state.prompt}
    """

    try:
        response = model.generate_content(gemini_prompt)
        # Clean the response to ensure it is a valid JSON string
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        plan_data = json.loads(cleaned_response)

        if isinstance(plan_data, dict) and 'heading' in plan_data and 'plan' in plan_data and isinstance(plan_data['plan'], list):
            st.session_state.plan_data = plan_data
            st.session_state.prompt = None  # Clear the prompt
        else:
            st.error("The AI response was not in the expected format. Please try again.")

    except json.JSONDecodeError:
        st.error("Sorry, I couldn't generate a valid plan. The AI response was not in the expected JSON format. Please try again.")
    except Exception as e:
        st.error(f"An error occurred while generating the plan: {e}")

if 'plan_data' in st.session_state:
    st.subheader(translations[st.session_state.lang]["generated_plan_header"])
    st.write(f"**{translations[st.session_state.lang]['heading_label']}**")
    edited_heading = st.text_input("", st.session_state.plan_data['heading'])
    
    st.write(f"**{translations[st.session_state.lang]['plan_label']}**")
    for i, step in enumerate(st.session_state.plan_data['plan']):
        st.write(f"**Step {step['step_number']}: {step['title']}**")
        st.session_state.plan_data['plan'][i]['description'] = st.text_area("", step['description'], height=100, key=f"step_{i}")

    # Combine the plan into a single string for the calendar event
    edited_plan = ""
    for step in st.session_state.plan_data['plan']:
        edited_plan += f"Step {step['step_number']}: {step['title']}\n{step['description']}\n\n"

    event_date = st.date_input(translations[st.session_state.lang]["select_date"])
    start_time = st.time_input(translations[st.session_state.lang]["select_start_time"])
    end_time = st.time_input(translations[st.session_state.lang]["select_end_time"])

    if st.button(translations[st.session_state.lang]["add_event_button"]):
        event_start = f"{event_date}T{start_time}"
        event_end = f"{event_date}T{end_time}"
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
st.header(translations[st.session_state.lang]["calendar_header"])

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
    "locale": st.session_state.lang,
}

calendar_output = calendar(events=st.session_state.events, options=calendar_options, callbacks=["eventClick"])

if calendar_output and calendar_output.get("callback") == "eventClick":
    st.session_state.selected_event = calendar_output.get("event", {}).get("extendedProps", {}).get("plan", "")
    modal.open()

if modal.is_open():
    with modal.container():
        st.subheader(translations[st.session_state.lang]["event_plan_header"])
        st.write(st.session_state.get("selected_event", ""))
