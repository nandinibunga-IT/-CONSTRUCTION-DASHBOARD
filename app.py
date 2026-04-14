import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

# Page Config
st.set_page_config(page_title="Construction Dashboard", layout="wide")

# Custom Background
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("🏗 Construction Project Analytics Dashboard")

# Load Data
df = pd.read_csv("projects.csv")

# -------------------- 🤖 AI MODEL --------------------
X = df[["PLANNED_DAYS", "BUDGET"]]
y = df["DELAY"]

model = LinearRegression()
model.fit(X, y)

# -------------------- SIDEBAR --------------------
st.sidebar.header("🔍 Filters")

selected_project = st.sidebar.selectbox(
    "Select Project",
    df["PROJECT_NAME"]
)

# AI Prediction Section
st.sidebar.header("🤖 Predict Delay")

planned_days = st.sidebar.number_input("Planned Days", value=200)
budget = st.sidebar.number_input("Budget", value=300000)

if st.sidebar.button("Predict"):
    prediction = model.predict([[planned_days, budget]])
    st.sidebar.success(f"Predicted Delay: {round(prediction[0], 2)} days")

# Filter Data
filtered_df = df[df["PROJECT_NAME"] == selected_project]

# -------------------- KPI SECTION --------------------
total_projects = len(df)
delayed_projects = len(df[df["DELAY"] > 0])
avg_delay = round(df["DELAY"].mean(), 2)
total_overrun = df["COST_OVERRUN"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("📊 Total Projects", total_projects)
col2.metric("⏱ Delayed Projects", delayed_projects)
col3.metric("📈 Avg Delay", avg_delay)
col4.metric("💰 Total Overrun", total_overrun)

st.markdown("---")

# -------------------- CHARTS --------------------
st.subheader("📊 Performance Overview")

col5, col6 = st.columns(2)

with col5:
    fig1 = px.bar(df,
                  x="PROJECT_NAME",
                  y="DELAY",
                  title="Project Delays",
                  color="DELAY")
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    fig2 = px.bar(df,
                  x="PROJECT_NAME",
                  y="COST_OVERRUN",
                  title="Cost Overrun",
                  color="COST_OVERRUN")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col7, col8 = st.columns(2)

with col7:
    df["STATUS"] = df["DELAY"].apply(lambda x: "Delayed" if x > 0 else "On-Time")
    fig3 = px.pie(df,
                  names="STATUS",
                  title="Project Status")
    st.plotly_chart(fig3, use_container_width=True)

with col8:
    fig4 = px.bar(df,
                  x="PROJECT_NAME",
                  y=["PLANNED_DAYS", "ACTUAL_DAYS"],
                  barmode="group",
                  title="Planned vs Actual Days")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# -------------------- FILTERED DATA --------------------
st.subheader(f"📄 Details for: {selected_project}")
st.write(filtered_df)

# -------------------- DOWNLOAD BUTTON --------------------
st.download_button(
    "📥 Download Data",
    df.to_csv(index=False),
    "projects.csv",
    "text/csv"
)