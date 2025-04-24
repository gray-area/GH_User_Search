import requests
from tabulate import tabulate
import csv
import time
import os
from datetime import datetime

# Load GitHub token (from environment or direct fallback)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or "your_token_here"

INPUT_FILE = "names.txt"
TXT_OUTPUT = "results.txt"
CSV_OUTPUT = "results.csv"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "GitHubUserSearchScript"
}

def search_github_users(query):
    url = f"https://api.github.com/search/users?q={'+'.join(query.split())}+in:fullname"

    while True:
        response = requests.get(url, headers=HEADERS)

        # Handle rate limiting
        if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
            remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
            reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
            current_time = int(time.time())

            if remaining == 0:
                wait_time = reset_time - current_time
                reset_str = datetime.utcfromtimestamp(reset_time).strftime('%Y-%m-%d %H:%M:%S')
                print(f"⏳ Rate limit hit! Sleeping for {wait_time} seconds (until {reset_str} UTC)...")
                time.sleep(wait_time + 1)
                continue  # retry after sleeping

        elif response.status_code != 200:
            print(f"❌ Error {response.status_code} for query '{query}': {response.json().get('message')}")
            return []

        break  # exit loop if everything is okay

    items = response.json().get("items", [])
    results = []

    for item in items:
        username = item["login"]
        profile_url = item["html_url"]
        results.append((query, "", username, profile_url))  # Full name not available here

    return results

def main():
    all_results = []

    with open(INPUT_FILE, "r") as f:
        names = [line.strip() for line in f if line.strip()]

    for name in names:
        print(f"🔎 Searching GitHub for: {name}")
        results = search_github_users(name)
        all_results.extend(results)
        time.sleep(1)  # Politeness delay

    if not all_results:
        print("⚠️ No users found.")
        return

    # Print results as table
    print("\n📋 Results:\n")
    print(tabulate(all_results, headers=["Query", "Full Name", "Username", "Profile URL"], tablefmt="grid"))

    # Save to TXT
    with open(TXT_OUTPUT, "w") as f:
        for r in all_results:
            f.write(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}\n")

    # Save to CSV
    with open(CSV_OUTPUT, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Query", "Full Name", "Username", "Profile URL"])
        writer.writerows(all_results)

    print(f"\n✅ Results saved to `{TXT_OUTPUT}` and `{CSV_OUTPUT}`")

if __name__ == "__main__":
    main()
