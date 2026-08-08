import json
import os
import urllib.request
import urllib.error
from datetime import date, timedelta


USERNAME = "ahujamonica"
TOKEN = os.environ["GITHUB_TOKEN"]


QUERY = """
query($username: String!) {
  user(login: $username) {

    repositories(
      first: 100
      ownerAffiliations: OWNER
      privacy: PUBLIC
    ) {
      totalCount
      nodes {
        stargazerCount
      }
    }

   contributionsCollection {
    totalCommitContributions
    totalIssueContributions
    totalPullRequestContributions

      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""


def github_graphql(query, variables):
    payload = json.dumps({
        "query": query,
        "variables": variables
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "github-stats-generator"
        },
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    if "errors" in result:
        raise RuntimeError(result["errors"])

    return result["data"]["user"]


def calculate_streaks(days):
    contribution_days = {
        day["date"]: day["contributionCount"]
        for day in days
    }

    today = date.today()

    # -----------------------------
    # Current Streak
    # -----------------------------

    current_streak = 0
    current_day = today

    # If there was no contribution today,
    # start checking from yesterday.
    if contribution_days.get(str(current_day), 0) == 0:
        current_day -= timedelta(days=1)

    while contribution_days.get(str(current_day), 0) > 0:
        current_streak += 1
        current_day -= timedelta(days=1)

    # -----------------------------
    # Longest Streak
    # -----------------------------

    longest_streak = 0
    running_streak = 0

    sorted_days = sorted(contribution_days.keys())

    previous_day = None

    for day_string in sorted_days:
        current = date.fromisoformat(day_string)

        if contribution_days[day_string] > 0:
            if (
                previous_day is not None
                and current == previous_day + timedelta(days=1)
            ):
                running_streak += 1
            else:
                running_streak = 1

            longest_streak = max(
                longest_streak,
                running_streak
            )
        else:
            running_streak = 0

        previous_day = current

    return current_streak, longest_streak


def main():

    user = github_graphql(
        QUERY,
        {"username": USERNAME}
    )

    repositories = user["repositories"]

    contributions = user["contributionsCollection"]

    days = []

    for week in contributions["contributionCalendar"]["weeks"]:
        days.extend(
            week["contributionDays"]
        )

    current_streak, longest_streak = calculate_streaks(days)

    total_stars = sum(
        repo["stargazerCount"]
        for repo in repositories["nodes"]
    )

    stats = {
        "username": USERNAME,

        "repositories": repositories["totalCount"],

        "stars": total_stars,

        "total_contributions":
            contributions["totalContributions"],

        "commits":
            contributions["totalCommitContributions"],

        "issues":
            contributions["totalIssueContributions"],

        "pull_requests":
            contributions["totalPullRequestContributions"],

        "current_streak":
            current_streak,

        "longest_streak":
            longest_streak,

        "updated":
            str(date.today())
    }

    os.makedirs("assets", exist_ok=True)

    with open(
        "assets/github-stats.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            stats,
            file,
            indent=2
        )

    print("GitHub statistics generated successfully.")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
