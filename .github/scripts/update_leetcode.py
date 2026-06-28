import requests, re, os

username = os.environ.get("LEETCODE_USERNAME", "nyxVici")

# LeetCode GraphQL API
query = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    profile { ranking }
    submitStats {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
"""

res = requests.post(
    "https://leetcode.com/graphql",
    json={"query": query, "variables": {"username": username}},
    headers={"Content-Type": "application/json", "Referer": "https://leetcode.com"},
    timeout=10
)

data  = res.json()["data"]["matchedUser"]
stats = {s["difficulty"]: s["count"] for s in data["submitStats"]["acSubmissionNum"]}
rank  = data["profile"]["ranking"]

easy   = stats.get("Easy",   0)
medium = stats.get("Medium", 0)
hard   = stats.get("Hard",   0)
total  = stats.get("All",    0)

block = f"""<!-- LEETCODE-STATS:START -->
| 🟢 Easy | 🟡 Medium | 🔴 Hard | 📊 Total | 🏆 Rank |
|:-------:|:---------:|:-------:|:--------:|:-------:|
| {easy}  |  {medium} |  {hard} |  {total} | #{rank} |
<!-- LEETCODE-STATS:END -->"""

readme = open("README.md").read()
readme = re.sub(
    r"<!-- LEETCODE-STATS:START -->.*?<!-- LEETCODE-STATS:END -->",
    block, readme, flags=re.DOTALL
)
open("README.md", "w").write(readme)
print(f"Done — {total} solved, Rank #{rank}")
