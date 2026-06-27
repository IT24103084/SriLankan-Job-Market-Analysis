import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://www.topjobs.lk/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Download the webpage
response = requests.get(url, headers=headers)

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find all links
links = soup.find_all("a")

jobs = []

for link in links:

    text = link.get_text(" ", strip=True)
    href = link.get("href")

    if href is None:
        continue

    # Keep only job advertisement links
    if "JobAdvertismentServlet" in href:

        match = re.search(r"'(.*?)'", href)

        if match:
            job_url = "https://www.topjobs.lk/" + match.group(1)

            jobs.append({
                "Job": text,
                "URL": job_url
            })

df = pd.DataFrame(jobs)

print(df.head())

print(f"\nTotal Jobs Found: {len(df)}")

# Save the dataset
df.to_csv("jobs_raw.csv", index=False)

print("CSV saved successfully!")

