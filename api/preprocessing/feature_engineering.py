import pandas as pd

# Load cleaned dataset
df = pd.read_csv("cleaned_accident.csv")

# Encode categorical variables
categorical_cols = [
    'State', 'Reason', 'Road_Type', 'Weather_Conditions',
    'Alcohol_Involved', 'Driver_Fatigue', 'Road_Conditions'
]

for col in categorical_cols:
    df[col] = df[col].astype('category').cat.codes

# Create Severity Score
df['Severity_Score'] = df['Number_of_Deaths'] * 2 + df['Number_of_Injuries']

df.to_csv("processed_accident.csv", index=False)
print("Processed dataset saved as processed_accident.csv")
