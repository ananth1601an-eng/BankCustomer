import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Bank Churn Dashboard",
    page_icon="🏦",
    layout="wide"
)

# 2. Load Dataset safely
@st.cache_data
def load_data():
    df = pd.read_csv("bank_churn_dataset.csv")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Could not find 'bank_churn_dataset.csv'. Please make sure it is in the same directory as app.py.")
    st.stop()

# 3. Main Header
st.title("🏦 Bank Customer Churn Analysis Dashboard")
st.markdown("Monitor customer metrics, segmentation, and risk characteristics dynamically.")
st.markdown("---")

# 4. Sidebar Navigation & Filters
st.sidebar.header("🎯 Filter Options")

# Segment Filter
all_segments = ["All"] + list(df['customer_segment'].unique())
selected_segment = st.sidebar.selectbox("Select Customer Segment", all_segments)

# Risk Segment Filter
all_risks = ["All"] + list(df['risk_segment'].unique())
selected_risk = st.sidebar.selectbox("Select Risk Segment", all_risks)

# Filter Logic
filtered_df = df.copy()
if selected_segment != "All":
    filtered_df = filtered_df[filtered_df['customer_segment'] == selected_segment]
if selected_risk != "All":
    filtered_df = filtered_df[filtered_df['risk_segment'] == selected_risk]

# 5. Top-Level KPI Dashboard Metrics
total_customers = len(filtered_df)
churn_rate = (filtered_df['exit'].sum() / total_customers) * 100 if total_customers > 0 else 0
avg_credit = filtered_df['credit_sco'].mean() if total_customers > 0 else 0
avg_balance = filtered_df['balance'].mean() if total_customers > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Customers Covered", f"{total_customers:,}")
with col2:
    st.metric("Overall Churn Rate", f"{churn_rate:.2f}%")
with col3:
    st.metric("Average Credit Score", f"{int(avg_credit)}")
with col4:
    st.metric("Average Balance", f"{avg_balance:,.0f} VND")

st.markdown("---")

# 6. Interactive Multi-column Data Visualization Layout
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("📊 Churn Status Breakdown")
    # Convert bool to readable string for clean plotting labels
    plot_df = filtered_df.copy()
    plot_df['Exited Status'] = plot_df['exit'].map({True: 'Churned (Exited)', False: 'Retained'})
    fig_exit = px.pie(plot_df, names='Exited Status', hole=0.4, 
                      color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_exit, use_container_width=True)

with row1_col2:
    st.subheader("👥 Age vs. Credit Score Profile")
    fig_scatter = px.scatter(filtered_df, x='age', y='credit_sco', 
                             color='exit', color_discrete_map={True: '#EF553B', False: '#636EFA'},
                             labels={'exit': 'Has Exited', 'age': 'Customer Age', 'credit_sco': 'Credit Score'},
                             opacity=0.6)
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("💼 Customer Loyalty Level Split")
    fig_loyalty = px.histogram(filtered_df, x='loyalty_level', color='exit', barmode='group',
                               labels={'loyalty_level': 'Loyalty Tier', 'exit': 'Exited'},
                               color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_loyalty, use_container_width=True)

with row2_col2:
    st.subheader("📱 Preferred Digital Behavior")
    fig_digital = px.bar(filtered_df.groupby(['digital_behavior', 'exit']).size().reset_index(name='count'),
                         x='digital_behavior', y='count', color='exit',
                         labels={'digital_behavior': 'Channels Used', 'count': 'Customer Base'},
                         barmode='stack')
    st.plotly_chart(fig_digital, use_container_width=True)

# 7. Raw Data Explorer Section
st.markdown("---")
st.subheader("🔍 Filtered Data Inspection Window")
st.dataframe(filtered_df[['id', 'full_name', 'gender', 'age', 'occupation', 'balance', 'customer_segment', 'risk_segment', 'exit']].head(100))