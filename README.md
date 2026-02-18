# 🚗 AI Vehicle Service Assistant  

An interactive, ChatGPT-style vehicle service chatbot built using **Streamlit** and **Python**.  

This application guides users step-by-step to check their vehicle’s service health, calculate service due risk, estimate costs, and receive maintenance recommendations.

---

## 📌 Project Overview  

The **AI Vehicle Service Assistant** is a rule-based conversational chatbot that:

- Collects vehicle information interactively  
- Tracks conversation context  
- Calculates service due status  
- Generates a vehicle health report  
- Provides maintenance cost estimates  
- Offers smart recommendations  

The chatbot mimics a structured AI conversation flow similar to ChatGPT.

---

## 🎯 Key Features  

- ✅ Conversational Chat UI (like ChatGPT)  
- ✅ Context-aware conversation stages  
- ✅ Vehicle type selection (Car / Bike)  
- ✅ Service health scoring system  
- ✅ Risk classification (Low / Medium / High)  
- ✅ Cost estimation  
- ✅ Maintenance tips generation  
- ✅ Restartable session flow  
- ✅ Clean Streamlit interface  

---

## 🧠 How It Works  

The chatbot follows a **state-based conversation engine**:

1. User selects vehicle type  
2. Enters last service date  
3. Enters last service kilometer reading  
4. Enters current kilometer reading  
5. System calculates:
   - Months since last service  
   - Kilometers driven  
   - Risk score  
6. Generates:
   - Health status  
   - Recommendations  
   - Cost estimation  

---

## 📊 Service Health Logic  

Service risk score is calculated based on:

- ≥ 6 months since last service → +1 risk  
- ≥ 5000 km driven since last service → +1 risk  

| Score | Status |
|--------|---------|
| 0 | ✅ Healthy |
| 1 | ⚠️ Service Due Soon |
| 2 | 🚨 Service Overdue |

---

## 🛠 Tech Stack  

- Python 3  
- Streamlit  
- python-dateutil  
- Stateful Session Management  
- Rule-Based Conversation Engine  
