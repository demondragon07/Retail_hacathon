import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- 1. SETUP MOCK MASTER DATA ---
stores = ['S001', 'S002', 'S003']
products = ['P001', 'P002', 'P003', 'P004', 'P005']
customers = ['C101', 'C102', 'C103', 'C104', 'C105']
promos = ['PR10', 'PR20', None]

def generate_retail_data():
    header_data = []
    line_data = []
    
    print("Generating raw data with anomalies...")
    
    for i in range(1, 1000):  # Generate 1000 transactions
        txn_id = f"TXN_{1000+i}"
        cust_id = random.choice(customers)
        store_id = random.choice(stores)
        date = datetime.now() - timedelta(days=random.randint(0, 10))
        
        # INJECTING ANOMALIES (Use Case 1)
        # 5% chance of negative amount, 5% chance of missing customer
        total_amount = round(random.uniform(20, 500), 2)
        if random.random() < 0.05: total_amount = -50.00  # Anomaly 1
        if random.random() < 0.05: cust_id = None        # Anomaly 2
        
        header_data.append([txn_id, cust_id, store_id, date, total_amount])
        
        # Generate 1-3 line items per transaction
        for j in range(random.randint(1, 3)):
            line_id = (i * 10) + j
            prod_id = random.choice(products)
            promo = random.choice(promos)
            qty = random.randint(1, 5)
            # Anomaly 3: Some quantities as zero or negative
            if random.random() < 0.02: qty = -1 
            
            line_data.append([line_id, txn_id, prod_id, promo, qty, round(qty * 25.5, 2)])

    # Convert to DataFrames
    df_header = pd.DataFrame(header_data, columns=['transaction_id', 'customer_id', 'store_id', 'transaction_date', 'total_amount'])
    df_line = pd.DataFrame(line_data, columns=['line_item_id', 'transaction_id', 'product_id', 'promotion_id', 'quantity', 'line_item_amount'])

    # Save Raw Files
    df_header.to_csv('sales_header_raw.csv', index=False)
    df_line.to_csv('sales_line_items_raw.csv', index=False)
    
    # --- USE CASE 1: DATA QUALITY PIPELINE (The "Logic") ---
    print("Running Quality Validation Pipeline...")
    
    # Identify Bad Records
    bad_header = df_header[(df_header['total_amount'] <= 0) | (df_header['customer_id'].isna())]
    clean_header = df_header[~df_header.index.isin(bad_header.index)]
    
    # Save Outputs
    clean_header.to_csv('sales_header_clean.csv', index=False)
    bad_header.to_csv('quarantine_header.csv', index=False)
    
    print(f"Success! Generated {len(df_header)} records.")
    print(f"Clean Records: {len(clean_header)} | Quarantined: {len(bad_header)}")

if __name__ == "__main__":
    generate_retail_data()