# 🔍 GitHub User Search

A Python script that searches GitHub for user profiles based on names provided in a `names.txt` file. It outputs the results in a pretty terminal table, as well as `.txt` and `.csv` files for further use.

---

## 📦 Features

- 🔎 Searches GitHub using the [GitHub Search API](https://docs.github.com/en/rest/search/users)
- 📋 Supports full name queries (`first last`)
- 📊 Outputs results in:
  - A table in your terminal
  - `results.txt` (pipe-separated)
  - `results.csv`
- 🧠 Skips empty lines and handles basic rate limiting

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/gray-area/GH_User_Search.git
cd GH_User_Search
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Add Your GitHub Token
Create a GitHub personal access token (no scopes needed) and either:

Save it as an environment variable:

```bash
export GITHUB_TOKEN=your_token_here
```
Or edit the script and replace:

```python
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or "your_token_here"
```
### 4. Add Your Name List
Create a names.txt file in the same directory. Format: one First Last per line.

```nginx
John Doe
Jane Smith
Elon Musk
```
### 5. Run It!
```bash
python ghusers.py
```
## 🖼️ Example Output
```text
+-------------+-------------+----------------+----------------------------+
| Query       | Full Name   | Username       | Profile URL                |
+-------------+-------------+----------------+----------------------------+
| Elon Musk   | Elon Reeve  | elonmusk       | https://github.com/elonmusk|
+-------------+-------------+----------------+----------------------------+
```
### Files generated:  

* results.txt  

* results.csv

<br/><br/>

## 💡 Future Enhancements
🌍 Add filters like location: to narrow down users geographically

📦 Display number of public repositories and followers

🧠 Add fuzzy matching (e.g. “Jon” → “John”)

🖼️ Download avatar images and generate visual reports

📥 Export results to JSON or SQLite

🌐 HTML report generation with clickable profile cards

🔁 Pagination to get more than 30 results per name

🔐 Token input from a .env file using python-dotenv
<br/><br/>

## 🛠️ Built With Python

* GitHub REST API v3  

* Tabulate  

* Requests

## 📄 License
MIT © gray-area






