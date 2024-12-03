import pandas as pd

def load_data(file_path):

    # Load each sheet into a DataFrame
    farmers_market_df = pd.read_csv(file_path)

    # Remove empty rows and columns
    cleaned_df = farmers_market_df.dropna(how='all', axis=0).dropna(how='all', axis=1)

    return cleaned_df

