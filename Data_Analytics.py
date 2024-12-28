import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit app configuration
st.set_page_config(page_title="Interactive Disease Report", layout="wide")

# Title of the app
st.title("Interactive Disease Report Data Visualizations")

# Load the dataset (replace 'data.csv' with your actual file path)
data_path = "grouped_disease_data.csv"
data = pd.read_csv(data_path)

# Display the dataset preview
st.write("Dataset Preview:")
st.dataframe(data.head())

# User input for visualization
entities = data["Entity"].unique().tolist()
diseases = data["Disease"].unique().tolist()

selected_entity = st.selectbox("Select an Entity (Country/Region)", options=entities)
selected_disease = st.selectbox("Select a Disease", options=diseases)

# Filter data based on user selection
filtered_data = data[
    (data["Entity"] == selected_entity) & 
    (data["Disease"] == selected_disease)
]

# Plot the data
if not filtered_data.empty:
    fig = px.line(
        filtered_data,
        x="Year",
        y="Deaths",
        title=f"{selected_disease} Deaths in {selected_entity} Over Time",
        labels={"Deaths": "Number of Deaths", "Year": "Year"},
        color_discrete_sequence=["#00FFFF"]  # Bright cyan for black background
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected entity and disease.")
