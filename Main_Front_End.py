import streamlit as st
import pandas as pd
#to run type streamlit run (file_directory).py in terminal

st.set_page_config(page_title="Budgeting Dashboard", layout="wide")

# --- NAVIGATION ---
page = st.sidebar.radio("Navigate", ["🏠 Home", "📊 Past Spendings", "🎯 Budgeting Goals", "🔮 Future Predictions"])

# --- SESSION STATE FOR USER INPUTS ---
if "monthly_income" not in st.session_state:
    st.session_state.monthly_income = 0
if "yearly_income" not in st.session_state:
    st.session_state.yearly_income = 0
if "goal_percent" not in st.session_state:
    st.session_state.goal_percent = 0

# --- HOME PAGE ---
if page == "🏠 Home":
    st.title("🏠 Home Page")
    st.write("Welcome to your budgeting dashboard!")

    st.subheader("Enter your income & savings goal:")

    monthly_income = st.number_input("Monthly Income ($)", min_value=0, step=100)
    goal_percent = st.slider("Percentage of income you want to save (%)", 0, 100, 20)

    if monthly_income > 0:
        st.session_state.monthly_income = monthly_income
        st.session_state.yearly_income = monthly_income * 12
        st.session_state.goal_percent = goal_percent

        st.success(f"Stored ✅: Monthly = ${monthly_income}, Yearly = ${monthly_income*12}, Save Goal = {goal_percent}%")

# --- PAST SPENDINGS ---
elif page == "📊 Past Spendings":
    st.title("📊 Past Spendings")

    option = st.selectbox("Choose dataset:", ["store_frequency_amt.csv", "store_frequency_avg_amt.csv"])
    df = pd.read_csv(option)

    # remove total row
    df = df[df["Store"].str.lower() != "total"]

    st.subheader(f"Viewing: {option}")
    st.dataframe(df, use_container_width=True)

    if "Total Spent ($)" in df.columns:
        st.bar_chart(df.set_index("Store")["Total Spent ($)"])
    elif "Avg Spent ($)" in df.columns:
        st.bar_chart(df.set_index("Store")["Avg Spent ($)"])

# --- BUDGETING GOALS ---
# --- BUDGETING GOALS ---
# --- BUDGETING GOALS ---
elif page == "🎯 Budgeting Goals":
    st.title("🎯 Budgeting Goals")

    if st.session_state.monthly_income == 0:
        st.warning("⚠️ Please enter your income & goal on the Home page first.")
    else:
        # Load the average spend CSV
        df = pd.read_csv("store_frequency_avg_amt.csv")
        df = df[df["Store"].str.lower() != "total"]

        # Separate out outliers (Count = 1)
        outliers = df[df["Count (avg/month)"] == 1]
        main_df = df[df["Count (avg/month)"] > 1]

        if not outliers.empty:
            total_outlier_avg = outliers["Avg Spent ($)"].sum()
            main_df = pd.concat([main_df, pd.DataFrame({
                "Store": ["Outliers"],
                "Count (avg/month)": [len(outliers)],
                "Avg Spent ($)": [total_outlier_avg]
            })], ignore_index=True)

        # Total avg spend for scaling
        total_spent = main_df["Avg Spent ($)"].sum()

        # Available budget = income * (1 - save%)
        allowed_spend = st.session_state.monthly_income * (1 - st.session_state.goal_percent / 100)

        # Scale avg spending proportions to fit into budget
        main_df["Recommended Spend ($)"] = main_df["Avg Spent ($)"] / total_spent * allowed_spend

        st.write(f"Based on your goal of saving **{st.session_state.goal_percent}%**, "
                 f"you should spend max **${allowed_spend:.2f}** per month.")

        st.dataframe(main_df[["Store", "Avg Spent ($)", "Recommended Spend ($)"]], use_container_width=True)
        st.bar_chart(main_df.set_index("Store")[["Avg Spent ($)", "Recommended Spend ($)"]])



# --- FUTURE PREDICTIONS ---
elif page == "🔮 Future Predictions":
    st.title("🔮 Future Predicted Spendings")

    df = pd.read_csv("store_frequency_avg_amt.csv")  # <-- you'd generate this from your long vertical concat
    st.dataframe(df, use_container_width=True)

    st.line_chart(df.set_index("Month")["Total Spent ($)"])
