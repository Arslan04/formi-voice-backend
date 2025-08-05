# Formi Resorts Voice AI Project

## Project Overview

This project implements a voice-based AI assistant for Formi Resorts using the Retell AI platform integrated with a custom FastAPI backend. The system enables real-time phone interactions to handle customer queries related to bookings, hotel policies, discounts, staff inquiries, and more.

The backend APIs are designed to deliver information in token-limited chunks (≤800 tokens) to comply with Retell AI and LLM limitations, maintain session context, and prevent hallucinations. Calls are logged to Google Sheets for auditing and analytics.

---

## Features

- **Intent Classification API** (`/classify-query`): Classifies user queries into supported intents like booking, policy, discount, etc.
- **Information Retrieval API** (`/retrieve-info`): Returns relevant information in manageable chunks based on the query intent.
- **Conversation Logging API** (`/log-conversation`): Logs detailed call metadata and summaries into a Google Sheet.
- **Session Management:** Maintains session IDs to retain context across multi-turn conversations.
- **Token Chunking:** Ensures API responses respect the 800-token limit.
- **Google Sheets Integration:** For data storage and analytics.
- **Retell AI Integration:** Conversation flow leveraging Retell AI custom functions and logic to deliver a natural voice experience.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Google Cloud service account credentials JSON for Google Sheets API
- ngrok (optional for exposing localhost)
- Retell AI account (for the voice agent)

### Setup

1. Clone the repository:

2. Install Python dependencies:


3. Place your Google Sheets service account credentials JSON file in the project folder and update any paths in `sheetlogger.py`.

4. Configure environment variables as needed, for example:
export RETELL_API_KEY="your_retell_api_key"
export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_credentials.json"

5. Run the FastAPI server:

uvicorn main:app --reload --port 8000

6. Use ngrok to expose your local backend (optional):

ngrok http 8000


7. Update Retell AI custom functions with your ngrok-generated URLs or deployed backend URLs.

---

## API Endpoints

- **POST `/classify-query`**

  Input:

{
"query": "User spoken query text",
"session_id": "optional-session-id"
}


Output:

{
"session_id": "generated-or-passed-session-id",
"intent": "detected_intent"
}



- **POST `/retrieve-info`**

Input:

{
"session_id": "session-id",
"intent": "detected_intent",
"chunk_id": 0,
"guest_count": 2,
"check_in": "2025-08-01",
"check_out": "2025-08-05",
"room_name": "Executive Room"
}



Output:

{
"data": "Information chunk text...",
"has_more": true,
"next_chunk_id": 1
}



- **POST `/log-conversation`**

Input:

{
"call_time": "2025-08-01T10:00:00",
"phone_number": "9876500001",
"call_outcome": "Booking",
"customer_name": "John Doe",
"room_name": "Executive Room",
"check_in": "2025-08-01",
"check_out": "2025-08-05",
"number_of_guests": 2,
"call_summary": "User requested booking and info was provided."
}



Output:

{
"status": "Conversation logged successfully"
}




## Data Files

CSV files used for information sources:

- `discount.csv`
- `hotel_rules.csv`
- `room_information.csv`
- `room_pricing.csv`
- `staff_queries.csv`

These files contain structured data loaded at application startup.

---

## How to Test

- Use the FastAPI interactive docs at `http://localhost:8000/docs` to test API endpoints.
- Use ngrok URLs to connect Retell AI custom functions.
- Simulate calls in Retell AI to verify multi-turn conversational flows and chunked responses.

---

## Future Work

- Complete chunk looping in Retell AI flow to handle multi-part responses fully.
- Integrate Twilio to enable real phone calls.
- Add advanced caching for popular queries.
- Build a admin dashboard for call logs analysis.

---






fastapi and uvicorn: For backend server and ASGI running.

pydantic: For request/response validation.

pandas and numpy: For CSV data loading and processing.

gspread and google-auth: For Google Sheets API integration.

tiktoken: For token counting/chunking (OpenAI token encoder).

requests: For any direct HTTP requests you may make.

python-dotenv: If you use .env for environment variables.



