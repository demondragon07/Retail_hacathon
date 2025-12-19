# RetailInsight 360: End-to-End Analytics Pipeline

RetailInsight 360 is a comprehensive data engineering solution designed to transform raw, fragmented retail transactions into actionable business intelligence. Developed for the **Retail Data Processing Hackathon**, this project covers the full data lifecycle—from ingestion and quality validation to customer loyalty engagement.

## 📊 Project Overview
The system processes high-volume sales data to provide insights across six core business use cases, ensuring data integrity while maximizing customer lifetime value.



### Core Use Cases Implemented
* **UC1: Automated Data Ingestion & Quality Validation:** A robust pipeline that segregates "bad" data (negative amounts, missing product IDs, or invalid store IDs) into a Quarantine table.
* **UC2: Promotion Effectiveness Analyzer:** Measures sales volume and revenue for items purchased under specific promotions versus a baseline to identify high-ROI strategies.
* **UC3: Loyalty Point Calculation Engine:** Automates reward accrual using defined business logic ($1 = 1 point, plus bonuses for high-value transactions).
* **UC4: Customer Segmentation:** Identifies "At-Risk" (60+ days since last purchase) and "High-Spender" (top 10% by total monetary value) segments using RFM metrics.
* **UC5: Automated Notification System:** Generates personalized email templates confirming newly earned points and total accrued points to complete the loyalty loop.
* **UC6: Inventory & Performance Correlation:** Quantifies potential lost sales by correlating store stock-outs with top-selling products.

---

## 🛠️ Technical Stack
* **Language:** Python 3.x
* **Data Processing:** Pandas
* **Dashboard:** Streamlit
* **Visualization:** Plotly
* **Database Logic:** SQL-based Staging (Simulating PostgreSQL/MySQL cloud capabilities)

---

## 📂 File Structure
* `data_gen.py`: Simulates 7 days of sales data and performs the **UC1** quality validation.
* `analysis.py`: Contains the core logic for **UC2 through UC6**, including loyalty calculations, RFM segmentation, and lost sales analysis.
* `app.py`: A Streamlit dashboard to visualize KPIs, promo lift, and customer segments.
* `sales_header_clean.csv`: Cleaned transaction headers ready for analysis.
* `quarantine_header.csv`: Records rejected during the quality check for later analysis and reporting.

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install the required dependencies:
```bash
pip install pandas plotly streamlit
```
### 2. Run the PipelineExecute the scripts in the following order to ensure data consistency:
* `Generate Data`: Creates raw and quarantined data.
      ``` python data_gen.py ```
* `Analyze Data`: Calculates loyalty, segments, and lost sales.
  ``` python analysis.py ```
* `Launch Dashboard`: Visualizes all project KPIs.
  ``` streamlit run app.py ```

 ---
 
## 📈 Business LogicApplied 

### Loyalty Accrual (UC3)
Points are earned for every eligible transaction based on the following logic:
* **Base:** 1 point for every $1 spent.
* **Bonus:** 50 points for any purchase over a $100 threshold.
### Customer Segmentation (UC4)
Customers are categorized into actionable segments using aggregated sales data:
* **High-Spenders:** Top 10% by total monetary value.
* **At-Risk:** Customers who have not shopped in 60+ days but have an existing point balance.
### Lost Sales Calculation (UC6)
To identify revenue leakage for the Top 5 best-selling products, we apply the following formula:
* **Formula:** ```Estimated Lost Sales = (Avg Daily Sales X Days Out-of-Stock) X (Unit Price)```.

---

## 🏁 Conclusion

This solution demonstrates a successful end-to-end cycle from ingestion to engagement. By automating complex calculations and rigid quality checks, the system empowers data-driven decisions that enhance operational efficiency and customer engagement.
