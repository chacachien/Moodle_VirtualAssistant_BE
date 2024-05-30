
# Moodle_VirtualAssistant_BE

## Modules Overview

### Active Module

The Active Module provides real-time alerts and reminders, ensuring users stay on top of their tasks and notifications. It is designed to engage users with timely and relevant information proactively.

#### Features:

1. **Real-Time Notifications:**
   - Instantly notify users about new messages, updates, or important events as they occur.
   - Ensure critical information is delivered promptly to keep users informed.

2. **Daily Reminders:**
   - Schedule and send daily reminders for tasks, meetings, or any important activities.
   - Customize reminder settings to fit the user’s preferences and schedule.

### Passive Module

The Passive Module enhances user interaction by supporting various roles: Talk, Rag, and Query. This module is designed to respond to user inputs and provide assistance as needed.

#### Roles:

1. **Talk:**
   - Engage in natural language conversations with users.
   - Answer questions, provide information, and assist with general queries.
   - Use NLP (Natural Language Processing) to understand and respond to user inputs effectively.

2. **Rag:**
   - Implement role-playing scenarios where the chatbot can simulate different characters or roles.
   - Use case-based responses to provide a more interactive and engaging user experience.

3. **Query:**
   - Handle specific user queries related to data retrieval, such as fetching information from a database or providing detailed answers to specific questions.
   - Efficiently process and respond to queries, ensuring users receive accurate and relevant information quickly.


## Requirements

Before running the application, ensure you have the following dependencies installed:

- Python 3.12
- Poetry


## Create venv

```bash
python3 -m venv venv
source venv/bin/activate
```


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/chacachien/Moodle_VirtualAssistant_BE
    ```

2. Navigate to the project directory:

    ```bash
    cd <project_directory>
    ```

3. Install the dependencies using Poetry:

    ```bash
    poetry install
    ```

## Usage

To run the FastAPI application, execute the following command:

```python
    python3 app/main.py
```
    
