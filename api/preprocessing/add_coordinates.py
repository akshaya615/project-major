import pandas as pd

df = pd.read_csv("processed_accident.csv")

# State → Coordinates
state_coords = {
    "Andhra Pradesh": (15.9, 79.7),
    "Karnataka": (15.3, 75.7),
    "Delhi": (28.7, 77.1),
    "Maharashtra": (19.7, 75.7),
    "Uttar Pradesh": (26.8, 80.9)
}

df["Latitude"] = df["State"].map(lambda x: state_coords.get(x, (0,0))[0])
df["Longitude"] = df["State"].map(lambda x: state_coords.get(x, (0,0))[1])

df.to_csv("processed_accident_with_coords.csv", index=False)
print("Coordinates added → processed_accident_with_coords.csv")
