import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

# Page Config
st.set_page_config(page_title="Construction Dashboard", layout="wide")

# Title
st.title("🏗 AI Construction Intelligence Dashboard")

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
    ["All"] + list(df["PROJECT_NAME"])
)

# -------------------- ➕ ADD PROJECT --------------------
st.sidebar.header("➕ Add New Project")

proj_id = st.sidebar.text_input("Project ID")
proj_name = st.sidebar.text_input("Project Name")

planned = st.sidebar.number_input("Planned Days", min_value=0, step=1, format="%d", key="p1")
actual = st.sidebar.number_input("Actual Days", min_value=0, step=1, format="%d", key="p2")

budget = st.sidebar.number_input("Budget", min_value=0, step=1000, format="%d", key="p3")
actual_cost = st.sidebar.number_input("Actual Cost", min_value=0, step=1000, format="%d", key="p4")

if st.sidebar.button("Add Project"):
    delay = actual - planned
    cost_overrun = actual_cost - budget

    new_row = pd.DataFrame({
        "PROJECT_ID": [proj_id],
        "PROJECT_NAME": [proj_name],
        "PLANNED_DAYS": [planned],
        "ACTUAL_DAYS": [actual],
        "BUDGET": [budget],
        "ACTUAL_COST": [actual_cost],
        "DELAY": [delay],
        "COST_OVERRUN": [cost_overrun]
    })

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("projects.csv", index=False)

    st.sidebar.success("✅ Project Added!")

# -------------------- 🤖 PREDICTION --------------------
st.sidebar.header("🤖 Predict Delay")

planned_days = st.sidebar.number_input("Planned Days", min_value=0, step=1, format="%d", value=200)
budget_pred = st.sidebar.number_input("Budget", min_value=0, step=1000, format="%d", value=300000)

if st.sidebar.button("Predict"):
    prediction = model.predict([[planned_days, budget_pred]])
    st.sidebar.success(f"Predicted Delay: {round(prediction[0], 2)} days")

# -------------------- KPI SECTION --------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("📊 Total Projects", len(df))
col2.metric("⏱ Delayed Projects", len(df[df["DELAY"] > 0]))
col3.metric("📈 Avg Delay", round(df["DELAY"].mean(), 2))
col4.metric("💰 Total Overrun", df["COST_OVERRUN"].sum())

st.markdown("---")

# -------------------- CHARTS --------------------
st.subheader("📊 Performance Overview")

col5, col6 = st.columns(2)

with col5:
    fig1 = px.bar(df, x="PROJECT_NAME", y="DELAY", color="DELAY",
                  title="Project Delays")
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    fig2 = px.bar(df, x="PROJECT_NAME", y="COST_OVERRUN", color="COST_OVERRUN",
                  title="Cost Overrun")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col7, col8 = st.columns(2)

with col7:
    df["STATUS"] = df["DELAY"].apply(lambda x: "Delayed" if x > 0 else "On-Time")
    fig3 = px.pie(df, names="STATUS", title="Project Status")
    st.plotly_chart(fig3, use_container_width=True)

with col8:
    fig4 = px.bar(df, x="PROJECT_NAME",
                  y=["PLANNED_DAYS", "ACTUAL_DAYS"],
                  barmode="group",
                  title="Planned vs Actual Days")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# -------------------- FULL TABLE --------------------
st.subheader("📊 All Projects")
st.dataframe(df, use_container_width=True, hide_index=True)

# -------------------- SELECTED PROJECT --------------------
if selected_project != "All":
    selected = df[df["PROJECT_NAME"] == selected_project]

    st.subheader(f"📌 Details for: {selected_project}")
    st.dataframe(selected, use_container_width=True, hide_index=True)

    # Status
    if selected["DELAY"].values[0] > 0:
        st.warning("⏱ Project is Delayed")
    else:
        st.success("⏱ Project is On Time")

    if selected["COST_OVERRUN"].values[0] > 0:
        st.error("💰 Project has Loss")
    else:
        st.success("💰 Project is Profitable")

# -------------------- DOWNLOAD --------------------
st.download_button(
    "📥 Download Data",
    df.to_csv(index=False),
    "projects.csv",
    "text/csv"
)