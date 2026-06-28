from pathlib import Path
import pandas as pd
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = BASE_DIR / "data" / "cleaned" / "jobs_cleaned.csv"

db_folder = BASE_DIR / "database"
db_folder.mkdir(exist_ok=True)

db_path = db_folder / "jobs.db"

df = pd.read_csv(csv_path)

conn = sqlite3.connect(db_path)

df.to_sql(
    "jobs",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Database created successfully!")