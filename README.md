# Finance_project

# 📊 Customer-Centric Financial Analytics Dashboard (Power BI)

A multi-page interactive Power BI dashboard designed to simulate a real-world business informatics use case for a financial services company. The dashboard provides deep insights into AUM trends, customer behavior, product performance, service quality, and digital engagement — supporting decision-making across business and technical teams.

---

## 🧩 Project Overview

This project replicates a business scenario where a data visualization analyst is tasked with integrating multiple data sources to build an executive-ready reporting system.

---

## 🎯 Objectives

- Track AUM, contributions, and withdrawals over time
- Compare product performance based on ROI, risk, and fee revenue
- Analyze customer growth, segmentation, and retention
- Identify patterns in service satisfaction and support resolution
- Visualize digital engagement trends and device adoption

---

## 📁 Data Sources (Simulated)
### 1. Customer Data (`customers.csv`)

customer_id,first_name,last_name,birth_date,enrollment_date,customer_segment,employer_id,email,phone,address_city,address_state

### 2. Financial Products (`products.csv`)

product_id,product_name,product_category,launch_date,min_investment,annual_fee_percentage,management_fee_fixed,risk_level,active_status

### 3. Customer Product Enrollment (`enrollments.csv`)

enrollment_id,customer_id,product_id,enrollment_date,initial_investment,contribution_frequency,monthly_contribution,advisor_id,channel,status

### 4. Account Balances (Time Series) (`account_balances.csv`)

balance_id,customer_id,product_id,date,balance,contributions_mtd,withdrawals_mtd,investment_returns_mtd,fees_mtd

### 5. Customer Service Interactions (`service_interactions.csv`)

interaction_id,customer_id,date,channel,reason_code,duration_minutes,satisfaction_score,resolution_status,agent_id

### 6. Customer Engagement (`engagement.csv`)

engagement_id,customer_id,date,action_type,device_type,session_duration,pages_viewed,actions_taken

### 7. Financial Advisors (`advisors.csv`)

advisor_id,first_name,last_name,office_location,certification_level,years_experience,customer_satisfaction_avg,clients_count

### 8. Market Data (`market_data.csv`)

date,sp500_index,bond_index,inflation_rate,prime_rate,unemployment_rate

### 9. Customer Retention/Churn (`retention.csv`)

customer_id,product_id,churn_date,churn_reason,exit_survey_score,recovered_flag,total_customer_lifetime_value

> 💡 *Data is synthetically generated using Python to match realistic patterns.*

---

## 📊 Dashboard Pages

### ✅ 1. Executive Summary
- KPIs: AUM, Net Flows, Active Customers, Retention Rate
- Time-series: AUM Trend with forecast
- AUM by Product Category (Donut), Net Flows Over Time
- Products Per Customer by Segment, Customer Map by State

### 📈 2. Product Performance
- Product Matrix: AUM, Fee Revenue, Net Flow
- Risk vs Return Scatter Plot (Bubble Size = AUM)
- ROI vs Benchmark (Line Chart), Top/Bottom Products
- Fee Revenue by Product, AUM by Risk Category

### 👥 3. Customer Insights
- Acquisition Trend (Line), Growth Drivers (Waterfall)
- Avg Balance by Segment & Age, Sankey: Channel → Product → Status
- Customer Value (Tenure vs Balance), Retention Heat Map

### 🛠 4. Service Quality
- Volume by Channel Over Time, Satisfaction by Issue Type
- FCR Gauge, Service Resolution Funnel, Issues by Segment/Product
- Top Contact Reasons Table

### 📱 5. Digital Engagement
- Engagement Trend Over Time, Device Distribution
- Common Digital Actions, Usage by Age Group and Device
- Session Duration Trend, Engagement vs Growth Scatter

---

## 🛠 Tools & Skills Used

- **Power BI Desktop** – Dashboard design, visuals, slicers
- **Power Query (M)** – Data transformation and cleaning
- **DAX** – Custom KPIs and calculated measures
- **Python** – Synthetic data generation (Pandas, NumPy)
- **GitHub** – Version control and documentation


