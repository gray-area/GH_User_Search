import requests
from tabulate import tabulate
import csv
import time
import os

# Replace with your GitHub token (or load from env)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or "your_personal_access_token"

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
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error {response.status_code} for query '{query}': {response.json().get('message')}")
        return []

    items = response.json().get("items", [])
    results = []

    for item in items:
        username = item["login"]
        profile_url = item["html_url"]
        full_name = item.get("name") or ""  # This field isn't always in the user object
        results.append((query, full_name, username, profile_url))

    return results

def main():
    all_results = []

    with open(INPUT_FILE, "r") as f:
        names = [line.strip() for line in f if line.strip()]

    for name in names:
        print(f"Searching GitHub for: {name}")
        results = search_github_users(name)
        all_results.extend(results)
        time.sleep(1)  # Stay under rate limits

    if not all_results:
        print("No users found.")
        return

    # Print to screen
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

    print(f"\nResults saved to {TXT_OUTPUT} and {CSV_OUTPUT}")

if __name__ == "__main__":
    main()
