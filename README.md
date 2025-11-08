# Calendar Assistant for Farmers

This is a Streamlit application that acts as a Calendar Assistant for Farmers. It leverages the Gemini API to generate farming plans based on user input and allows users to add these plans as events to an interactive calendar. The application supports multiple languages (English, Hindi, Marathi).

## Features

*   **AI-Powered Farming Plans:** Generate detailed farming plans using the Gemini API.
*   **Interactive Calendar:** Add generated plans as events to a calendar.
*   **Multi-language Support:** Switch between English, Hindi, and Marathi.

## Setup Instructions

Follow these steps to get the application up and running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/Madhura-mule25/pccoe1.git
cd pccoe1
```

### 2. Create and Activate a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

Install the necessary Python packages using `pip`:

```bash
pip install -r calender_app/requirements.txt
```

### 4. Configure Gemini API Key

Create a `.env` file in the root directory of the project (e.g., `pccoe1/.env`) and add your Gemini API key:

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

Replace `"YOUR_GEMINI_API_KEY_HERE"` with your actual Gemini API key. You can obtain a key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## How to Run the Application

Once you have completed the setup, you can run the Streamlit application:

1.  **Activate your virtual environment** (if not already active):
    ```bash
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
2.  **Navigate to the project root directory** (if not already there):
    ```bash
    cd pccoe1
    ```
3.  **Run the Streamlit application:**
    ```bash
    streamlit run calender_app/app.py
    ```

The application will open in your web browser.
