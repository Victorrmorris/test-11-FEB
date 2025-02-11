import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------- Page Configuration -------------------- #
st.set_page_config(page_title="DECC Automated Savings", layout="wide", initial_sidebar_state="expanded")

# -------------------- Sidebar -------------------- #
with st.sidebar:
    st.header("📊 DECC Automated Savings Dashboard")
    round_up_type = st.selectbox("Select Round-Up Method", ["Nearest $1", "Nearest $5", "Nearest $10"])
    monthly_savings_goal = st.number_input("Set Your Monthly Savings Goal ($)", min_value=10, value=500, step=50)

# -------------------- Main Title -------------------- #
st.title("🏦 Linked Checking Accounts & Savings")

# -------------------- Checking Accounts -------------------- #
with st.container():
    st.subheader("💰 Checking Account Balances")
    checking_accounts = pd.DataFrame({
        "Account": ["USAA Checking", "AMEX Savings", "Germany Checking", "Wise", "Greenlight (Kids)"],
        "Balance ($)": [4500.13, 20348.05, 233.81, 198.76, 300.00]
    })
    st.table(checking_accounts)

# -------------------- Savings Visualizations -------------------- #
with st.container():
    st.subheader("Savings Visualizations")
    col1, col2 = st.columns(2)

    # --- Simulated Round-Up Savings ---
    with col1:
        st.markdown("#### 🔄 Round-Up Savings by Checking Account")
        # Hardcoded round-up savings data
        round_up_savings = {
            "USAA Checking": 78.62,
            "Germany Checking": 32.19,
            "Wise": 59.12,
            "Greenlight": 24.56
        }
        df_savings = pd.DataFrame(list(round_up_savings.items()), columns=["Account", "Round-Up Savings ($)"])
        total_round_up_savings = df_savings["Round-Up Savings ($)"].sum()
        
        st.metric("Total Simulated Round-Up Savings", f"${total_round_up_savings:.2f}")

        # Plotting the bar chart for round-up savings
        fig1, ax1 = plt.subplots(figsize=(7, 4))
        colors = ["#1E3A8A", "#4A90E2", "#72BF44", "#00C48C"]
        bars = ax1.bar(df_savings["Account"], df_savings["Round-Up Savings ($)"],
                       color=colors, edgecolor="black")
        ax1.set_title("Round-Up Savings by Checking Account", fontsize=14, fontweight="bold")
        ax1.set_xlabel("Accounts", fontsize=12)
        ax1.set_ylabel("Savings ($)", fontsize=12)
        ax1.grid(axis="y", linestyle="--", alpha=0.5)
        plt.xticks(rotation=20)
        # Adding value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, height + 2,
                     f"${height:.2f}", ha="center", fontsize=12, fontweight="bold")
        st.pyplot(fig1)

    # --- Compounding Interest Simulation ---
    with col2:
        st.markdown("#### 📈 Projected Savings Growth")
        # Parameters for the compound interest simulation
        initial_balance = 0  
        monthly_contribution = total_round_up_savings  # Using simulated round-up savings as monthly contribution
        annual_interest_rate = 0.038  # 3.80% APY
        compounding_periods_per_year = 12  # Monthly compounding
        years = 3  # 3-year projection

        # Calculate projected savings growth
        future_values = []
        years_list = list(range(1, years + 1))
        balance = initial_balance

        for month in range(1, years * 12 + 1):
            balance += monthly_contribution
            balance *= (1 + annual_interest_rate / compounding_periods_per_year)
            if month % 12 == 0:
                future_values.append(balance)

        df_growth = pd.DataFrame({"Year": years_list, "Projected Balance ($)": future_values})

        # Plotting the projected savings growth
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        bars = ax2.bar(df_growth["Year"], df_growth["Projected Balance ($)"],
                       color="#4A90E2", edgecolor="black")
        ax2.set_title("Projected Savings Growth Over Time", fontsize=14, fontweight="bold")
        ax2.set_xlabel("Years", fontsize=12)
        ax2.set_ylabel("Total Savings ($)", fontsize=12)
        ax2.grid(axis="y", linestyle="--", alpha=0.5)
        ax2.set_xticks(years_list)
        # Adding value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2, height + 500,
                     f"${height:,.2f}", ha="center", fontsize=12, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig2)

# -------------------- AI-Driven Savings Insights -------------------- #
with st.container():
    st.subheader("🤖 AI Savings Insights")
    # Compare simulated monthly savings against the user's monthly savings goal
    if total_round_up_savings >= monthly_savings_goal:
        st.success(f"🚀 Great job! You're on track to save **${total_round_up_savings * 12:.2f}** this year.")
    else:
        additional_needed = monthly_savings_goal - total_round_up_savings
        st.warning(f"⚠️ You need to save **${additional_needed:.2f}** more per month to reach your goal.")
    st.info("💡 Tip: Consider switching to a higher round-up amount or adjusting your savings target for better results.")

# -------------------- Footer -------------------- #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
