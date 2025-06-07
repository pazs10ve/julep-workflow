# Tour Planning Assistant

## Description
This project is an AI-powered tour planning assistant designed to help users plan their trips by providing comprehensive itineraries, cuisine recommendations, and real-time weather information. It now features a web interface powered by a FastAPI backend and a React frontend.

## Features
*   **Itinerary Planning:** Generates detailed tour plans based on user preferences.
*   **Cuisine Agent:** Suggests local dishes and restaurants.
*   **Weather Service:** Provides current weather updates for planned destinations.
*   **Web API:** FastAPI backend serving tour planning functionalities.
*   **React Frontend:** Interactive user interface to plan tours.

## Prerequisites
*   Python 3.x
*   pip (Python package installer)
*   Node.js (v14 or newer recommended)
*   npm (comes with Node.js) or Yarn

## Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repository-url>
    cd julep-workflow
    ```

2.  **Backend Setup (Python):**
    a.  **Create a virtual environment:**
        ```bash
        python -m venv .venv
        ```
    b.  **Activate the virtual environment:**
        *   On Windows:
            ```bash
            .venv\Scripts\activate
            ```
        *   On macOS/Linux:
            ```bash
            source .venv/bin/activate
            ```
    c.  **Install Python dependencies:**
        ```bash
        pip install -r requirements.txt
        ```

3.  **Frontend Setup (React):**
    a.  **Navigate to the frontend directory:**
        ```bash
        cd frontend
        ```
    b.  **Install JavaScript dependencies:**
        ```bash
        npm install
        ```
        (or `yarn install` if you prefer Yarn)
    c.  **Return to the project root directory:**
        ```bash
        cd ..
        ```

## Configuration

This project uses a `.env` file in the root directory for managing environment variables, such as API keys or other configuration settings.

1.  Ensure a file named `.env` exists in the root project directory (`julep-workflow/.env`).
2.  Add the necessary environment variables to this file. For example:
    ```env
    JULEP_API_KEY="your_julep_api_key_here"
    OPENWEATHERMAP_API_KEY="your_openweathermap_api_key"
    # Add other necessary configurations for services like cuisine_agent if needed
    ```
    Refer to the specific modules (`weather_service.py`, `cuisine_agent.py`) for required API keys or settings.

## Usage

The application consists of a backend API server and a frontend client.

### 1. Running the Backend (FastAPI Server)

*   Ensure your Python virtual environment is activated.
*   Navigate to the project root directory (`julep-workflow`).
*   Start the FastAPI server by running `app.py`:
    ```bash
    python app.py
    ```
    This will typically start the server on `http://localhost:8000` (as configured in `app.py`).

### 2. Running the Frontend (React App)

*   Open a new terminal or command prompt.
*   Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
*   Start the React development server:
    ```bash
    npm start
    ```
    This will usually open the application in your default web browser at `http://localhost:3000`.

### 3. Command-Line Interface (Original `main.py`)

If you need to use the original command-line interface (e.g., for specific tasks not yet exposed via the web UI):

*   Ensure your Python virtual environment is activated.
*   Navigate to the project root directory (`julep-workflow`).
*   Execute the `main.py` script:
    ```bash
    python main.py [arguments]
    ```
    Replace `[arguments]` with any required command-line arguments for the `main.py` script. Check `main.py` for details on available arguments.
