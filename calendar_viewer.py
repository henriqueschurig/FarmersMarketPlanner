import pandas as pd
import streamlit as st

def build_calendar(df):

    #Create Index for each event
    df["Event ID"] = df.index

    # Event Selection
    selected_events = st.multiselect(
        "Select events to display",
        options=df["Name"].unique()
    )

    # Filtered Dataframe
    filtered_df = df[df["Name"].isin(selected_events)]

    return filtered_df

def view_calendar(df):
    # Pivot the data for better visualization
    calendar_df = (
        df.pivot_table(
            index=["Start", "End", "Event ID"],
            columns="Day of the Week",
            values="Name",
            aggfunc=lambda x: ", ".join(x) if len(x) > 0 else None,
        )
        .reset_index()
    )

    # Drop Event ID from display but keep rows separated
    calendar_df = calendar_df.drop(columns=["Event ID"]).fillna("")

    return calendar_df