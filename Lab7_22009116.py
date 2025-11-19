import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(
    page_title="Titanic Data Explorer",
    page_icon="🚢",
    layout="wide"
)

# Apply pastel theme via markdown
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #FCF5EE;  /* main soft cream background */
        color: #850E35;  /* dark accent for text */
    }}
    .stMetric label {{
        color: #850E35;  /* metric text color */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Titanic Survivor Dashboard")
st.write("Interactive dashboard that explores the survival patterns from the Titanic dataset.")

# Load Dataset
@st.cache_data
def load_titanic():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    return df

df = load_titanic()

# Sidebar Filters
st.sidebar.header("Filter Options")

# Filter by Gender
gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=df["Sex"].unique(),
    default=[]
)

# Filter by Passenger Class
pclass_filter = st.sidebar.multiselect(
    "Select Passenger Class (Pclass)",
    options=sorted(df["Pclass"].unique()),
    default=[]
)

# Apply filters
filtered_df = df.copy()
if len(gender_filter) > 0:
    filtered_df = filtered_df[filtered_df["Sex"].isin(gender_filter)]
if len(pclass_filter) > 0:
    filtered_df = filtered_df[filtered_df["Pclass"].isin(pclass_filter)]

# Summary
st.subheader("Dataset Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Total Passengers (Filtered)", len(filtered_df))
col2.metric("Survived", filtered_df["Survived"].sum())
col3.metric("Did Not Survive", len(filtered_df) - filtered_df["Survived"].sum())

st.markdown("---")

# Visualization 1: Survival Count
st.subheader("Survival Count by Gender")

fig_bar = px.bar(
    filtered_df,
    x="Sex",
    y="Survived",
    color="Sex",
    color_discrete_sequence=["#FFC4C4", "#EE6983"],  # light & medium pink
    title="Number of Survivors by Gender",
    barmode="group"
)
fig_bar.update_layout(plot_bgcolor="#FCF5EE", paper_bgcolor="#FCF5EE", font_color="#850E35")
st.plotly_chart(fig_bar, use_container_width=True)

# Visualization 2: Age Distribution Histogram
st.subheader("Age Distribution of Passengers")

fig_hist = px.histogram(
    filtered_df,
    x="Age",
    color="Survived",
    color_discrete_sequence=["#EE6983", "#850E35"],  # medium pink & dark accent
    title="Age Distribution by Survival Status",
    nbins=30
)
fig_hist.update_layout(plot_bgcolor="#FCF5EE", paper_bgcolor="#FCF5EE", font_color="#850E35")
st.plotly_chart(fig_hist, use_container_width=True)

# Raw Data Table
st.markdown("---")
if st.checkbox("Show Raw Filtered Data"):
    st.dataframe(filtered_df, use_container_width=True)
