# Tour Planning Assistant

## Description
This project is an AI-powered tour planning assistant designed to help users plan their trips by providing comprehensive itineraries, cuisine recommendations, and real-time weather information.

## Features
*   **Itinerary Planning:** Generates detailed tour plans based on user preferences.
*   **Cuisine Agent:** Suggests local dishes and restaurants.
*   **Weather Service:** Provides current weather updates for planned destinations.

## Prerequisites
*   Python 3.x
*   pip (Python package installer)

## Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repository-url>
    cd julep-workflow
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

This project uses a `.env` file for managing environment variables, such as API keys or other configuration settings.

1.  Create a file named `.env` in the root directory of the project.
2.  Add the necessary environment variables to this file. For example:
    ```env
    JULEP_API_KEY="your_julep_api_key_here"
    # Add other necessary configurations
    ```
    Refer to the specific modules (`weather_service.py`, `cuisine_agent.py`) for required API keys or settings.

## Usage

To run the application, execute the `main.py` script from the root directory:

```bash
python main.py [arguments]
```

Replace `[arguments]` with any required command-line arguments for the `main.py` script. Check `main.py` for details on available arguments.


