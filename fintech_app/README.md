# Fintech App

This is a backend application for a fintech mobile app, built with FastAPI.

## Getting Started

### Prerequisites

- Python 3.10+
- Poetry

### Installation

1.  **Clone the repository and navigate to the `fintech_app` directory:**

    ```bash
    git clone https://github.com/restackio/examples-python
    cd examples-python/fintech_app
    ```

2.  **Install the dependencies using Poetry:**

    ```bash
    poetry install
    ```

### Running the Application

1.  **Create a `.env` file** in the `fintech_app` directory and add the following line:

    ```
    SECRET_KEY=my-super-secret-key
    ```

2.  **Run the FastAPI server:**

    ```bash
    poetry run uvicorn src.main:app --reload
    ```

    The application will be available at `http://127.0.0.1:8000`.

### Running the Tests

To run the tests, use the following command:

```bash
poetry run pytest
```
