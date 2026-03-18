<h1 align="center">🚀 AI-Powered Parametric Insurance Platform</h1>
<p align="center">
Protecting Quick Commerce Delivery Partners from Income Loss
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Phase-1-blue" />
  <img src="https://img.shields.io/badge/Domain-InsurTech-orange" />
  <img src="https://img.shields.io/badge/Model-Parametric-green" />
</p>

---

## 📌 Problem

Delivery partners in quick commerce platforms (Blinkit, Zepto, etc.) face **income loss due to external disruptions** such as:

- Heavy rain 🌧️  
- Traffic congestion 🚗  
- Extreme heat 🌡️  
- Platform/server outages ⚠️  

These disruptions are **unpredictable and uncontrollable**, yet workers have **no structured income protection system**.

---

## 💡 Solution

We propose an **AI-powered parametric insurance platform** where:

✅ No manual claims are required  
✅ Real-time external data is monitored  
✅ Payouts are automatically triggered  

This ensures **fast, transparent, and reliable compensation** for gig workers.

---

## 🧠 System Architecture

<p align="center">
  <img src="docs/architecture.png" width="700"/>
</p>

---

## ⚙️ Workflow

<p align="center">
  <img src="docs/workflow.png" width="700"/>
</p>

### 🔄 Flow Summary

1. Delivery partner registers via mobile app  
2. Worker profile, location, and income data collected  
3. AI engine calculates:
   - Risk score  
   - Exposure score  
   - Reliability score  
4. Weekly premium and coverage generated  
5. Policy activated (7-day cycle)  

---

### 📡 Disruption Monitoring

- System continuously monitors:
  - Weather API  
  - AQI API  
  - Traffic API  
  - Flood API  
  - News API  

- If disruption detected → event tracking begins  

---

### 📊 Claim Evaluation

- Worker activity data retrieved  
- Work loss ratio calculated  

WorkLossRatio = (ExpectedOrders - ActualOrders) / ExpectedOrders  

- If WorkLossRatio ≥ 0.5 → Claim Approved  
- Otherwise → Claim Rejected  

---

### 💰 Payout System

- Approved claims → instant payout via UPI  
- Dashboard updated in real-time  

---

## 🚀 Key Features

- Dynamic weekly premium calculation  
- Real-time disruption detection  
- Automated claim triggering (zero-touch)  
- Fraud detection using activity validation  
- Instant payout processing  

---

## 🤖 AI/ML Integration

- Risk prediction based on historical disruption patterns  
- Dynamic pricing using zone-level risk  
- Fraud detection via anomaly detection  

---

## 🛠️ Tech Stack

| Layer       | Technology |
|------------|-----------|
| Frontend   | React |
| Backend    | Flask |
| Database   | MongoDB |
| APIs       | Weather, Traffic, AQI |
| Payments   | UPI (Simulated) |

---

## 📁 Project Structure

parametric-insurance/
├── docs/              
├── src/               
├── backend/           
├── frontend/          
├── README.md          

---

## 🎯 Vision

To build a **scalable, automated financial safety net** for gig workers, ensuring **income stability during real-world disruptions**.