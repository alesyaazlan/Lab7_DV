import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(
    page_title="Titanic Data Explorer",
    layout="wide"
)

# Apply pastel theme via CSS
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
st.write("Interactive dashboard that explores survival patterns from the Titanic dataset.")

# Load Dataset
@st.cache_data
def load_titanic():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    # Handle missing Age values
    df['Age'] = df['Age'].fillna(df['Age'].median())
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

# Filter by Age
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_filter = st.sidebar.slider(
    "Select Age Range",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# Filter by Fare
min_fare, max_fare = int(df['Fare'].min()), int(df['Fare'].max())
fare_filter = st.sidebar.slider(
    "Select Fare Range",
    min_value=min_fare,
    max_value=max_fare,
    value=(min_fare, max_fare)
)

# Filter by Embarked
embarked_filter = st.sidebar.multiselect(
    "Select Embarked Port",
    options=df['Embarked'].dropna().unique(),
    default=[]
)

# Filter by Survival Status
survival_filter = st.sidebar.multiselect(
    "Select Survival Status",
    options=[0, 1],
    format_func=lambda x: "Survived" if x==1 else "Did Not Survive",
    default=[]
)

# Apply Filters
filtered_df = df.copy()

if len(gender_filter) > 0:
    filtered_df = filtered_df[filtered_df["Sex"].isin(gender_filter)]
if len(pclass_filter) > 0:
    filtered_df = filtered_df[filtered_df["Pclass"].isin(pclass_filter)]

# Age filter
filtered_df = filtered_df[(filtered_df['Age'] >= age_filter[0]) & (filtered_df['Age'] <= age_filter[1])]

# Fare filter
filtered_df = filtered_df[(filtered_df['Fare'] >= fare_filter[0]) & (filtered_df['Fare'] <= fare_filter[1])]

# Embarked filter
if len(embarked_filter) > 0:
    filtered_df = filtered_df[filtered_df['Embarked'].isin(embarked_filter)]

# Survival filter
if len(survival_filter) > 0:
    filtered_df = filtered_df[filtered_df['Survived'].isin(survival_filter)]


# Metric Summary
st.subheader("Dataset Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Total Passengers (Filtered)", len(filtered_df))
col2.metric("Survived", filtered_df["Survived"].sum())
col3.metric("Did Not Survive", len(filtered_df) - filtered_df["Survived"].sum())

st.markdown("---")

# Visualization 1: Survival Count by Gender
st.subheader("Survival Count by Gender")

fig_bar = px.bar(
    filtered_df,
    x="Sex",
    y="Survived",
    color="Sex",
    color_discrete_map={"male": "#FFC4C4", "female": "#EE6983"},  # consistent pastel mapping
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
    color_discrete_map={1: "#EE6983", 0: "#850E35"},  # survived / not survived
    title="Age Distribution by Survival Status",
    nbins=30
)
fig_hist.update_layout(plot_bgcolor="#FCF5EE", paper_bgcolor="#FCF5EE", font_color="#850E35")
st.plotly_chart(fig_hist, use_container_width=True)

# Visualization 3: Survival Rate by Passenger Class
st.subheader("Survival Rate by Passenger Class")

# Calculate survival rate
survival_rate = filtered_df.groupby('Pclass')['Survived'].mean().reset_index()

# Convert Pclass to string so Plotly applies colors correctly
survival_rate['Pclass'] = survival_rate['Pclass'].astype(str)

fig_rate = px.bar(
    survival_rate,
    x='Pclass',
    y='Survived',
    color='Pclass',
    color_discrete_map={"1": "#FFC4C4", "2": "#EE6983", "3": "#850E35"},  # pastel colors
    title="Survival Rate by Passenger Class",
    text=survival_rate['Survived'].apply(lambda x: f"{x:.1%}"),
    category_orders={"Pclass": ["1", "2", "3"]}
)
fig_rate.update_layout(plot_bgcolor="#FCF5EE", paper_bgcolor="#FCF5EE", font_color="#850E35")
st.plotly_chart(fig_rate, use_container_width=True)


# Show Raw Data
st.markdown("---")
if st.checkbox("Show Raw Filtered Data"):
    st.dataframe(filtered_df, use_container_width=True)

# Missing Values Summary
st.subheader("Missing Values Summary")
st.dataframe(df.isnull().sum())
