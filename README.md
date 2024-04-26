# FastAPI Application

## Overview

This is a FastAPI application designed to create a virtual assistant chatbot.

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
    git clone <repository_url>
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

```bash
  uvicorn main:app --reload --port 8000
