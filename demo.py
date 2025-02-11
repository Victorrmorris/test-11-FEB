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
bars = ax.bar(df_savings["Account"], df_savings["Round-Up Savings ($)"], 
              color=["#1E3A8A", "#4A90E2", "#72BF44", "#00C48C"], 
              edgecolor="black")

# Set labels and title
ax.set_title("Round-Up Savings by Checking Account", fontsize=14, fontweight="bold")
ax.set_xlabel("Accounts", fontsize=12)
ax.set_ylabel("Savings ($)", fontsize=12)
plt.xticks(rotation=20)
plt.grid(axis="y", linestyle="--", alpha=0.5)

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 2, f"${height:.2f}", ha="center", fontsize=12, fontweight="bold")

# Display the chart in Streamlit
st.pyplot(fig)

# -------------------- Compounding Interest Simulation -------------------- #
st.write("### 📈 Projected Savings Growth")

# Define parameters
initial_balance = 0  # No initial savings
monthly_contribution = total_round_up_savings  # Amount saved via round-ups
annual_interest_rate = 0.038  # 3.80% APY for high-yield savings
compounding_periods_per_year = 12  # Monthly compounding
years = 3  # 3-year projection

# Calculate savings growth
future_values = []
years_list = list(range(1, years + 1))
balance = initial_balance

for month in range(1, years * 12 + 1):
    balance += monthly_contribution  # Add round-up savings
    balance *= (1 + annual_interest_rate / compounding_periods_per_year)  # Apply monthly interest
    if month % 12 == 0:  # Record yearly growth
        future_values.append(balance)

# Create a dataframe for visualization
df_growth_bar = pd.DataFrame({"Year": years_list, "Projected Balance ($)": future_values})

# Plot bar chart for savings growth
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(df_growth_bar["Year"], df_growth_bar["Projected Balance ($)"], color="#4A90E2", edgecolor="black")

# Set labels and title
ax.set_title("Projected Savings Growth Over Time", fontsize=14, fontweight="bold")
ax.set_xlabel("Years", fontsize=12)
ax.set_ylabel("Total Savings ($)", fontsize=12)

# Add value labels on top of bars
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 500, f"${height:,.2f}", ha="center", fontsize=12, fontweight="bold")

plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.xticks(years_list)
plt.tight_layout()

st.pyplot(fig)

# -------------------- AI-Driven Savings Insights -------------------- #
st.write("### 🤖 AI Savings Insights")

if total_round_up_savings >= monthly_savings_goal:
    st.success(f"🚀 Great job! You're on track to save **${total_round_up_savings * 12:.2f}** this year.")
else:
    additional_needed = monthly_savings_goal - total_round_up_savings
    st.warning(f"⚠️ You need to save **${additional_needed:.2f}** more to reach your goal.")

st.info("💡 Tip: Try switching to a higher round-up amount or adjusting savings targets.")

# -------------------- Footer -------------------- #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
