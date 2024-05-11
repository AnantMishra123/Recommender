import pandas as pd

# Load the entire CSV file into a DataFrame
df = pd.read_csv("data/async_movie_db.csv")

# Retrieve the last 5 rows of the DataFrame
last_5_rows = df.tail(5)["id"]

print(last_5_rows)
