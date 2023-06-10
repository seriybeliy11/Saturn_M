from SaturiC import data_issues
from SaturiC import data_contributors
from SaturiC import contributors
from SaturiC import issues_sorted
from plate import *
import requests
from datetime import *
import csv
import pandas as pd
import time

def main():
    url = "https://api.github.com/repos/ton-society/ton-footsteps/issues"
    params = {"state": "all", "per_page": 100}
    issues = []

    while True:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            break

        page_issues = response.json()
        if not page_issues:
            break

        issues.extend(page_issues)
        if "next" in response.links:
            url = response.links["next"]["url"]
        else:
            break

    numbers = [issue["number"] for issue in issues]

    durations = []
    for issue in issues:
        created_at = datetime.fromisoformat(issue["created_at"][:-1])
        if issue["closed_at"] is not None:
            closed_at = datetime.fromisoformat(issue["closed_at"][:-1])
            duration = (closed_at - created_at).days
        else:
            duration = None
        durations.append(duration)

    with open("issue_numbers_and_durations.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["number", "duration"])
        writer.writerows(zip(numbers, durations))
    df = pd.read_csv("issue_numbers_and_durations.csv")
    df_sorted = df.sort_values("duration", ascending=False)
    df_sorted.to_csv("issues_sorted.csv", index=False)
#################################################################################
    owner = 'ton-society'
    repo = 'ton-footsteps'
    url = f'https://api.github.com/repos/{owner}/{repo}/stats/contributors'

    while True:
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status()
            contributors = response.json()

        if not contributors:
            print("No contributors found for the specified repository. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
            continue

        with open('contributors.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['name', 'date', 'additions', 'deletions', 'commits'])
            for contributor in contributors:
                for week in contributor['weeks']:
                    if pd.isna(week['a']) or pd.isna(week['d']) or pd.isna(week['c']):
                        continue
                    date = datetime.fromtimestamp(week['w']).strftime('%Y-%m-%d')
                    writer.writerow([contributor['author']['login'], date, week['a'], week['d'], week['c']])

        df = pd.read_csv('contributors.csv').dropna(subset=['date'])
        df.to_csv('contributors.csv', index=False)
        break  # Exit the loop if data is successfully retrieved

    print("Contributors data successfully retrieved.")





    ############################################################################
    all_issues = []

    page = 1
    while True:
        url = f'https://api.github.com/repos/ton-society/ton-footsteps/issues?page={page}&per_page=100'
        response = requests.get(url)
        issues = response.json()

        if not issues:
            break

        all_issues.extend(issues)
        page += 1

    issues_data = []

    for issue in all_issues:
        issue_state = issue['state']
        issue_labels = issue.get('labels', [])
        issue_labels = ",".join([label['name'] for label in issue_labels])
        issues_data.append([issue_state, issue_labels])

    df = pd.DataFrame(issues_data, columns=['state', 'labels'])

    df.to_csv('issues_data.csv', index=False)
    ############################################################################
    url = 'https://api.github.com/repos/ton-society/ton-footsteps/contributors'
    response = requests.get(url)

    data = response.json()

    df = pd.DataFrame(data, columns=['login', 'id', 'node_id', 'avatar_url', 'gravatar_id', 'url', 'html_url', 'followers_url', 'following_url', 'gists_url', 'starred_url', 'subscriptions_url', 'organizations_url', 'repos_url', 'events_url', 'received_events_url', 'type', 'site_admin', 'contributions'])
    df.to_csv('data_contributors.csv', index=False)
    ############################################################################


    
    headers = {'Authorization': f'Token {access_token}'}

    
    all_issues = []
    page = 1
    while True:
        url = f'https://api.github.com/repos/ton-society/ton-footsteps/issues?page={page}&per_page=100&state=all'
        response = requests.get(url, headers=headers)
        issues = response.json()
        if not issues:
            break
        all_issues.extend(issues)
        page += 1


    issues_data = []

    for issue in all_issues:
        issue_data = [issue['state'], issue['title'], issue['body'], issue['created_at'], issue['updated_at']]
        issues_data.append(issue_data)

   
    df = pd.DataFrame(issues_data, columns=['state', 'title', 'body', 'created_at', 'updated_at'])

   
    df.to_csv('data_issues.csv', index=False)

if __name__ == "__main__":
    main()
