import csv
import random
import datetime
import math
import os
import numpy as np
from faker import Faker

# Initialize Faker to generate realistic data
fake = Faker()
random.seed(42)  # For reproducibility
np.random.seed(42)

# Create output directory if it doesn't exist
output_dir = "financial_dataset"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define constants and parameters
NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 15
NUM_ADVISORS = 50
NUM_INTERACTIONS = 5000
NUM_ENGAGEMENT = 10000
START_DATE = datetime.date(2020, 1, 1)
END_DATE = datetime.date(2024, 10, 1)
DAYS_RANGE = (END_DATE - START_DATE).days

# Customer segments
CUSTOMER_SEGMENTS = ["Mass Market", "Affluent", "High Net Worth", "Ultra High Net Worth"]
SEGMENT_WEIGHTS = [0.6, 0.25, 0.1, 0.05]

# Product categories
PRODUCT_CATEGORIES = [
    "Retirement Account", "Investment Fund", "Savings Account", 
    "Stock Portfolio", "Bond Fund", "Real Estate Fund", 
    "ETF", "Mutual Fund", "Insurance Product"
]

# Risk levels
RISK_LEVELS = ["Low", "Medium-Low", "Medium", "Medium-High", "High"]

# Contribution frequencies
CONTRIBUTION_FREQUENCIES = ["Monthly", "Quarterly", "Bi-annual", "Annual", "One-time"]

# Interaction channels
CHANNELS = ["Phone", "Email", "Web", "Mobile App", "In-person", "Chat", "Social Media"]

# Interaction reasons
REASON_CODES = [
    "Account Inquiry", "Investment Advice", "Technical Support", 
    "Complaint", "Transaction Issue", "Password Reset", 
    "Statement Request", "Fee Inquiry", "Market Information"
]

# Engagement types
ACTION_TYPES = [
    "Login", "View Balance", "Update Profile", "Research Product", 
    "Modify Investment", "Download Statement", "Contact Support", 
    "Complete Survey", "Watch Educational Video", "Use Planning Tool"
]

# Device types
DEVICE_TYPES = ["Desktop", "Mobile Phone", "Tablet", "Smart TV", "Voice Assistant"]

# Churn reasons
CHURN_REASONS = [
    "Competitor Offering", "Fee Concerns", "Poor Performance", 
    "Service Issue", "Life Event", "Financial Hardship", 
    "Product Dissatisfaction", "Advisor Change", "Relocation"
]

# States
US_STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

# Helper function to generate a random date
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_number_of_days)

# Helper function for seasonal effects 
def seasonal_effect(date):
    # Higher contributions in Q4 (tax planning), lower in summer
    month = date.month
    if 10 <= month <= 12:  # Q4
        return 1.2
    elif 6 <= month <= 8:  # Summer
        return 0.8
    else:
        return 1.0

# Helper function for market fluctuations
def market_fluctuation(date):
    # Simple sinusoidal pattern with some randomness
    days_since_start = (date - START_DATE).days
    annual_cycle = math.sin(days_since_start / 365 * 2 * math.pi)
    monthly_noise = math.sin(days_since_start / 30 * 2 * math.pi) * 0.2
    random_factor = random.uniform(-0.1, 0.1)
    
    return 1.0 + annual_cycle * 0.1 + monthly_noise + random_factor

# Helper function for digital adoption trend
def digital_adoption_trend(date):
    # Increasing trend from 30% to 80% over the time period
    days_since_start = (date - START_DATE).days
    total_days = (END_DATE - START_DATE).days
    base_digital = 0.3
    max_increase = 0.5
    return base_digital + (days_since_start / total_days) * max_increase

# Helper function to adjust value based on customer segment
def segment_multiplier(segment):
    if segment == "Ultra High Net Worth":
        return 8.0
    elif segment == "High Net Worth":
        return 4.0
    elif segment == "Affluent":
        return 2.0
    else:
        return 1.0

# Helper function to adjust behavior based on age
def age_factor(birth_date):
    age = (datetime.date.today() - birth_date).days / 365
    if age < 30:
        return {"digital_affinity": 0.9, "risk_tolerance": 0.8, "contribution_rate": 0.7}
    elif age < 45:
        return {"digital_affinity": 0.7, "risk_tolerance": 0.7, "contribution_rate": 1.0}
    elif age < 60:
        return {"digital_affinity": 0.5, "risk_tolerance": 0.5, "contribution_rate": 1.2}
    else:
        return {"digital_affinity": 0.3, "risk_tolerance": 0.3, "contribution_rate": 0.8}

# Generate Financial Advisors
advisors = []
advisor_offices = [f"{fake.city()}, {random.choice(US_STATES)}" for _ in range(12)]

with open(f"{output_dir}/advisors.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "advisor_id", "first_name", "last_name", "office_location", 
        "certification_level", "years_experience", "customer_satisfaction_avg", "clients_count"
    ])
    
    for i in range(1, NUM_ADVISORS + 1):
        advisor_id = f"ADV{i:04d}"
        first_name = fake.first_name()
        last_name = fake.last_name()
        office_location = random.choice(advisor_offices)
        certification_level = random.choice(["Junior", "Associate", "Senior", "Expert", "Master"])
        years_experience = random.randint(1, 30)
        # More experienced advisors tend to have better satisfaction
        base_satisfaction = 3.0 + (years_experience / 30) * 1.5
        satisfaction_noise = random.uniform(-0.5, 0.5)
        customer_satisfaction_avg = min(5.0, max(1.0, base_satisfaction + satisfaction_noise))
        # Experienced and higher-satisfaction advisors tend to have more clients
        clients_count = int(random.normalvariate(20, 5) * (1 + years_experience/15) * (customer_satisfaction_avg/3))
        
        advisors.append({
            "advisor_id": advisor_id,
            "first_name": first_name,
            "last_name": last_name,
            "office_location": office_location,
            "certification_level": certification_level,
            "years_experience": years_experience,
            "customer_satisfaction_avg": customer_satisfaction_avg,
            "clients_count": clients_count
        })
        
        writer.writerow([
            advisor_id, first_name, last_name, office_location, 
            certification_level, years_experience, 
            round(customer_satisfaction_avg, 2), clients_count
        ])

# Generate Financial Products
products = []

with open(f"{output_dir}/products.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "product_id", "product_name", "product_category", "launch_date", 
        "min_investment", "annual_fee_percentage", "management_fee_fixed", 
        "risk_level", "active_status"
    ])
    
    for i in range(1, NUM_PRODUCTS + 1):
        product_id = f"PRD{i:04d}"
        category = random.choice(PRODUCT_CATEGORIES)
        product_name = f"{fake.company_suffix()} {category}"
        launch_date = random_date(
            START_DATE - datetime.timedelta(days=365*5), 
            START_DATE + datetime.timedelta(days=365)
        )
        
        # Higher risk products tend to have higher min investments
        risk_level = random.choice(RISK_LEVELS)
        risk_index = RISK_LEVELS.index(risk_level)
        
        min_investment_base = [500, 1000, 2500, 5000, 10000][risk_index]
        min_investment = min_investment_base * random.randint(1, 5)
        
        # Fees tend to correlate with product category and risk
        if "Fund" in category or "Portfolio" in category:
            annual_fee_percentage = random.uniform(0.5, 2.0) * (1 + risk_index/5)
            management_fee_fixed = 0
        else:
            annual_fee_percentage = random.uniform(0.1, 0.5) * (1 + risk_index/10)
            management_fee_fixed = random.choice([0, 25, 50, 100])
            
        active_status = random.choices(["Active", "Inactive"], weights=[0.9, 0.1])[0]
        
        products.append({
            "product_id": product_id,
            "product_name": product_name,
            "product_category": category,
            "launch_date": launch_date,
            "min_investment": min_investment,
            "annual_fee_percentage": round(annual_fee_percentage, 2),
            "management_fee_fixed": management_fee_fixed,
            "risk_level": risk_level,
            "active_status": active_status
        })
        
        writer.writerow([
            product_id, product_name, category, launch_date.strftime("%Y-%m-%d"),
            min_investment, round(annual_fee_percentage, 2), management_fee_fixed,
            risk_level, active_status
        ])

# Generate Customers
customers = []

with open(f"{output_dir}/customers.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "customer_id", "first_name", "last_name", "birth_date", "enrollment_date",
        "customer_segment", "employer_id", "email", "phone", "address_city", "address_state"
    ])
    
    for i in range(1, NUM_CUSTOMERS + 1):
        customer_id = f"CUS{i:06d}"
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        # Age distribution skewed toward adults
        age = random.choices(
            [random.randint(18, 30), random.randint(30, 50), random.randint(50, 75), random.randint(75, 90)],
            weights=[0.2, 0.4, 0.3, 0.1]
        )[0]
        birth_date = datetime.date.today() - datetime.timedelta(days=int(age*365.25))
        
        enrollment_date = random_date(START_DATE, END_DATE - datetime.timedelta(days=30))
        customer_segment = random.choices(CUSTOMER_SEGMENTS, weights=SEGMENT_WEIGHTS)[0]
        employer_id = f"EMP{random.randint(1, 500):04d}"
        
        email = f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}"
        phone = fake.phone_number()
        address_city = fake.city()
        address_state = random.choice(US_STATES)
        
        customers.append({
            "customer_id": customer_id,
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "enrollment_date": enrollment_date,
            "customer_segment": customer_segment,
            "employer_id": employer_id,
            "email": email,
            "phone": phone,
            "address_city": address_city,
            "address_state": address_state,
            "age_factors": age_factor(birth_date),
            "segment_multiplier": segment_multiplier(customer_segment)
        })
        
        writer.writerow([
            customer_id, first_name, last_name, birth_date.strftime("%Y-%m-%d"),
            enrollment_date.strftime("%Y-%m-%d"), customer_segment, employer_id,
            email, phone, address_city, address_state
        ])

# Generate Customer Product Enrollments
enrollments = []

with open(f"{output_dir}/enrollments.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "enrollment_id", "customer_id", "product_id", "enrollment_date",
        "initial_investment", "contribution_frequency", "monthly_contribution",
        "advisor_id", "channel", "status"
    ])
    
    enrollment_id = 1
    
    # Determine number of products per customer based on segment
    for customer in customers:
        segment = customer["customer_segment"]
        if segment == "Ultra High Net Worth":
            num_products = random.randint(3, 8)
        elif segment == "High Net Worth":
            num_products = random.randint(2, 5)
        elif segment == "Affluent":
            num_products = random.randint(1, 3)
        else:  # Mass Market
            num_products = random.randint(1, 2)
            
        # Select products for this customer
        customer_products = random.sample(products, min(num_products, len(products)))
        
        for product in customer_products:
            enrollment_date = max(customer["enrollment_date"], product["launch_date"])
            
            # Make sure enrollment date is within our time range
            if enrollment_date > END_DATE:
                continue
                
            # Calculate initial investment based on customer segment and product minimum
            segment_mult = customer["segment_multiplier"]
            base_investment = product["min_investment"]
            initial_investment = base_investment * random.uniform(1.0, 2.0) * segment_mult
            
            # Determine contribution frequency and monthly amount
            contribution_frequency = random.choice(CONTRIBUTION_FREQUENCIES)
            
            # Monthly contribution based on customer segment and age
            base_monthly = initial_investment * 0.02  # 2% of initial investment per month
            age_contribution_factor = customer["age_factors"]["contribution_rate"]
            monthly_contribution = base_monthly * age_contribution_factor * segment_mult
            
            if contribution_frequency == "Quarterly":
                monthly_contribution *= 3
            elif contribution_frequency == "Bi-annual":
                monthly_contribution *= 6
            elif contribution_frequency == "Annual":
                monthly_contribution *= 12
            elif contribution_frequency == "One-time":
                monthly_contribution = 0
                
            # Assign advisor - higher net worth customers get more experienced advisors
            suitable_advisors = sorted(
                advisors, 
                key=lambda a: a["years_experience"] + a["customer_satisfaction_avg"],
                reverse=True
            )
            
            if segment == "Ultra High Net Worth":
                advisor = suitable_advisors[random.randint(0, min(5, len(suitable_advisors)-1))]
            elif segment == "High Net Worth":
                advisor = suitable_advisors[random.randint(0, min(10, len(suitable_advisors)-1))]
            else:
                advisor = random.choice(advisors)
                
            # Determine channel based on age and digital trends
            digital_affinity = customer["age_factors"]["digital_affinity"]
            enrollment_days_since_start = (enrollment_date - START_DATE).days
            digital_trend = digital_adoption_trend(enrollment_date)
            
            if random.random() < digital_affinity * digital_trend:
                channel = random.choice(["Web", "Mobile App"])
            else:
                channel = random.choice(["Phone", "In-person"])
                
            status = "Active"
            
            enrollments.append({
                "enrollment_id": f"ENR{enrollment_id:07d}",
                "customer_id": customer["customer_id"],
                "product_id": product["product_id"],
                "enrollment_date": enrollment_date,
                "initial_investment": round(initial_investment, 2),
                "contribution_frequency": contribution_frequency,
                "monthly_contribution": round(monthly_contribution, 2),
                "advisor_id": advisor["advisor_id"],
                "channel": channel,
                "status": status
            })
            
            writer.writerow([
                f"ENR{enrollment_id:07d}", customer["customer_id"], product["product_id"],
                enrollment_date.strftime("%Y-%m-%d"), round(initial_investment, 2),
                contribution_frequency, round(monthly_contribution, 2),
                advisor["advisor_id"], channel, status
            ])
            
            enrollment_id += 1

# Generate Market Data
market_data = []
current_date = START_DATE
sp500_index = 3000  # Starting value
bond_index = 100    # Starting value
inflation_rate = 2.0  # Starting value
prime_rate = 3.5     # Starting value
unemployment_rate = 4.5  # Starting value

with open(f"{output_dir}/market_data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "date", "sp500_index", "bond_index", "inflation_rate", 
        "prime_rate", "unemployment_rate"
    ])
    
    while current_date <= END_DATE:
        # Market fluctuations
        market_factor = market_fluctuation(current_date)
        
        # SP500 changes with some randomness and market factor
        sp500_change = random.normalvariate(0.0004, 0.01) * market_factor  # ~10% annual growth with volatility
        sp500_index = max(sp500_index * (1 + sp500_change), 1000)  # Ensure it doesn't go too low
        
        # Bond index changes more slowly
        bond_change = random.normalvariate(0.0001, 0.002) * (1 / market_factor)  # Inverse relationship with stocks
        bond_index = max(bond_index * (1 + bond_change), 90)
        
        # Inflation changes slowly with some correlation to market
        inflation_change = random.normalvariate(0, 0.05) * market_factor
        inflation_rate = max(min(inflation_rate + inflation_change, 8.0), 0.5)  # Keep between 0.5% and 8%
        
        # Prime rate follows inflation with a lag
        if random.random() < 0.05:  # Rate changes are infrequent
            if inflation_rate > 4.0 and prime_rate < 7.0:
                prime_rate += random.uniform(0.25, 0.5)
            elif inflation_rate < 2.0 and prime_rate > 3.0:
                prime_rate -= random.uniform(0.25, 0.5)
        
        # Unemployment rate
        if random.random() < 0.1:  # Unemployment changes monthly
            unemployment_change = random.normalvariate(0, 0.1) * (1 / market_factor)  # Better market, lower unemployment
            unemployment_rate = max(min(unemployment_rate + unemployment_change, 10.0), 3.0)  # Keep between 3% and 10%
        
        market_data.append({
            "date": current_date,
            "sp500_index": round(sp500_index, 2),
            "bond_index": round(bond_index, 2),
            "inflation_rate": round(inflation_rate, 2),
            "prime_rate": round(prime_rate, 2),
            "unemployment_rate": round(unemployment_rate, 2)
        })
        
        writer.writerow([
            current_date.strftime("%Y-%m-%d"),
            round(sp500_index, 2),
            round(bond_index, 2),
            round(inflation_rate, 2),
            round(prime_rate, 2),
            round(unemployment_rate, 2)
        ])
        
        # Advance to next date (using business days approximation)
        current_date += datetime.timedelta(days=1)
        if current_date.weekday() >= 5:  # Skip weekends
            current_date += datetime.timedelta(days=8 - current_date.weekday())

# Generate Account Balances
# We'll generate monthly balances for each enrollment
balance_id = 1

with open(f"{output_dir}/account_balances.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "balance_id", "customer_id", "product_id", "date",
        "balance", "contributions_mtd", "withdrawals_mtd", 
        "investment_returns_mtd", "fees_mtd"
    ])
    
    for enrollment in enrollments:
        customer_id = enrollment["customer_id"]
        product_id = enrollment["product_id"]
        enrollment_date = enrollment["enrollment_date"]
        
        # Find the customer and product details
        customer = next(c for c in customers if c["customer_id"] == customer_id)
        product = next(p for p in products if p["product_id"] == product_id)
        
        # Set up initial balance and date
        current_date = enrollment_date
        balance = enrollment["initial_investment"]
        
        # Monthly processing until end date
        while current_date <= END_DATE:
            # Calculate month-end date
            month_end = datetime.date(current_date.year, current_date.month, 1)
            month_end = month_end.replace(day=28) + datetime.timedelta(days=4)
            month_end = month_end - datetime.timedelta(days=month_end.day)
            
            # If we're past month-end, move to next month
            if current_date.day > month_end.day:
                current_date = datetime.date(
                    current_date.year + (current_date.month // 12), 
                    (current_date.month % 12) + 1, 
                    1
                )
                continue
                
            # Get market data for this month
            monthly_market_data = [m for m in market_data if m["date"].year == current_date.year and m["date"].month == current_date.month]
            if not monthly_market_data:
                # No market data for this month, move to next
                current_date = datetime.date(
                    current_date.year + (current_date.month // 12), 
                    (current_date.month % 12) + 1, 
                    1
                )
                continue
                
            # Calculate monthly contributions based on frequency
            contributions_mtd = 0
            if enrollment["contribution_frequency"] == "Monthly":
                contributions_mtd = enrollment["monthly_contribution"]
            elif enrollment["contribution_frequency"] == "Quarterly" and current_date.month % 3 == 0:
                contributions_mtd = enrollment["monthly_contribution"]
            elif enrollment["contribution_frequency"] == "Bi-annual" and current_date.month in [6, 12]:
                contributions_mtd = enrollment["monthly_contribution"]
            elif enrollment["contribution_frequency"] == "Annual" and current_date.month == 12:
                contributions_mtd = enrollment["monthly_contribution"]
                
            # Apply seasonal effect to contributions
            seasonal = seasonal_effect(current_date)
            contributions_mtd = contributions_mtd * seasonal
            
            # Calculate withdrawals (random, but more common for older customers)
            withdrawals_mtd = 0
            age = (current_date - customer["birth_date"]).days / 365
            
            withdrawal_probability = 0.01  # Base 1% chance per month
            if age > 60:  # Retirement age
                withdrawal_probability = 0.05  # 5% chance
            
            if random.random() < withdrawal_probability:
                withdrawals_mtd = balance * random.uniform(0.01, 0.05)  # 1-5% withdrawal
                
            # Calculate investment returns based on market performance and risk
            risk_level = product["risk_level"]
            risk_index = RISK_LEVELS.index(risk_level)
            risk_factor = (risk_index + 1) / len(RISK_LEVELS)  # Normalize to 0-1
            
            # Average market performance this month
            avg_market = np.mean([m["sp500_index"] for m in monthly_market_data])
            avg_prev_market = np.mean([m["sp500_index"] for m in market_data 
                                    if m["date"].year == current_date.year and m["date"].month == current_date.month - 1]) \
                             if current_date.month > 1 else np.mean([m["sp500_index"] for m in monthly_market_data])
            
            market_return = (avg_market / avg_prev_market) - 1 if avg_prev_market > 0 else 0
            
            # Bond performance (inverse to market)
            avg_bonds = np.mean([m["bond_index"] for m in monthly_market_data])
            avg_prev_bonds = np.mean([m["bond_index"] for m in market_data 
                                   if m["date"].year == current_date.year and m["date"].month == current_date.month - 1]) \
                           if current_date.month > 1 else np.mean([m["bond_index"] for m in monthly_market_data])
            
            bond_return = (avg_bonds / avg_prev_bonds) - 1 if avg_prev_bonds > 0 else 0
            
            # Calculate weighted return based on risk profile
            # Higher risk = more market exposure, less bond exposure
            weighted_return = (market_return * risk_factor) + (bond_return * (1 - risk_factor))
            
            # Add some noise
            weighted_return += random.normalvariate(0, 0.005)
            
            # Calculate investment returns
            investment_returns_mtd = balance * weighted_return
            
            # Calculate fees
            annual_fee_pct = product["annual_fee_percentage"] / 100
            monthly_fee_pct = annual_fee_pct / 12
            monthly_fee_fixed = product["management_fee_fixed"] / 12 if product["management_fee_fixed"] > 0 else 0
            
            fees_mtd = (balance * monthly_fee_pct) + monthly_fee_fixed
            
            # Update balance
            balance = balance + contributions_mtd - withdrawals_mtd + investment_returns_mtd - fees_mtd
            
            # Record the balance
            writer.writerow([
                f"BAL{balance_id:08d}", customer_id, product_id, 
                current_date.strftime("%Y-%m-%d"), round(balance, 2),
                round(contributions_mtd, 2), round(withdrawals_mtd, 2),
                round(investment_returns_mtd, 2), round(fees_mtd, 2)
            ])
            
            balance_id += 1
            
            # Move to next month
            current_date = datetime.date(
                current_date.year + (current_date.month // 12), 
                (current_date.month % 12) + 1, 
                1
            )

# Generate Customer Service Interactions
interactions = []

with open(f"{output_dir}/service_interactions.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "interaction_id", "customer_id", "date", "channel", 
        "reason_code", "duration_minutes", "satisfaction_score", "resolution_status", "agent_id"
    ])
    
    for _ in range(NUM_INTERACTIONS):
        # Pick a random customer
        customer = random.choice(customers)
        customer_id = customer["customer_id"]
        
        # Generate interaction date
        interaction_date = random_date(
            max(customer["enrollment_date"], START_DATE),
            END_DATE
        )
        
        # Determine channel based on age and digital trend
        digital_affinity = customer["age_factors"]["digital_affinity"]
        digital_trend = digital_adoption_trend(interaction_date)
        
        if random.random() < digital_affinity * digital_trend:
            channel = random.choice(["Web", "Mobile App", "Email", "Chat"])
        else:
            channel = random.choice(["Phone", "In-person"])
            
        # Reason code
        reason_code = random.choice(REASON_CODES)
        
        # Duration varies by channel and reason
        if channel in ["Phone", "In-person"]:
            base_duration = random.randint(5, 30)
        else:
            base_duration = random.randint(2, 15)
            
        if reason_code in ["Complaint", "Transaction Issue"]:
            base_duration *= 1.5
            
        duration_minutes = int(base_duration)
        
        # Satisfaction score
        # Base satisfaction influenced by duration and reason
        base_satisfaction = 4.0  # Start with good satisfaction
        
        if duration_minutes > 20:
            base_satisfaction -= 0.5  # Longer interactions less satisfying
            
        if reason_code in ["Complaint", "Transaction Issue", "Technical Support"]:
            base_satisfaction -= 1.0  # Problem-based interactions less satisfying
            
        # Add random variation
        satisfaction_noise = random.normalvariate(0, 0.5)
        satisfaction_score = max(1, min(5, base_satisfaction + satisfaction_noise))
        
        # Resolution status
        if satisfaction_score >= 4.0:
            resolution_status = "Resolved"
        elif satisfaction_score >= 3.0:
            resolution_status = random.choice(["Resolved", "Partially Resolved"])
        else:
            resolution_status = random.choice(["Partially Resolved", "Unresolved"])
            
        # Agent ID 
        agent_id = f"AGT{random.randint(1, 100):04d}"
        
        interactions.append({
            "interaction_id": f"INT{_+1:06d}",
            "customer_id": customer_id,
            "date": interaction_date.strftime("%Y-%m-%d"),
            "channel": channel,
            "reason_code": reason_code,
            "duration_minutes": duration_minutes,
            "satisfaction_score": round(satisfaction_score, 1),
            "resolution_status": resolution_status,
            "agent_id": agent_id
        })
        
        writer.writerow([
            f"INT{_+1:06d}", customer_id, interaction_date.strftime("%Y-%m-%d"),
            channel, reason_code, duration_minutes, 
            round(satisfaction_score, 1), resolution_status, agent_id
        ])

# Generate Customer Engagement
engagements = []

with open(f"{output_dir}/engagement.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "engagement_id", "customer_id", "date", "action_type",
        "device_type", "session_duration", "pages_viewed", "actions_taken"
    ])
    
    for i in range(NUM_ENGAGEMENT):
        # Pick a random customer
        customer = random.choice(customers)
        customer_id = customer["customer_id"]
        
        # Generate engagement date
        engagement_date = random_date(
            max(customer["enrollment_date"], START_DATE),
            END_DATE
        )
        
        # Action type based on age
        action_type = random.choice(ACTION_TYPES)
        
        # Device type based on age
        digital_affinity = customer["age_factors"]["digital_affinity"]
        if random.random() < digital_affinity:
            device_type = random.choice(["Mobile Phone", "Tablet"])
        else:
            device_type = random.choice(["Desktop", "Smart TV", "Voice Assistant"])
        
        # Session duration
        if action_type in ["Login", "Update Profile", "Download Statement"]:
            session_minutes = random.randint(1, 5)
        elif action_type in ["Research Product", "Watch Educational Video", "Use Planning Tool"]:
            session_minutes = random.randint(5, 30)
        else:
            session_minutes = random.randint(2, 10)
            
        # Pages viewed
        pages_viewed = max(1, int(session_minutes / 2))
        
        # Actions taken
        actions_taken = max(1, int(pages_viewed / 2))
        
        engagements.append({
            "engagement_id": f"ENG{i+1:07d}",
            "customer_id": customer_id,
            "date": engagement_date.strftime("%Y-%m-%d"),
            "action_type": action_type,
            "device_type": device_type, 
            "session_duration": session_minutes,
            "pages_viewed": pages_viewed,
            "actions_taken": actions_taken
        })
        
        writer.writerow([
            f"ENG{i+1:07d}", customer_id, engagement_date.strftime("%Y-%m-%d"),
            action_type, device_type, session_minutes, pages_viewed, actions_taken
        ])

# Generate Customer Retention/Churn
# We'll churn a small percentage of customers
with open(f"{output_dir}/retention.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "customer_id", "product_id", "churn_date", "churn_reason",
        "exit_survey_score", "recovered_flag", "total_customer_lifetime_value"
    ])
    
    # Choose ~5% of enrollments to churn
    churn_enrollments = random.sample(enrollments, int(len(enrollments) * 0.05))
    
    for enrollment in churn_enrollments:
        customer_id = enrollment["customer_id"]
        product_id = enrollment["product_id"]
        enrollment_date = enrollment["enrollment_date"]
        
        # Churn date is at least 90 days after enrollment and before end date
        min_churn = enrollment_date + datetime.timedelta(days=90)
        if min_churn >= END_DATE:
            continue
            
        churn_date = random_date(min_churn, END_DATE)
        
        # Find related data for this customer+product
        customer = next(c for c in customers if c["customer_id"] == customer_id)
        
        # Find interactions for this customer
        customer_interactions = [i for i in interactions if i["customer_id"] == customer_id]
        
        # Determine churn reason based on interaction history
        if any(i["resolution_status"] == "Unresolved" for i in customer_interactions) and random.random() < 0.7:
            churn_reason = "Service Issue"
        elif any(i["reason_code"] == "Fee Inquiry" for i in customer_interactions) and random.random() < 0.5:
            churn_reason = "Fee Concerns"
        else:
            churn_reason = random.choice(CHURN_REASONS)
            
        # Exit survey score
        if churn_reason in ["Service Issue", "Fee Concerns", "Poor Performance", "Product Dissatisfaction"]:
            exit_survey_score = random.uniform(1.0, 3.0)
        else:
            exit_survey_score = random.uniform(2.0, 4.0)
            
        # Recovery flag
        recovered_flag = "No"
        if exit_survey_score > 3.0 and random.random() < 0.3:
            recovered_flag = "Yes"
            
        # Calculate lifetime value
        # Sum of all balances * fee percentage, plus fixed fees
        # We'll approximate with their enrollment details
        enrollment_duration_years = (churn_date - enrollment_date).days / 365
        annual_fees = enrollment["initial_investment"] * (product["annual_fee_percentage"] / 100)
        fixed_fees = product["management_fee_fixed"] * 12
        total_annual_revenue = annual_fees + fixed_fees
        lifetime_value = total_annual_revenue * enrollment_duration_years
        
        writer.writerow([
            customer_id, product_id, churn_date.strftime("%Y-%m-%d"),
            churn_reason, round(exit_survey_score, 1), recovered_flag,
            round(lifetime_value, 2)
        ])

print(f"Synthetic financial dataset generated in the '{output_dir}' directory.")
print(f"Generated {len(customers)} customers, {len(products)} products, and {len(enrollments)} enrollments.")
print(f"Generated {balance_id} account balance records, {len(interactions)} service interactions.")
print(f"Generated {len(engagements)} engagement records and {len(market_data)} market data points.")
