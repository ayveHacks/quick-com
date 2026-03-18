<h1 align="center">🚀 AI-Powered Parametric Insurance Platform</h1>
<p align="center">
Protecting Quick Commerce Delivery Partners from Income Loss
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Phase-1-blue" />
  <img src="https://img.shields.io/badge/Domain-InsurTech-orange" />
  <img src="https://img.shields.io/badge/Model-Parametric-green" />
  <img src="https://img.shields.io/badge/UX-Zero--Touch-success" />
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

## 🚫 What We DON'T Cover (Strict Rule Compliance)

As per problem constraints, this platform strictly excludes:

- Health Insurance  
- Life Insurance  
- Accident Coverage  
- Vehicle Repairs  

We focus **only on income loss protection**.

---

## 💡 Solution

We propose an **AI-powered parametric insurance platform** with:

✅ Zero-Touch Payout System  
✅ Real-time disruption monitoring  
✅ Weekly-based insurance model  

No manual claims. No delays. Just **instant compensation**.

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
3. AI engine computes risk and reliability  
4. Weekly premium & coverage generated  
5. Policy activated for **7-day cycle**  
6. System continuously monitors disruptions  
7. If conditions met → **Zero-Touch Payout triggered**

---

## 📡 Disruption Monitoring

- Weather API  
- AQI API  
- Traffic API  
- Flood API  
- News API  

System checks every **15 minutes** for disruptions.

---

## 📊 Claim Evaluation Logic

- Worker activity retrieved from platform  
- Work Loss Ratio computed  

WorkLossRatio = (ExpectedOrders - ActualOrders) / ExpectedOrders  

- If WorkLossRatio ≥ 0.5 → Claim Approved  
- Else → Claim Rejected  

---

## 💰 Zero-Touch Payout System

- No manual claim filing  
- Automatic payout via UPI  
- Instant dashboard update  

---

## 🚀 Key Features

- Weekly pricing aligned with gig economy  
- Dynamic premium calculation  
- Real-time disruption detection  
- Zero-touch claim & payout system  
- Fraud-resistant claim validation  

---

## 🤖 AI/ML Integration

- Risk prediction using historical disruption patterns  
- Dynamic pricing using zone-level data  
- Fraud detection via anomaly detection:
  - GPS spoofing detection  
  - Fake disruption claim detection  

---

## 🧮 Mathematical Framework

### 1. Risk & Exposure Modeling

Risk Score:
RiskScore = Σ (Pᵢ × Wᵢ)

Exposure Score:
ES = (Σ Pᵢ) / N

---

### 2. Reliability Score (RS)

RS = (ActivityScore + CompletionScore + WorkHistoryScore + FraudScore) / 4

FraudScore = 1 - FraudFlags  

---

### 3. Weekly Financial Model (Core Innovation)

Coverage Factor (CF):
CF = 0.3 + 0.2 × RS + 0.1 × ES  

(Protects 30% – 70% of weekly income)

Weekly Premium:
Premium = WeeklyIncome × CF × BaseRate × (1 + RiskScore)

---

### 4. Payout Logic

If WorkLossRatio ≥ 0.5:

Final Payout = DailyIncome × PayoutPercent × DurationFactor  

Where:
DurationFactor = DisruptionHours / 24  

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

To build a **scalable, automated financial safety net** for gig workers using **data-driven parametric insurance principles**.
