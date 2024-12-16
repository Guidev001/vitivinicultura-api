# FastAPI Project

This is a simple FastAPI project that provides a basic API endpoint.

## Requirements

The project dependencies are listed in the `requirements.txt` file. To install them, run:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the FastAPI application, use the following command:

```bash
uvicorn app.main:app --reload
```

This will start the server on `http://127.0.0.1:8000`.

## API Endpoints

### GET /

Returns a simple JSON response.

- **URL:** `/`
- **Method:** `GET`
- **Response:**
  - `200 OK`: `{"Hello": "World"}`

## Project Structure

```
.
├── app
│   └── main.py
├── requirements.txt
└── README.md
```

- `app/main.py`: Contains the FastAPI application code.
- `requirements.txt`: Lists the project dependencies.
- `README.md`: Project documentation (this file).
