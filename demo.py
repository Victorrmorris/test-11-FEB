import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------- Page Configuration -------------------- #
st.set_page_config(page_title="DECC Automated Savings", layout="wide")

# -------------------- Sidebar -------------------- #
st.sidebar.header("📊 DECC Automated Savings Dashboard")

# User selects round-up method
round_up_type = st.sidebar.selectbox(
    "Select Round-Up Method",
    ["Nearest $1", "Nearest $5", "Nearest $10"]
)

# User sets savings goal
monthly_savings_goal = st.sidebar.number_input(
    "Set Your Monthly Savings Goal ($)", min_value=10, value=500, step=50
)

# -------------------- Checking Accounts -------------------- #
st.title("🏦 Linked Checking Accounts & Savings")

# Hardcoded checking account balances
checking_accounts = pd.DataFrame({
    "Account": ["USAA Checking", "AMEX Savings", "Germany Checking", "Wise", "Greenlight (Kids)"],
    "Balance ($)": [4500.13, 20348.05, 233.81, 198.76, 300.00]
})

# Display checking accounts
st.write("### 💰 Checking Account Balances")
st.table(checking_accounts)

# -------------------- Simulated Round-Up Savings -------------------- #
st.write("### 🔄 Simulated Round-Up Savings Across Accounts")

# Hardcoded round-up savings per account
round_up_savings = {
    "USAA Checking": 78.62,
    "Germany Checking": 32.19,
    "Wise": 59.12,
    "Greenlight": 24.56
}

# Create DataFrame for visualization
df_savings = pd.DataFrame(list(round_up_savings.items()), columns=["Account", "Round-Up Savings ($)"])

# Display total savings
total_round_up_savings = df_savings["Round-Up Savings ($)"].sum()
st.metric("Total Simulated Round-Up Savings", f"${total_round_up_savings:.2f}")

# Plot bar chart for savings distribution
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(df_savings["Account"], df_savings["Round-Up
