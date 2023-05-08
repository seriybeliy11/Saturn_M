import requests
import json
from plate import repo
from plate import access_token
from plate import owner
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import statistics
import pandas as pd
import plotly.graph_objs as go
from openpyxl import Workbook
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import time


def get_contributors():
    try:
        url = f"https://api.github.com/repos/ton-society/ton-footsteps/stats/contributors"
        headers = {"Authorization": f"Bearer {access_token}"}


        response = requests.get(url, headers=headers)
        contributors = response.json()
        #print(contributors)
        #for contributor in contributors:
            #print("Contributor:")
            #print(f"\tID: {contributor['author']['id']}")
            #print(f"\tLogin: {contributor['author']['login']}")
            #print(f"\tTotal commits: {contributor['total']}")
            #print("Weeks:")
        #for week in contributor['weeks']:
            #print(f"\tStart of week: {week['w']}")
            #print(f"\tNumber of additions: {week['a']}")
            #print(f"\tNumber of deletions: {week['d']}")
            #print(f"\tNumber of commits: {week['c']}")
            #print(f"\tEnd of week: {week['w'] + 604800}") # 604800 seconds = 1 week

        frame_div = []
        for contributor in contributors:
            #print(f"\tTotal commits: {contributor['total']}")
            frame_div.append(contributor['total'])

        #print(frame_div)
        commits_average = sum(frame_div) / len(frame_div)
        #print(commits_average)

        list_high_average = []
        for contributor in contributors:
            if contributor['total'] > commits_average:
                list_high_average.append(contributor['author']['login'])

        all_commits = sum(frame_div)
        print('Number of regular contributors to TON Footsteps -', len(list_high_average))
        num_active_contributors = sum(1 for c in contributors if c["total"] > 0)
        print('Number of active contributors to TON Footsteps initiatives -',num_active_contributors)
        print('Number of contributions made by community members -', all_commits)
    except:
        print('Something Wrong...Try later')

def get_issues():
    try:
        url = f"https://api.github.com/repos/ton-society/{repo}/issues"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"per_page": 30, "state": "all"}

        getting_issues = []
        page_number = 1
        while True:
            params["page"] = page_number
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                break

            page_issues = response.json()
            if not page_issues:
                break

            getting_issues.extend(page_issues)
            page_number += 1

        issues_container = []
        for issue in getting_issues:
            issues_container.append(issue['number'])

        open_issues = []
        closed_issues = []

        for issue in getting_issues:
            if issue["state"] == "open":
                open_issues.append(issue)
            elif issue["state"] == "closed":
                closed_issues.append(issue)

        print('Open -', len(open_issues))
        print('Closed -', len(closed_issues))
        print('All -', len(issues_container))
    except:
        print('Something wrong')


def get_pulls():
    url = f"https://api.github.com/repos/ton-society/{repo}/pulls"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"per_page": 30, "state": "all"}

    getting_pulls = []
    page_number = 1
    while True:
        params["page"] = page_number
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            break

        page_pulls = response.json()
        if not page_pulls:
            break

        getting_pulls.extend(page_pulls)
        page_number += 1

    open_pulls = []
    closed_pulls = []

    for pull in getting_pulls:
        if pull["state"] == "open":
            open_pulls.append(pull)
        elif pull["state"] == "closed":
            closed_pulls.append(pull)

    print('Number of pulls:', len(closed_pulls) + len(open_pulls))


def average_time_issue():
    url = "https://api.github.com/repos/ton-society/ton-footsteps/issues"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"state": "all", "per_page": 100}

    all_issues = []
    delta_times = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break
        issues = response.json()
        if not issues:
            break
        for issue in issues:
            if issue.get("closed_at"):
                created_time = datetime.strptime(issue["created_at"], '%Y-%m-%dT%H:%M:%SZ').timestamp()
                closed_time = datetime.strptime(issue["closed_at"], '%Y-%m-%dT%H:%M:%SZ').timestamp()
                delta_times.append(closed_time - created_time)
                all_issues.append(issue)
        params["page"] = params.get("page", 1) + 1


    average_time = statistics.mean(delta_times) // 86400
    print(f"Average solving time: {average_time} days")


def plot_contributors():
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)
        contributors = response.json()
        commits = [contributor['total'] for contributor in contributors]

        fig = go.Figure(
            data=[go.Bar(x=[contributor['author']['login'] for contributor in contributors], y=commits)],
            layout_title_text="Total Commits by Contributor"
        )

        fig.show()
        fig.write_image('plotting_contributors.png')
    except:
        print("Something wrong...Try later")

def get_AVG():
    try:
        org = 'ton-society'
        repo = 'ton-footsteps'


        url = f'https://api.github.com/repos/{org}/{repo}/community/profile'
        headers = {'Authorization': f'token {access_token}'}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            avg = data['health_percentage']

            print(f'AVG for {org}/{repo}: {avg}')
        else:
            print(f'Request failed with status code {response.status_code}')
    except:
        print('Something wrong...')

def get_KPI_pulls():
    try:
        owner = 'ton-society'
        repo = 'ton-footsteps'

        response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/issues?state=open')
        open_issues = response.json()
        open_issues_count = len(open_issues)

        response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/issues?state=closed&since=30d')
        closed_issues = response.json()
        closed_issues_count = len(closed_issues)

        response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/pulls?state=open')
        open_pulls = response.json()
        open_pulls_count = len(open_pulls)

        response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&since=30d')
        closed_pulls = response.json()
        closed_pulls_count = len(closed_pulls)

        issues_kpi = closed_issues_count / (open_issues_count + closed_issues_count)
        pulls_kpi = closed_pulls_count / (open_pulls_count + closed_pulls_count)

        print(f'KPI для pulls: {pulls_kpi}')
    except:
        print('Something wrong...')

def get_KPI_contribute():
    try:
        owner = 'delovoyhomie'
        repo = 'ton-footsteps'

        response = requests.get(f'https://api.github.com/repos/{owner}/{repo}')
        repo_info = response.json()
        commit_count = repo_info['size']

        print(f"KPI for the whole period of time: {commit_count}")
    except:
        print('Something wrong...')

def export_CSV_contribute():
    try:
        params = {'per_page': 100, 'page': 1}
        contributors = []

        while True:
            response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contributors', params=params)
            contributors += response.json()
            if 'next' not in response.links:
                break
            params = {'per_page': 100, 'page': params['page']+1}

        df = pd.json_normalize(contributors)
        df.to_csv('data_conributors.csv', index=False)
    except:
        print('...')

def issues():
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

    df = pd.DataFrame(all_issues, columns=['state', 'labels', 'labels_url'])
    df.to_csv('issues.csv', index=False)




def get_commenters():
    try:
        url = 'https://api.github.com/repos/ton-society/ton-footsteps/issues/comments'
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            comments = response.json()
            commenters = set()
            for comment in comments:
                commenters.add(comment['user']['login'])
            num_commenters = len(commenters)
            print('Number of commenters:', num_commenters)
        else:
            print('Failed to retrieve comments:', response.status_code)

    except:
        print('Something wrong...')

def get_time_ad():
    try:
        url = f"https://api.github.com/repos/ton-society/ton-footsteps/issues"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"per_page": 30, "state": "all"}
        issues = []

        while True:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                issues += response.json()
                if 'next' in response.links.keys():
                    url = response.links['next']['url']
                else:
                    break
            else:
                print(f'Failed to retrieve issues: {response.status_code}')
                break

        for issue in issues:
            created_at = datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            if issue['closed_at']:
                closed_at = datetime.strptime(issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
                time_to_close = closed_at - created_at
                print(f"Issue #{issue['number']} opened at {created_at} and closed at {closed_at}. Time to close: {time_to_close}")
            else:
                print(f"Issue #{issue['number']} opened at {created_at} and is still open.")
            time.sleep(0.5)


    except:
        print('Something wrong...')

def issues_sorted():
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
        params["page"] = params.get("page", 1) + 1

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

def contributors():
    owner = 'ton-society'
    repo = 'ton-footsteps'
    url = f'https://api.github.com/repos/{owner}/{repo}/stats/contributors'

    response = requests.get(url)
    contributors = response.json()

    with open('contributors.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'date', 'additions', 'deletions', 'commits'])
        for contributor in contributors:
            for week in contributor['weeks']:
                if pd.isna(week['a']) or pd.isna(week['d']) or pd.isna(week['c']):
                    continue
                date = datetime.fromtimestamp(week['w']).strftime('%Y-%m-%d')
                writer.writerow([contributor['author']['login'], date, week['a'], week['d'], week['c']])


def issues_data():
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

def data_contributors():
    import requests
    import pandas as pd

    url = 'https://api.github.com/repos/ton-society/ton-footsteps/contributors'
    response = requests.get(url)

    data = response.json()

    df = pd.DataFrame(data, columns=['login', 'id', 'node_id', 'avatar_url', 'gravatar_id', 'url', 'html_url', 'followers_url', 'following_url', 'gists_url', 'starred_url', 'subscriptions_url', 'organizations_url', 'repos_url', 'events_url', 'received_events_url', 'type', 'site_admin', 'contributions'])
    df.to_csv('data_contributors.csv', index=False)

def data_issues():

    # Создаем заголовок с токеном для авторизации в GitHub API
    headers = {'Authorization': f'Token {access_token}'}

    # Получаем issues постранично
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

    # Создаем список для хранения данных
    issues_data = []

    # Извлекаем данные для каждой проблемы
    for issue in all_issues:
        issue_data = [issue['state'], issue['title'], issue['body'], issue['created_at'], issue['updated_at']]
        issues_data.append(issue_data)

    # Создаем DataFrame из полученных данных
    df = pd.DataFrame(issues_data, columns=['state', 'title', 'body', 'created_at', 'updated_at'])

    # Экспортируем DataFrame в CSV-файл
    df.to_csv('data_issues.csv', index=False)
