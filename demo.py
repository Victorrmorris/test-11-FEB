import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# -------------------- Global Style -------------------- #
plt.style.use('seaborn-whitegrid')  # Use a clean Seaborn style for all charts

# -------------------- Page Configuration -------------------- #
st.set_page_config(page_title="DECC Automated Savings", layout="wide", initial_sidebar_state="expanded")

# -------------------- Sidebar -------------------- #
with st.sidebar:
    st.header("📊 DECC Automated Savings Dashboard")
    # User selects the round-up method
    round_up_type = st.selectbox("Select Round-Up Method", ["Nearest $1", "Nearest $5", "Nearest $10"])
    # User sets the desired monthly savings goal
    monthly_savings_goal = st.number_input("Set Your Monthly Savings Goal ($)", min_value=10, value=500, step=50)

# Define multipliers for dummy data based on round-up method selection.
# Base data (for "Nearest $1") represents total monthly round-up savings of $194.49.
multipliers = {"Nearest $1": 1, "Nearest $5": 5, "Nearest $10": 10}
multiplier = multipliers[round_up_type]

# -------------------- Dummy Data for Round-Up Savings -------------------- #
# Base simulated round-up savings per account (for $1 round-up)
base_round_up = {
    "USAA Checking": 78.62,
    "Germany Checking": 32.19,
    "Wise": 59.12,
    "Greenlight": 24.56
}
# Apply the multiplier to simulate higher round-up savings
round_up_savings = {account: round(amount * multiplier, 2) for account, amount in base_round_up.items()}
total_round_up_savings = sum(round_up_savings.values())

# -------------------- Main Title and Checking Accounts -------------------- #
st.title("🏦 Linked Checking Accounts & Savings")
with st.container():
    st.subheader("💰 Checking Account Balances")
    checking_accounts = pd.DataFrame({
        "Account": ["USAA Checking", "Germany Checking", "Wise", "Greenlight (Kids)"],
        "Balance ($)": [4500.13, 233.81, 198.76, 300.00]
    })
    st.table(checking_accounts)

# -------------------- Savings Visualizations -------------------- #
with st.container():
    st.subheader("Savings Visualizations")
    col1, col2 = st.columns(2)

    # --- Left Column: Round-Up Savings Chart ---
    with col1:
        st.markdown("#### 🔄 Round-Up Savings by Checking Account")
        st.metric("Total Simulated Round-Up Savings (Monthly)", f"${total_round_up_savings:.2f}")
        
        # Prepare DataFrame for plotting
        df_savings = pd.DataFrame(list(round_up_savings.items()), columns=["Account", "Round-Up Savings ($)"])
        
        # Create figure and axis with improved resolution
        fig1, ax1 = plt.subplots(figsize=(8, 5), dpi=100)
        colors = ["#1E3A8A", "#4A90E2", "#72BF44", "#00C48C"]
        
        bars = ax1.bar(df_savings["Account"], df_savings["Round-Up Savings ($)"],
                       color=colors, edgecolor="black", linewidth=0.8)
        
        # Set titles and labels with adjusted font sizes
        ax1.set_title("Round-Up Savings by Checking Account", fontsize=16, fontweight="bold")
        ax1.set_xlabel("Accounts", fontsize=14)
        ax1.set_ylabel("Savings ($)", fontsize=14)
        ax1.tick_params(axis='x', labelrotation=20, labelsize=12)
        ax1.tick_params(axis='y', labelsize=12)
        
        # Remove the top and right spines for a cleaner look
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        
        # Add gridlines only for the y-axis
        ax1.yaxis.grid(True, linestyle="--", alpha=0.6)
        
        # Annotate each bar with its value
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, height + (0.02 * total_round_up_savings),
                     f"${height:.2f}", ha="center", va="bottom", fontsize=12, fontweight="bold")
        
        plt.tight_layout()
        st.pyplot(fig1, use_container_width=True)

    # --- Right Column: Projected Savings Growth Chart ---
    with col2:
        st.markdown("#### 📈 Projected Savings Growth")
        # Parameters for the compound interest simulation:
        initial_balance = 0
        monthly_contribution = total_round_up_savings
        annual_interest_rate = 0.038
        compounding_periods_per_year = 12
        years = 3

        # Calculate future values with monthly compounding and contributions
        future_values = []
        balance = initial_balance
        for month in range(1, years * 12 + 1):
            balance += monthly_contribution
            balance *= (1 + annual_interest_rate / compounding_periods_per_year)
            if month % 12 == 0:
                future_values.append(balance)

        df_growth = pd.DataFrame({
            "Year": list(range(1, years + 1)),
            "Projected Balance ($)": future_values
        })

        # Create figure and axis with improved resolution
        fig2, ax2 = plt.subplots(figsize=(8, 5), dpi=100)
        bar_color = "#4A90E2"
        bars = ax2.bar(df_growth["Year"], df_growth["Projected Balance ($)"],
                       color=bar_color, edgecolor="black", linewidth=0.8)
        
        ax2.set_title("Projected Savings Growth Over Time", fontsize=16, fontweight="bold")
        ax2.set_xlabel("Years", fontsize=14)
        ax2.set_ylabel("Total Savings ($)", fontsize=14)
        ax2.set_xticks(list(range(1, years + 1)))
        ax2.tick_params(axis='x', labelsize=12)
        ax2.tick_params(axis='y', labelsize=12)
        
        # Remove top and right spines for a modern look
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        
        # Add gridlines for y-axis
        ax2.yaxis.grid(True, linestyle="--", alpha=0.6)
        
        # Annotate each bar with its projected value
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2, height + (0.02 * height),
                     f"${height:,.2f}", ha="center", va="bottom", fontsize=12, fontweight="bold")
        
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)

# -------------------- AI-Driven Savings Insights -------------------- #
with st.container():
    st.subheader("🤖 AI Savings Insights")
    annual_savings = total_round_up_savings * 12
    if total_round_up_savings >= monthly_savings_goal:
        st.success(f"🚀 Great job! With the **{round_up_type}** method, you're projected to save **${annual_savings:,.2f}** annually.")
    else:
        additional_needed = monthly_savings_goal - total_round_up_savings
        st.warning(f"⚠️ You need to save **${additional_needed:.2f}** more per month with the **{round_up_type}** method to reach your goal.")
    st.info("💡 Tip: Experiment with different round-up methods to see how they impact your projected savings growth.")

# -------------------- Footer -------------------- #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
