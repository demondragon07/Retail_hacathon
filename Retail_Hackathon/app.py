import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retail Hackathon Dashboard", layout="wide")

st.title("🚀 Retail Data Processing Insights")
st.markdown("---")

# Load the data we analyzed in the previous steps
try:
    df_loyalty = pd.read_csv('loyalty_results.csv')
    df_segments = pd.read_csv('customer_segments.csv')
    df_quarantine = pd.read_csv('quarantine_header.csv')
except FileNotFoundError:
    st.error("Missing CSV files! Please run analysis.py first.")

# --- ROW 1: Data Quality & Loyalty ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Use Case 1: Data Quality Proof")
    st.write(f"Items rejected and sent to Quarantine: **{len(df_quarantine)}**")
    st.dataframe(df_quarantine.head(5))
    st.caption("These records had negative amounts or missing IDs.")

with col2:
    st.subheader("🏆 Use Case 3: Loyalty Leaderboard")
    top_loyalty = df_loyalty.sort_values('total_accrued_points', ascending=False).head(5)
    fig_points = px.bar(top_loyalty, x='customer_id', y='total_accrued_points', 
                        color='total_accrued_points', title="Top 5 Customers by Points")
    st.plotly_chart(fig_points, use_container_width=True)

# --- ROW 2: Segmentation ---
st.markdown("---")
st.subheader("🎯 Use Case 4: Customer Segmentation (RFM)")
col3, col4 = st.columns([1, 2])

with col3:
    segment_counts = df_segments['segment'].value_counts().reset_index()
    fig_pie = px.pie(segment_counts, values='count', names='segment', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    st.write("### Targeted Action List")
    at_risk = df_segments[df_segments['segment'] == 'At-Risk'][['customer_id', 'transaction_date']]
    st.warning(f"Found {len(at_risk)} At-Risk customers who haven't shopped in 60+ days!")
    st.dataframe(at_risk)

st.markdown("---")
# Load the new data
df_promo = pd.read_csv('promo_effectiveness.csv')
df_inv = pd.read_csv('inventory_analysis.csv')
df_notif = pd.read_csv('notifications.csv')

col5, col6 = st.columns(2)

with col5:
    st.subheader("📈 Use Case 2: Promo Effectiveness")
    fig_lift = px.bar(df_promo.dropna(), x='promotion_id', y='lift_percentage', 
                      title="Sales Lift % per Promotion", color='lift_percentage')
    st.plotly_chart(fig_lift)

with col6:
    st.subheader("📦 Use Case 6: Inventory & Lost Sales")
    st.dataframe(df_inv)
    st.error(f"Estimated Revenue Leakage: ${df_inv['lost_revenue'].sum()}")

st.markdown("---")
st.subheader("📧 Use Case 5: Automated Loyalty Notifications")
st.write("Preview of generated emails for customer engagement:")
st.table(df_notif[['customer_id', 'email_subject', 'email_body']].head(3))    