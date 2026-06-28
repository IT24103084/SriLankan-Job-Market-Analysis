from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

db_path = BASE_DIR / "database" / "jobs.db"

conn = sqlite3.connect(db_path)

print("Connected successfully!")

query = """
SELECT region,
COUNT(*) AS total_jobs
FROM jobs
GROUP BY region
ORDER BY total_jobs DESC;
"""

result = pd.read_sql(query, conn)

print(result)