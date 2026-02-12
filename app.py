import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Page config
st.set_page_config(page_title="Vehicle Service FAQ Bot", page_icon="🚗")

st.title("🚗 Vehicle Service FAQ Chatbot")
st.write("Ask me about vehicle service schedules, costs, or check your service due date.")

# --- FAQ Data ---
faq = {
    "when is my vehicle service due": 
        "Most vehicles require service every 6 months or 5,000–10,000 km, whichever comes first.",
    
    "what is included in basic service":
        "Basic service includes engine oil change, oil filter replacement, brake inspection, battery check, and general inspection.",
    
    "how much does service cost":
        "Basic service typically costs between ₹2000 – ₹6000 depending on vehicle type.",
    
    "why is regular servicing important":
        "Regular servicing improves fuel efficiency, prevents breakdowns, and increases vehicle lifespan.",
    
    "what happens if i skip service":
        "Skipping service can cause engine damage, poor mileage, and expensive repairs later."
}

# --- Chat Input ---
user_input = st.text_input("Ask your question here:")

if user_input:
    user_input_lower = user_input.lower()

    # FAQ Matching
    response = None
    for question in faq:
        if question in user_input_lower:
            response = faq[question]
            break

    if response:
        st.success(response)

    # Service Due Calculator
    elif "check service due" in user_input_lower:
        st.subheader("📅 Service Due Calculator")

        last_service_date = st.date_input("Select your last service date:")
        last_service_km = st.number_input("Enter km at last service:", min_value=0)
        current_km = st.number_input("Enter current km reading:", min_value=0)

        if st.button("Check Service Status"):
            next_service_date = last_service_date + relativedelta(months=6)
            km_difference = current_km - last_service_km

            if datetime.today().date() >= next_service_date or km_difference >= 5000:
                st.error("⚠️ Your vehicle service is DUE!")
            else:
                st.success("✅ Your vehicle service is NOT due yet.")

    else:
        st.warning("Sorry, I couldn't understand that. Try asking about service cost, schedule, or check service due.")
