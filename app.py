import streamlit as st
import seaborn as sns
import pandas as pd
import plotly.express as px

# Load dataset
df = sns.load_dataset("titanic")

# Fill missing values for cleaner visuals
df['age'].fillna(df['age'].median(), inplace=True)
df.dropna(subset=['embarked'], inplace=True)

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔍 Filter Options")

sex_filter = st.sidebar.multiselect("Select Sex", df['sex'].unique(), default=df['sex'].unique())
class_filter = st.sidebar.multiselect("Select Class", df['class'].unique(), default=df['class'].unique())
embark_filter = st.sidebar.multiselect("Select Embarkation Port", df['embarked'].unique(), default=df['embarked'].unique())
age_filter = st.sidebar.slider("Select Age Range", int(df['age'].min()), int(df['age'].max()), (0, 80))

# Apply filters
filtered_df = df[
    (df['sex'].isin(sex_filter)) &
    (df['class'].isin(class_filter)) &
    (df['embarked'].isin(embark_filter)) &
    (df['age'].between(age_filter[0], age_filter[1]))
]

# -------------------------------
# Dashboard Title
# -------------------------------
st.title("🚢 Titanic Survival Interactive Dashboard")

st.markdown("Explore passenger survival based on different factors like sex, class, age, and embarkation port.")

# -------------------------------
# KPIs / Summary Cards
# -------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Passengers", len(filtered_df))
col2.metric("Survival Rate", f"{filtered_df['survived'].mean()*100:.1f}%")
col3.metric("Avg Age", f"{filtered_df['age'].mean():.1f} yrs")

# Safe female %
sex_counts = filtered_df['sex'].value_counts(normalize=True)
female_pct = sex_counts.get('female', 0) * 100
col4.metric("Female %", f"{female_pct:.1f}%")

# -------------------------------
# Visualizations
# -------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🧑 Survival Analysis", "🔎 Passenger Data"])

with tab1:
    st.subheader("Survival by Sex and Class")
    fig1 = px.histogram(filtered_df, x="sex", color="survived", barmode="group",
                        title="Survival by Sex")
    st.plotly_chart(fig1)

    fig2 = px.histogram(filtered_df, x="class", color="survived", barmode="group",
                        title="Survival by Class")
    st.plotly_chart(fig2)

with tab2:
    st.subheader("Age Distribution by Survival")
    fig3 = px.histogram(filtered_df, x="age", color="survived", nbins=30,
                        title="Age Distribution by Survival")
    st.plotly_chart(fig3)

    st.subheader("Embarkation Port Analysis")
    fig4 = px.histogram(filtered_df, x="embarked", color="survived", barmode="group",
                        title="Survival by Embarkation Port")
    st.plotly_chart(fig4)

with tab3:
    st.subheader("Passenger Data Table (Filtered)")
    st.dataframe(filtered_df[['sex','age','class','embarked','survived']])
