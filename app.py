import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

st.set_page_config(page_title="AI Vehicle Service Assistant", page_icon="🚗")

st.title("🚗 AI Vehicle Service Assistant")
st.caption("Your intelligent vehicle health companion")

# ---------------------------
# SESSION STATE INIT
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stage" not in st.session_state:
    st.session_state.stage = "start"

if "vehicle_data" not in st.session_state:
    st.session_state.vehicle_data = {}

# ---------------------------
# DISPLAY CHAT HISTORY
# ---------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------
# CHAT INPUT
# ---------------------------
if prompt := st.chat_input("Type your message..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    response = ""
    lower = prompt.lower()

    # ---------------------------
    # START CONVERSATION
    # ---------------------------
    if st.session_state.stage == "start":
        response = "Great! Let's check your vehicle health 🚗\n\nWhat type of vehicle do you have?\n\n1️⃣ Car\n2️⃣ Bike"
        st.session_state.stage = "vehicle_type"

    # ---------------------------
    # VEHICLE TYPE
    # ---------------------------
    elif st.session_state.stage == "vehicle_type":
        if "car" in lower:
            st.session_state.vehicle_data["type"] = "Car"
            response = "Got it 👍 When was your last service? (Enter date in YYYY-MM-DD format)"
            st.session_state.stage = "last_service_date"

        elif "bike" in lower:
            st.session_state.vehicle_data["type"] = "Bike"
            response = "Nice 🏍 When was your last service? (Enter date in YYYY-MM-DD format)"
            st.session_state.stage = "last_service_date"
        else:
            response = "Please type 'Car' or 'Bike'."

    # ---------------------------
    # LAST SERVICE DATE
    # ---------------------------
    elif st.session_state.stage == "last_service_date":
        try:
            service_date = datetime.strptime(prompt, "%Y-%m-%d").date()
            st.session_state.vehicle_data["last_service_date"] = service_date
            response = "How many kilometers were recorded at last service?"
            st.session_state.stage = "last_km"
        except:
            response = "Please enter date in YYYY-MM-DD format."

    # ---------------------------
    # LAST KM
    # ---------------------------
    elif st.session_state.stage == "last_km":
        if prompt.isdigit():
            st.session_state.vehicle_data["last_km"] = int(prompt)
            response = "What is your current kilometer reading?"
            st.session_state.stage = "current_km"
        else:
            response = "Please enter numbers only."

    # ---------------------------
    # CURRENT KM + CALCULATION
    # ---------------------------
    elif st.session_state.stage == "current_km":
        if prompt.isdigit():

            st.session_state.vehicle_data["current_km"] = int(prompt)

            data = st.session_state.vehicle_data
            months_passed = relativedelta(datetime.today().date(), data["last_service_date"]).months + \
                            relativedelta(datetime.today().date(), data["last_service_date"]).years * 12

            km_used = data["current_km"] - data["last_km"]

            # Scoring Logic
            score = 0
            if months_passed >= 6:
                score += 1
            if km_used >= 5000:
                score += 1

            if score == 2:
                health_status = "🚨 Service OVERDUE (High Risk)"
            elif score == 1:
                health_status = "⚠️ Service Due Soon (Medium Risk)"
            else:
                health_status = "✅ Vehicle is Healthy (Low Risk)"

            tips = [
                "🔧 Consider checking brake pads.",
                "🛞 Maintain proper tyre pressure.",
                "🛢 Change engine oil regularly.",
                "🔋 Check battery condition before long trips."
            ]

            response = f"""
### 📊 Vehicle Health Report

**Vehicle Type:** {data['type']}  
**Months Since Service:** {months_passed}  
**KM Driven Since Service:** {km_used}  

### 🏥 Status:
{health_status}

### 💡 Recommendation:
{random.choice(tips)}

Would you like maintenance cost estimation or tips?
(Type: cost / tips / restart)
"""
            st.session_state.stage = "post_report"

        else:
            response = "Please enter numeric value."

    # ---------------------------
    # POST REPORT OPTIONS
    # ---------------------------
    elif st.session_state.stage == "post_report":

        if "cost" in lower:
            if st.session_state.vehicle_data["type"] == "Car":
                response = "💰 Estimated Service Cost: ₹4000 – ₹8000"
            else:
                response = "💰 Estimated Service Cost: ₹1500 – ₹3000"

        elif "tips" in lower:
            response = """
### 🔧 Maintenance Tips:
- Check oil every 2 weeks
- Clean air filters monthly
- Inspect brakes every 10,000 km
- Avoid aggressive driving
"""

        elif "restart" in lower:
            st.session_state.stage = "start"
            st.session_state.vehicle_data = {}
            response = "Restarting service assistant... 🚗 Type anything to begin again."

        else:
            response = "Type 'cost', 'tips', or 'restart'."

    # ---------------------------
    # DEFAULT
    # ---------------------------
    else:
        response = "Type something to start your vehicle health check 🚗"

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
