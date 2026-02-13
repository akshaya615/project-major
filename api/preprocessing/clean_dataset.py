import pandas as pd

# Load dataset
df = pd.read_csv("accident.csv")

print("\nBefore Cleaning:")
print(df.isnull().sum())

# Fix Speed_Limit missing values
df['Speed_Limit'] = df['Speed_Limit'].fillna(df['Speed_Limit'].median())

# Convert Date column
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Convert Time column
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')

# Convert Time to only time (HH:MM:SS)
df['Time'] = df['Time'].dt.time

# Convert Injuries to int
df['Number_of_Injuries'] = pd.to_numeric(df['Number_of_Injuries'], errors='coerce').fillna(0).astype(int)

# Extract features
df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.hour
df['Month'] = df['Date'].dt.month
df['DayOfWeek'] = df['Date'].dt.dayofweek

print("\nAfter Cleaning:")
print(df.head())
print(df.info())

df.to_csv("cleaned_accident.csv", index=False)
print("\nCleaned dataset saved as cleaned_accident.csv")
