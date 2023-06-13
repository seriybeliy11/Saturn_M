import requests
import csv
from plate import access_token
import time

def get_commentators(issue_url, headers):
    response = requests.get(issue_url + "/comments", headers=headers)
    if response.status_code == 200:
        comments = response.json()
        commentators = set()
        for comment in comments:
            commentators.add(comment["user"]["login"])
        return commentators
    else:
        return None

repo_url = "https://api.github.com/repos/ton-society/ton-footsteps"
issues_endpoint = "/issues"
token = access_token

headers = {
    "Authorization": f"Bearer {token}"
}

per_page = 100
params = {
    "per_page": per_page
}

data = []
page = 1

while True:
    params["page"] = page
    response = requests.get(repo_url + issues_endpoint, headers=headers, params=params)
    time.sleep(5)

    if response.status_code == 200:
        issues = response.json()
        if len(issues) == 0:
            break

        for issue in issues:
            issue_number = issue["number"]
            issue_url = issue["url"]

            while True:
                commentators = get_commentators(issue_url, headers)
                if commentators is not None:
                    break

            num_commentators = len(commentators)
            data.append([issue_number, num_commentators])

        page += 1

    else:
        print("Failed to retrieve issues", response.status_code)
        break

with open("commentators.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Number issue", "Uniq Com"])
    writer.writerows(data)
