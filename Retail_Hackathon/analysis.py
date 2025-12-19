import pandas as pd
import random  
from datetime import datetime, timedelta

# 1. Load the Clean Data we generated in Step 2
df_sales = pd.read_csv('sales_header_clean.csv')

# --- USE CASE 3: Loyalty Point Calculation Engine ---
def calculate_loyalty_points(row):
    # Rule: $1 = 1 Point
    base_points = int(row['total_amount']) 
    # Rule: Bonus 50 points for purchases over $100
    bonus = 50 if row['total_amount'] > 100 else 0
    return base_points + bonus

df_sales['points_earned'] = df_sales.apply(calculate_loyalty_points, axis=1)

# Aggregating points per customer
loyalty_summary = df_sales.groupby('customer_id')['points_earned'].sum().reset_index()
loyalty_summary.columns = ['customer_id', 'total_accrued_points']


# --- USE CASE 4: Customer Segmentation (RFM) ---
# We simulate 'Recency' by checking the last purchase date
df_sales['transaction_date'] = pd.to_datetime(df_sales['transaction_date'])
today = datetime.now()

customer_stats = df_sales.groupby('customer_id').agg({
    'transaction_date': 'max',      # Most recent purchase (Recency)
    'transaction_id': 'count',      # Number of visits (Frequency)
    'total_amount': 'sum'           # Total spend (Monetary)
}).reset_index()

def segment_customer(row):
    days_since_last_purchase = (today - row['transaction_date']).days
    
    # Logic for "At-Risk" (Use Case 4)
    if days_since_last_purchase > 60:
        return 'At-Risk'
    # Logic for "High-Spender" (Top 20% in this mock)
    elif row['total_amount'] > 300:
        return 'High-Spender'
    else:
        return 'Regular'

customer_stats['segment'] = customer_stats.apply(segment_customer, axis=1)


# --- SAVE THE RESULTS ---
loyalty_summary.to_csv('loyalty_results.csv', index=False)
customer_stats.to_csv('customer_segments.csv', index=False)

print("--- Analysis Complete ---")
print(f"Loyalty Points calculated for {len(loyalty_summary)} customers.")
print(f"Customer Segments identified: {customer_stats['segment'].value_counts().to_dict()}")

# --- USE CASE 2: Promotion Effectiveness ---
# Join sales with promo details (simulated)
df_lines = pd.read_csv('sales_line_items_raw.csv')

# Calculate revenue per promotion
promo_perf = df_lines.groupby('promotion_id')['line_item_amount'].sum().reset_index()
# Calculate lift (vs no promo/baseline)
baseline_sales = promo_perf[promo_perf['promotion_id'].isna()]['line_item_amount'].sum()
promo_perf['lift_percentage'] = ((promo_perf['line_item_amount'] - baseline_sales) / baseline_sales * 100).round(2)

# --- USE CASE 5: Automated Notification Simulator ---
# We take the loyalty results and generate a "Personalized Email Template"
df_loyalty = pd.read_csv('loyalty_results.csv')
df_loyalty['email_subject'] = "Your Rewards Update!"
df_loyalty['email_body'] = df_loyalty.apply(lambda x: 
    f"Hi {x['customer_id']}, you earned new points! Your total balance is now {x['total_accrued_points']}.", axis=1)

# --- USE CASE 6: Inventory Correlation (The 'Lost Sales' Logic) ---
# We simulate a "Stock Out" scenario for the Top 5 products
top_5_products = df_lines.groupby('product_id')['quantity'].sum().nlargest(5).index
inventory_issues = []
for prod in top_5_products:
    days_oos = random.randint(1, 5) # Simulating days out of stock
    lost_revenue = days_oos * (df_lines[df_lines['product_id'] == prod]['line_item_amount'].mean())
    inventory_issues.append({'product_id': prod, 'days_oos': days_oos, 'lost_revenue': round(lost_revenue, 2)})

df_inventory = pd.DataFrame(inventory_issues)

# Save the new analysis files
promo_perf.to_csv('promo_effectiveness.csv', index=False)
df_loyalty.to_csv('notifications.csv', index=False)
df_inventory.to_csv('inventory_analysis.csv', index=False)

print("Use Cases 2, 5, and 6 analyzed successfully.")