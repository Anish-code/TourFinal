import pandas as pd

# Read the CSV file
df = pd.read_csv('tourdata.csv')

# Convert 'total_review' column to numeric, coerce errors to NaN
df['total_review'] = pd.to_numeric(df['total_review'], errors='coerce')

# Drop rows with NaN values in 'total_review' column
df.dropna(subset=['total_review'], inplace=True)

# Save the modified DataFrame to a new CSV file
df.to_csv('tour_output_file.csv', index=False)

print("Conversion complete. New CSV file saved successfully.")
