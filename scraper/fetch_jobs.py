import requests
from bs4 import BeautifulSoup

url = "https://www.topjobs.lk/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find all links
links = soup.find_all("a")

print(f"Total links found: {len(links)}")

for i, link in enumerate(links[:50], start=1):
    print(f"\nLink {i}")
    print("Text :", link.get_text(strip=True))
    print("URL  :", link.get("href"))