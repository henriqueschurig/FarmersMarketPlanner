import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime, timedelta

from data_loader import load_data
from map_renderer import create_map
from data_analyzer import data_analysis
from calendar_viewer import view_calendar, build_calendar

#Locate and Load Data
file_path = 'Database.csv'
df = load_data(file_path)

#Manipulate Data
df = data_analysis(df)

# Streamlit page configuration
st.set_page_config(page_title="Event Locations", layout="wide")

# Sidebar filters with an expander
st.sidebar.header("Filters")

# Day of the Week Filter
with st.sidebar.expander("Day of the Week"):
    unique_days = df["Day of the Week"].unique()
    selected_days = st.multiselect(
        "Select Day of the Week",
        options=unique_days,
        default=unique_days,
    )

# Total Duration Filter (Slider)
with st.sidebar.expander("Duration"):
    min_duration = float(df["Duration"].min())
    max_duration = float(df["Duration"].max())
    selected_duration_range = st.slider(
        "Select Duration Range",
        min_value=min_duration,
        max_value=max_duration,
        value=(min_duration, max_duration),
        step=0.25,
    )

# County Filter
with st.sidebar.expander("County"):
    unique_counties = df["County"].unique()
    selected_counties = st.multiselect(
        "Select County",
        options=unique_counties,
        default=unique_counties,
    )

# Weekly Fee Filter
with st.sidebar.expander("Weekly Fee"):
    min_fee, max_fee = st.slider(
        "Select Weekly Fee Range",
        min_value=float(df["Weekly Fee Float"].min()),
        max_value=float(df["Weekly Fee Float"].max()),
        value=(float(df["Weekly Fee Float"].min()), float(df["Weekly Fee Float"].max())),
    )

# Applying all Filters
filtered_df = df[
    (df["Day of the Week"].isin(selected_days)) &
    (df["County"].isin(selected_counties)) &
    (df["Duration"].between(*selected_duration_range)) &
    (df["Weekly Fee Float"].between(min_fee, max_fee))
]

# Page Setup
st.logo("FarmersJam.png")
st.image("Banner.png")

st.divider()

st.header("1. Event Scounting")

col1, col2 = st.columns([0.6, 0.3])

with col1:

    market_names = filtered_df["Name"].unique().tolist()  # List of unique market names
    selected_markets = st.multiselect("Choose the farmers markets to display", market_names, default=market_names)

    # Filter the DataFrame based on the selected markets
    filtered_df = filtered_df[filtered_df["Name"].isin(selected_markets)]

    # Checkbox for column selection
    columns_to_display = ["Name", "Location", "Day of the Week", "County", "Start", "End", "Duration", "Weekly Fee", "Total Weeks", "Total Cost", "Description", "Price per Hour", "Vendor Application Link", "Source", "5x5 Booth", "10x10 Booth", "5x5 Price per SqFt", "10x10 Price per SqFt"]
    selected_columns = st.multiselect("Select columns to display", columns_to_display, default=["Name", "Location"])

    # Display the DataFrame based on selected columns and markets
    if selected_columns:
        st.write(filtered_df[selected_columns])
    else:
        st.write("Please select at least one column to display.")

with col2:
    #Initial Description
    st.write("This map shows the locations of various Farmers' Markets.")
    st.write("Hover over each marker for more information.")

    #Slider for adjusting circle radius
    radius = st.slider("Select Circle Radius", min_value=100, max_value=2000, value=500, step=200)

    #Render Map
    initial_view_state = pdk.ViewState(latitude=33.7490, longitude=-84.3880, zoom=10, pitch=0)
    map_deck = create_map(filtered_df, radius, initial_view_state)
    st.pydeck_chart(map_deck)

st.subheader("2. Event Calendar")

filtered_calendar_df = build_calendar(df)
st.dataframe(view_calendar(filtered_calendar_df), use_container_width=True)

# Display cost information
st.subheader("3. Summary & Cost Breakdown")
cost_info = filtered_calendar_df[["Name", "Day of the Week", "Start Time", "End Time", "Total Weeks", "Weekly Fee", "Total Cost"]]
st.dataframe(cost_info, use_container_width=True)
total_cost = filtered_calendar_df["Total Cost"].sum()
total_hours = filtered_calendar_df["Total Hours"].sum()
num = len(cost_info)
avg_fm_cost = filtered_calendar_df["Total Cost"].mean()
try:
    avg_hour_cost = total_cost/total_hours
except ZeroDivisionError:
    avg_hour_cost = 0
if total_cost != 0:
    st.write(f"The Total Cost is \${total_cost:,.2f} for {num} Farmers' Market. Each Farmers' Market costs on average \${avg_fm_cost:,.2f}. Each Hour costs on average \${avg_hour_cost:,.2f}")
else:
    st.write("The Total Cost is $0")

for _, row in filtered_calendar_df.iterrows():
    st.write(
        f"- **{row['Name']}** on **{row['Day of the Week']}** from "
        f"**{row['Start']} to {row['End']}**: "
        f"Duration: {row['Total Weeks']} weeks, "
        f"Weekly Fee: \${row['Weekly Fee Float']}, "
        f"Total Cost: \${row['Total Cost']}."
    )
