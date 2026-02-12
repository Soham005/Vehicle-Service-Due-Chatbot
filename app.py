import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

st.set_page_config(page_title="Smart Vehicle Service Bot", page_icon="🚗")

st.title("🚗 Smart Vehicle Service Assistant")
st.write("Your interactive assistant for vehicle maintenance.")

# ---------------------------
# Initialize chat memory
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "awaiting_service_check" not in st.session_state:
    st.session_state.awaiting_service_check = False

# ---------------------------
# Expanded FAQ Library
# ---------------------------
faq = {
    "service due": "Most vehicles require service every 6 months or 5,000–10,000 km.",
    "engine oil": "Engine oil should be changed every 5,000–10,000 km depending on vehicle type.",
    "battery": "Car batteries usually last 3–5 years.",
    "brake": "Brake pads typically last 30,000–70,000 km.",
    "tyre pressure": "Check tyre pressure at least once a month.",
    "insurance": "Vehicle insurance should be renewed yearly.",
    "mileage low": "Low mileage can be due to dirty air filters, old oil, or incorrect tyre pressure.",
    "overheating": "Engine overheating may be due to low coolant or radiator issues.",
    "cost": "Basic vehicle service costs between ₹2000 – ₹6000.",
    "skip service": "Skipping service may cause expensive engine damage."
}

maintenance_tips = [
    "💡 Tip: Regular oil changes improve engine life.",
    "💡 Tip: Maintain correct tyre pressure for better mileage.",
    "💡 Tip: Clean air filters improve fuel efficiency.",
    "💡 Tip: Check brake pads every 10,000 km.",
    "💡 Tip: Wash your vehicle regularly to prevent rust."
]

# ---------------------------
# Display Chat History
# ---------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------
# Chat Input
# ---------------------------
if prompt := st.chat_input(placeholder="Ask about your vehicle..."):

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    response = None
    lower_prompt = prompt.lower()

    # ---------------------------
    # Service Due Trigger
    # ---------------------------
    if "check service" in lower_prompt:
        response = "Sure! Please enter your last service date, last service km, and current km below."
        st.session_state.awaiting_service_check = True

    # ---------------------------
    # FAQ Matching
    # ---------------------------
    else:
        for keyword in faq:
            if keyword in lower_prompt:
                response = faq[keyword]
                break

    if not response:
        response = "I'm not sure about that. Can you ask about service, mileage, battery, brakes, cost, or engine oil?"

    # Display bot response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

    # Ask Follow-up Question Automatically
    follow_up_questions = [
        "Would you like to check if your vehicle service is due?",
        "Do you want maintenance tips?",
        "Would you like to know about service costs?",
        "Do you want to check battery health tips?"
    ]

    follow_up = random.choice(follow_up_questions)
    st.session_state.messages.append({"role": "assistant", "content": follow_up})
    with st.chat_message("assistant"):
        st.markdown(follow_up)

# ---------------------------
# Service Due Calculator Section
# ---------------------------
if st.session_state.awaiting_service_check:
    st.subheader("📅 Service Due Calculator")

    last_service_date = st.date_input("Last Service Date")
    last_service_km = st.number_input("KM at Last Service", min_value=0)
    current_km = st.number_input("Current KM Reading", min_value=0)

    if st.button("Check Now"):
        next_service_date = last_service_date + relativedelta(months=6)
        km_difference = current_km - last_service_km

        risk_score = 0

        if datetime.today().date() >= next_service_date:
            risk_score += 1
        if km_difference >= 5000:
            risk_score += 1

        if risk_score == 2:
            result = "🚨 HIGH RISK: Your vehicle service is OVERDUE!"
        elif risk_score == 1:
            result = "⚠️ MEDIUM RISK: Service is approaching soon."
        else:
            result = "✅ LOW RISK: Service not required yet."

        st.success(result)

        # Add maintenance tip
        tip = random.choice(maintenance_tips)
        st.info(tip)

        st.session_state.awaiting_service_check = False
