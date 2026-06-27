import pandas as pd
import requests
import json
import time
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = BASE_DIR / "data" / "raw" / "jobs_raw.csv"

df = pd.read_csv(csv_path)

headers = {
    "User-Agent": "Mozilla/5.0"
}


def extract_job(url):

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Find elements that contain "Please refer"

        for tag in soup.find_all():
          text = tag.get_text(" ", strip=True)

          if "Please refer" in text:
             print("\n====================")
             print("Tag:", tag.name)
             print(tag.prettify()[:4000])

        json_script = soup.find("script", type="application/ld+json")

        if not json_script:
            return None

        job = json.loads(json_script.string)

        location = job["jobLocation"][0]["address"]

        job_title = job.get("title", "")

        if "Data" in job_title:
            category = "Data"

        elif "Software" in job_title:
            category = "Software"

        elif "Manager" in job_title:
            category = "Management"

        elif "Executive" in job_title:
            category = "Executive"

        elif "Engineer" in job_title:
            category = "Engineering"

        else:
            category = "Other"

        return {
    "title": job_title,
    "company": job["hiringOrganization"]["name"],
    "posted_date": job.get("datePosted"),
    "closing_date": job.get("validThrough"),
    "city": location.get("addressLocality"),
    "region": location.get("addressRegion"),
    "category": category,
    "url": url
}

    except Exception as e:
        print(e)
        return None
    
jobs = []

for i, url in enumerate(df["URL"]):     # First 20 jobs

    print(f"{i+1}/{len(df)}")

    job = extract_job(url)

    if job:
        jobs.append(job)

    time.sleep(1)

jobs_df = pd.DataFrame(jobs)

print(jobs_df.head())

output = BASE_DIR / "data" / "processed"

output.mkdir(parents=True, exist_ok=True)

jobs_df.to_csv(output / "jobs_detailed.csv", index=False)

print("Saved successfully!")  

