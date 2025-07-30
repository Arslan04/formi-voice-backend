def classify_query(user_text: str) -> dict:
    text = user_text.lower()
    if "book" in text or "availability" in text:
        return {"intent": "booking"}
    elif "discount" in text:
        return {"intent": "discount"}
    elif "rule" in text or "policy" in text:
        return {"intent": "policy"}
    elif "staff" in text:
        return {"intent": "staff"}
    else:
        return {"intent": "general_enquiry"}
