import pandas as pd
import numpy as np
from datetime import datetime

def data_analysis(df):

    # Ensure "Start Time" and "End Time" are in datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%H:%M:%S')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%H:%M:%S')

    # Calculate the difference in hours
    df['Duration'] = (df['End Time'] - df['Start Time']).dt.total_seconds() / 3600

    df['Start'] = df['Start Time'].dt.strftime('%I:%M %p')
    df['End'] = df['End Time'].dt.strftime('%I:%M %p')

    #Calculate Price per Hour
    df['Weekly Fee Float'] = df['Weekly Fee'].replace('[\$,]', '', regex=True).astype(float)
    df['Price per Hour'] = df['Weekly Fee Float']/df['Duration']
    df['Price per Hour'] = df['Price per Hour'].round(2)

    #Number of Weeks
    # Convert "Start of Period" and "End of Period" to datetime
    # Define the current year to assume for date parsing
    current_year = datetime.now().year
    df['Start of Period Date'] = pd.to_datetime(df["Start of Period"] + f"-{current_year}", format="%d-%b-%Y")
    df['End of Period Date'] = pd.to_datetime(df["End of Period"] + f"-{current_year}", format="%d-%b-%Y")

    # Calculate the number of weeks between the dates
    df['Total Weeks'] = ((df["End of Period Date"] - df["Start of Period Date"]).dt.days / 7).astype(int).abs()

    #Calculate Total Number of Hours
    df['Total Hours'] = df['Total Weeks']*df['Duration']

    #Calculate Total Cost
    df['Total Cost'] = df['Weekly Fee Float']*df["Total Weeks"]

    #Calculate Price per Area
    # Clean the price columns
    df["5x5 Booth"] = (
        df["5x5 Booth"]
        .str.replace("$", "", regex=False)  # Remove the dollar sign
        .replace("Not an Option", np.nan)  # Replace "Not an Option" with NaN
        .astype(float)  # Convert to float
    )

    df["10x10 Booth"] = (
        df["10x10 Booth"]
        .str.replace("$", "", regex=False)  # Remove the dollar sign
        .replace("Not an Option", np.nan)  # Replace "Not an Option" with NaN
        .astype(float)  # Convert to float
    )

    # Calculate the area for each booth type
    df["5x5 Area"] = 5 * 5  # Area of a 5x5 booth
    df["10x10 Area"] = 10 * 10  # Area of a 10x10 booth

    # Calculate price per square foot, handling NaN values
    df["5x5 Price per SqFt"] = df["5x5 Booth"] / df["5x5 Area"]
    df["10x10 Price per SqFt"] = df["10x10 Booth"] / df["10x10 Area"]

    return df