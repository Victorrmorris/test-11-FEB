import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------- Page Configuration -------------------- #
st.set_page_config(page_title="DECC Savings MVP", layout="wide")

# -------------------- Sidebar -------------------- #
st.sidebar.header("📊 DECC Automated Savings MVP")

# User selects round-up method
round_up_type = st.sidebar.selectbox(
    "Select Round-Up Method",
    ["Nearest $1", "Nearest $5", "Nearest $10"]
)

# User sets savings goal
monthly_savings_goal = st.sidebar.number_input(
    "Set Your Monthly Savings Goal ($)", min_value=10, value=500, step=50
)

# File upload for mock transactions
uploaded_file = st.sidebar.file_uploader("Upload Transactions (CSV)", type=["csv"])

# -------------------- Simulated Transactions -------------------- #
st.title("💰 DECC Savings Simulator")

# If no file is uploaded, show a sample dataset
if uploaded_file is None:
    st.info("📂 Upload a CSV file with mock transactions, or use the sample dataset below.")

    # Sample transaction data
    transactions = pd.DataFrame({
        "Date": ["2024-02-01", "2024-02-02", "2024-02-03", "2024-02-04"],
        "Description": ["Coffee", "Groceries", "Gym", "Dinner"],
        "Amount ($)": [3.75, 42.10, 25.99, 18.45]
    })
else:
    transactions = pd.read_csv(uploaded_file)

# Show transaction table
st.write("### 📋 Transactions")
st.table(transactions)

# -------------------- Calculate Round-Up Savings -------------------- #
st.write("### 🔄 Simulated Round-Up Savings")

# Determine round-up savings based on user selection
round_up_amount = int(round_up_type.split("$")[1])  # Extract nearest round-up value
transactions["Round-Up ($)"] = transactions["Amount ($)"].apply(
    lambda x: round_up_amount - (x % round_up_amount) if x % round_up_amount != 0 else 0
)

# Calculate total savings
total_round_up_savings = transactions["Round-Up ($)"].sum()

# Display total savings
st.metric("Total Simulated Round-Up Savings", f"${total_round_up_savings:.2f}")

# -------------------- Compounding Interest Simulation -------------------- #
st.write("### 📈 Savings Growth Projection")

# Define parameters
initial_balance = 0  # No initial savings
monthly_contribution = total_round_up_savings  # Amount saved via round-ups
annual_interest_rate = 0.045  # 4.5% APY
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

# Plot bar chart instead of a line chart
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(df_growth_bar["Year"], df_growth_bar["Projected Balance ($)"], color="#4A90E2", edgecolor="black")

# Set labels and title
ax.set_title("Projected Savings Growth Over Time", fontsize=14, fontweight="bold")
ax.set_xlabel("Years", fontsize=12)
ax.set_ylabel("Total Savings ($)", fontsize=12)

# Add value labels on top of bars
for i, v in enumerate(future_values):
    ax.text(years_list[i], v + 500, f"${v:,.2f}", ha="center", fontsize=12, fontweight="bold")

plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.xticks(years_list)
plt.tight_layout()

# Display the bar chart in Streamlit
st.pyplot(fig)

# -------------------- AI-Driven Savings Insights -------------------- #
st.write("### 🤖 AI Savings Insights")

if total_round_up_savings >= monthly_savings_goal:
    st.success("🚀 Great job! You're meeting your savings goal.")
else:
    additional_needed = monthly_savings_goal - total_round_up_savings
    st.warning(f"⚠️ You need to save **${additional_needed:.2f}** more to reach your goal.")

st.info("💡 Tip: Try switching to a higher round-up amount or reducing unnecessary expenses.")

# -------------------- Footer -------------------- #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
