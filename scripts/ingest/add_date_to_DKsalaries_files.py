# add week and date to projections and salaries csv files
# data is loaded into one large table in database, and it needs date to distinguish different weeks
import datetime 
import pandas as pd
from glob import glob

files = glob(r"C:\Users\onlyu\OneDrive\Coding_Projects\Fantasy_Football\data\*DKSalaries*.csv")

for file in files:
    print(f"Found file: {file}")

for file_path in files:
    df = pd.read_csv(file_path)
    relative_path = file_path.split("\\")[-1]
    print(f"Processing file: {relative_path}")
    if "date" in df.columns:
        print(f"File with date column: {relative_path}")
    else:
        date = file_path.split("DKSalaries_")[-1].split(".csv")[0]
        #date = datetime.datetime.strptime(date, "%Y_%m_%d").date()
        week = pd.to_datetime(date).week - 36
        print(f"Date: {date}, week: {week}")
        
        df["date"] = date
        df['week'] = week
        
        df = df[["date", "week"] + [c for c in df.columns if c not in ["date", "week"]]]

        file_path = file_path.split(".csv")[0]
        df.to_csv(file_path + "_cleaned.csv", index=False)
        print(f"Cleaned file saved: {file_path + '_cleaned.csv'}")
