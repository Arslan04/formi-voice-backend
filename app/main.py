from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
from datetime import datetime

from app import utils
from app.services import data_loader, google_sheets_logger, info_retriever, query_classifier, session_manager

app = FastAPI()
data = data_loader.DataLoader()
data.load_all()

# ------------------- Models -------------------

class QueryRequest(BaseModel):
    session_id: Optional[str]
    query: str = Field(..., min_length=1)

class RetrieveInfoRequest(BaseModel):
    session_id: str
    intent: str
    topic: Optional[str] = None
    chunk_id: Optional[int] = 0
    guest_count: Optional[int] = None
    check_in: Optional[str] = None  # YYYY-MM-DD
    check_out: Optional[str] = None  # YYYY-MM-DD
    room_name: Optional[str] = None

class LogConversationRequest(BaseModel):
    call_time: str  # ISO format recommended
    phone_number: str = Field(..., pattern="^\d{10}$")
    call_outcome: str
    customer_name: Optional[str]
    room_name: Optional[str]
    check_in: Optional[str]
    check_out: Optional[str]
    number_of_guests: Optional[int]
    call_summary: str

# ----------------- Endpoints -----------------

@app.post("/classify-query")
async def classify_query_endpoint(req: QueryRequest):
    try:
        intent_data = query_classifier.classify_query(req.query)
        session_id = req.session_id or str(uuid.uuid4())
        return {"session_id": session_id, "intent": intent_data['intent']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {e}")

@app.post("/retrieve-info")
async def retrieve_info_endpoint(req: RetrieveInfoRequest):
    try:
        # Validate dates if provided
        if req.check_in and not utils.validate_date(req.check_in):
            raise HTTPException(status_code=400, detail="Invalid check_in date format, should be YYYY-MM-DD")
        if req.check_out and not utils.validate_date(req.check_out):
            raise HTTPException(status_code=400, detail="Invalid check_out date format, should be YYYY-MM-DD")
        
        # Based on intent, get appropriate info
        info_text = ""
        if req.intent == "booking":
            if not req.guest_count:
                raise HTTPException(status_code=400, detail="guest_count is required for booking info")
            info_text = info_retriever.get_room_info(data, guest_count=req.guest_count)
            if req.room_name and req.check_in and req.check_out:
                price_str = info_retriever.calculate_price(data, req.room_name, req.check_in, req.check_out)
                info_text += f"\n\n{price_str}"

        elif req.intent == "policy":
            info_text = info_retriever.get_hotel_rules(data)
        elif req.intent == "staff":
            info_text = info_retriever.get_staff_queries(data)
        elif req.intent == "discount":
            info_text = info_retriever.get_discount_info(data)
        else:
            # For general enquires, fallback to generic info (hotel rules + rooms)
            info_text = "I can provide information about rooms, pricing, policies, staff services, and discounts at Formi Resorts."
        
        # If empty info, respond politely
        if not info_text.strip():
            return {
                "data": "I'm sorry, I do not have information on that topic. Can I assist you with something else?",
                "has_more": False,
                "next_chunk_id": None
            }

        # Chunk info_text to <800 tokens
        chunks = info_retriever.chunk_text(info_text, max_tokens=800)
        cid = req.chunk_id if req.chunk_id is not None else 0
        if cid >= len(chunks):
            return {"data": "", "has_more": False, "next_chunk_id": None}
        
        # Save session context
        session_manager.save_session_chunk(req.session_id, cid)

        return {
            "data": chunks[cid],
            "has_more": cid < len(chunks) - 1,
            "next_chunk_id": cid + 1 if cid < len(chunks) - 1 else None
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving info: {e}")

@app.post("/log-conversation")
async def log_conversation_endpoint(req: LogConversationRequest):
    try:
        # Prepare data fields and fill NA if missing
        call_time = req.call_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [
            call_time,
            req.phone_number,
            req.call_outcome,
            utils.format_na_if_empty(req.customer_name),
            utils.format_na_if_empty(req.room_name),
            utils.format_na_if_empty(req.check_in),
            utils.format_na_if_empty(req.check_out),
            req.number_of_guests if req.number_of_guests is not None else "NA",
            req.call_summary
        ]
        google_sheets_logger.log_conversation(row)
        return {"status": "Conversation logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log conversation: {e}")


@app.get("/")
async def root():
    return {"message": "Formi Resorts Voice AI backend is running."}

