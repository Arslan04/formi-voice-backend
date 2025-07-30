from app.services.chunker import chunk_text
from datetime import datetime
import pandas as pd

def get_room_info(data, guest_count=None):
    df = data.rooms
    if guest_count:
        df = df[df['Max Guests'] >= guest_count]

    room_list = []
    for idx, row in df.iterrows():
        amenities = []
        # Select example amenities to show, add more if needed
        for amenity_col in ['baby_cot_available', 'pool_available', 'gym', 'pets_allowed']:
            val = row.get(amenity_col, 'NA')
            if val != 'No' and pd.notna(val):
                amenities.append(f"{amenity_col.replace('_', ' ').title()}: {val}")
        amenities_str = ", ".join(amenities) if amenities else 'None'

        speciality = row.get('Speciality (additional Information)', 'NA')
        desc = (f"Room: {row['Room Name']}, Max Guests: {row['Max Guests']}, "
                f"Amenities: {amenities_str}, Speciality: {speciality}")
        room_list.append(desc)

    return "\n".join(room_list)

def calculate_price(data, room_name: str, check_in: str, check_out: str):
    try:
        # The API inputs use ISO format YYYY-MM-DD, parsing accordingly
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    except Exception:
        return "Invalid check-in or check-out date format. Please use YYYY-MM-DD."

    df = data.pricing.copy()
    # Convert the 'Date' column from string DD/MM/YYYY to datetime
    df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y", errors='coerce')

    mask = (df['Property Name'].str.lower() == room_name.lower()) & \
           (df['Date'] >= check_in_date) & (df['Date'] < check_out_date)

    filtered = df.loc[mask]

    if filtered.empty:
        return f"No pricing found for {room_name} between {check_in} and {check_out}."

    total_price = filtered['price'].sum()
    nights = (check_out_date - check_in_date).days
    return f"The total price for {room_name} from {check_in} to {check_out} ({nights} nights) is {total_price}."





def get_hotel_rules(data):
    df = data.rules
    if df.empty:
        return "No hotel rules available."
    
    rules_texts = []
    for _, row in df.iterrows():
        parts = []
        for col in df.columns:
            val = row.get(col, None)
            if val and pd.notna(val) and str(val).strip() != "":
                parts.append(f"{col}: {val}")
        # Join all parts of this row with newlines or commas; here I use newlines
        rule_str = "\n".join(parts)
        rules_texts.append(rule_str)
    
    # Join all rows separated by double newlines for readability
    return "\n\n".join(rules_texts)





def get_staff_queries(data):
    df = data.staff_queries
    if df.empty:
        return "No staff queries available."
    
    staff_info_list = []
    for _, row in df.iterrows():
        parts = []
        for col in df.columns:
            val = row.get(col, None)
            if val and pd.notna(val) and str(val).strip() != "":
                parts.append(f"{col}: {val}")
        staff_info_str = "\n".join(parts)
        staff_info_list.append(staff_info_str)
    
    return "\n\n".join(staff_info_list)



def get_discount_info(data):
    discounts = []
    if 'Member Type' in data.discounts.columns and 'Discount' in data.discounts.columns:
        for _, row in data.discounts.iterrows():
            mem_type = row.get('Member Type', 'NA')
            discount = row.get('Discount', 'NA')
            discounts.append(f"Member Type: {mem_type}, Discount: {discount}")
    else:
        return "No discount information available."
    return "\n".join(discounts)
