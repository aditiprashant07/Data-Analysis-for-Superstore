# Data Cleaning is done here

import kagglehub
import os
import pandas as pd

# Define the dataset identifier
dataset_id = "rohitsahoo/sales-forecasting"

print(f"Attempting to download dataset: {dataset_id}")
# Download the dataset
download_path = kagglehub.dataset_download(dataset_id)

# Check if download was successful
if os.path.exists(download_path):
    print(f"Download successful! Dataset saved at: {download_path}")
    # Find the first CSV file in the downloaded folder
    csv_file = None
    for file in os.listdir(download_path):
        if file.endswith(".csv"):
            csv_file = os.path.join(download_path, file)
            break
    if csv_file:
        df = pd.read_csv(csv_file)

        # Fill missing values for each column
        for col in df.columns:
            if df[col].dtype == 'O':  # Object type (categorical)
                mode_val = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
                df[col] = df[col].fillna(mode_val)
            else:  # Numeric type
                mean_val = df[col].mean()
                df[col] = df[col].fillna(mean_val)

        # Special handling for 'postal code' if present
        if 'postal code' in df.columns:
            df['postal code'] = df['postal code'].fillna(9800).astype(int)

        if df.duplicated().any():
            print("Duplicates present")
        else:
            print("No duplicates!")

        # Save cleaned data to a new CSV file
        cleaned_csv = os.path.join(download_path, "cleaned_data.csv")
        df.to_csv(cleaned_csv, index=False)
        print(f"Cleaned data saved to: {cleaned_csv}")

        print(df.head())
        print(df.columns)
        print(df.info())
    else:
        print("No CSV file found in the downloaded dataset folder.")
else:
    print("Download failed.")