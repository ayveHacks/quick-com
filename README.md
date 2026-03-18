<h1 align="center">AI-Powered Parametric Insurance Platform</h1>
<p align="center">
Protecting Quick Commerce Delivery Partners from Income Loss
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Phase-1-blue" />
  <img src="https://img.shields.io/badge/Domain-InsurTech-orange" />
  <img src="https://img.shields.io/badge/Model-Parametric-green" />
</p>

---

## Problem

Delivery partners in quick commerce platforms (Blinkit, Zepto, etc.) face income loss due to external disruptions such as heavy rain, traffic congestion, extreme heat, and platform outages.

These disruptions are unpredictable and uncontrollable, yet workers have no structured income protection system.

---

## What We Don't Cover

As per problem constraints, this platform strictly excludes:

- Health insurance  
- Life insurance  
- Accident coverage  
- Vehicle repairs  

The system focuses only on income loss protection.

---

## Solution

We propose a parametric insurance platform with a zero-touch payout system.

- Real-time external data is monitored  
- No manual claims are required  
- Payouts are automatically triggered  

This ensures fast, transparent, and reliable compensation.

---

## System Architecture

<p align="center">
  <img src="docs/architecture.png" width="700"/>
</p>

---

## Workflow

<p align="center">
  <img src="docs/workflow.png" width="700"/>
</p>

### Flow Summary

1. Worker registers and provides profile and income data  
2. System computes risk and reliability scores  
3. Weekly premium and coverage are generated  
4. Policy is activated for a 7-day cycle  
5. System monitors real-time disruptions  
6. If conditions are satisfied, payout is triggered automatically  

---

## Disruption Monitoring

The system continuously monitors:

- Weather API  
- AQI API  
- Traffic API  
- Flood alerts  
- News signals  

Monitoring frequency: every 15 minutes.

---

## Claim Evaluation Logic

WorkLossRatio = (ExpectedOrders - ActualOrders) / ExpectedOrders  

- If WorkLossRatio ≥ 0.5 → Claim approved  
- Otherwise → Claim rejected  

---

## Payout System

- Zero-touch claim processing  
- Instant payout via UPI (simulated)  
- Real-time dashboard updates  

---

## Key Features

- Weekly pricing aligned with gig economy  
- Dynamic premium calculation  
- Real-time disruption detection  
- Automated claim triggering  
- Fraud-resistant validation  

---

## AI/ML Integration

- Risk prediction using historical disruption data  
- Dynamic pricing based on zone-level patterns  
- Fraud detection using anomaly detection:
  - GPS spoofing detection  
  - Fake disruption claim detection  

---

## Mathematical Framework

### Risk and Exposure

RiskScore = Σ (Pᵢ × Wᵢ)  
ES = (Σ Pᵢ) / N  

---

### Reliability Score

RS = (ActivityScore + CompletionScore + WorkHistoryScore + FraudScore) / 4  

FraudScore = 1 - FraudFlags  

---

### Weekly Financial Model

CoverageFactor (CF):  
CF = 0.3 + 0.2 × RS + 0.1 × ES  

Weekly Premium:  
Premium = WeeklyIncome × CF × BaseRate × (1 + RiskScore)  

---

### Payout Logic

If WorkLossRatio ≥ 0.5:

Final Payout = DailyIncome × PayoutPercent × DurationFactor  

DurationFactor = DisruptionHours / 24  

---

## Tech Stack

| Layer       | Technology |
|------------|-----------|
| Frontend   | React |
| Backend    | Flask |
| Database   | MongoDB |
| APIs       | Weather, Traffic, AQI |
| Payments   | UPI (Simulated) |

---

## Project Structure

parametric-insurance/
├── docs/  
├── src/  
├── backend/  
├── frontend/  
├── README.md  

---

## Vision

To build a scalable, automated financial safety net for gig workers using data-driven parametric insurance principles.

