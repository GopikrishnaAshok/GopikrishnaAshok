import json
import os
import re
import urllib.request
from datetime import datetime, timedelta


USERNAME = "GopikrishnaAshok"
OUTPUT_FILE = "data/contributions.json"


def fetch_page():
    url = f"https://github.com/users/{USERNAME}/contributions"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8")


def parse_contributions(html):
    pattern = re.compile(
        r'<td[^>]*data-date="([^"]+)"[^>]*data-level="([^"]+)"'
    )

    matches = pattern.findall(html)

    contributions = []

    for date, level in matches:
        contributions.append({
            "date": date,
            "level": int(level)
        })

    return contributions


def main():
    os.makedirs("data", exist_ok=True)

    html = fetch_page()
    contributions = parse_contributions(html)

    data = {
        "username": USERNAME,
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "contributions": contributions
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    print(
        f"Saved {len(contributions)} contribution entries "
        f"to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
