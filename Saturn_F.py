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
from Saturn_M import *

def dst_get_contributors(start_date, end_date):
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"since": start_date.isoformat(), "until": end_date.isoformat()}

        response = requests.get(url, headers=headers, params=params)
        contributors = response.json()

        frame_div = []
        for contributor in contributors:
            frame_div.append(contributor['total'])

        commits_average = sum(frame_div) / len(frame_div)

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


def dst_get_issues(start_date, end_date):
    url = f"https://api.github.com/repos/ton-society/{repo}/issues"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"per_page": 30, "state": "all", "since": start_date, "until": end_date}

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

    return {
        'Number issues': len(issues_container),
        'Number closed issues': len(closed_issues),
        'Number open issues': len(open_issues)
    }


def dst_get_pulls(start_date, end_date):
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
        created_at = datetime.strptime(pull['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        if start_date <= created_at <= end_date:
            if pull["state"] == "open":
                open_pulls.append(pull)
            elif pull["state"] == "closed":
                closed_pulls.append(pull)

    return {
        'Number of pulls': len(closed_pulls) + len(open_pulls),
        'Number of open pulls': len(open_pulls),
        'Number of closed pulls': len(closed_pulls)
    }


def dst_average_time_issue():
    url = f"https://api.github.com/repos/ton-society/{repo}/issues"
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
                created_time = datetime.fromisoformat(issue["created_at"].replace('Z', '+00:00')).timestamp()
                closed_time = datetime.fromisoformat(issue["closed_at"].replace('Z', '+00:00')).timestamp()
                delta_times.append(closed_time - created_time)
                all_issues.append(issue)
        params["page"] = params.get("page", 1) + 1

    average_time = statistics.mean(delta_times) // 86400
    print(f"Average solving time: {average_time} days")


def dst_plot_contributors(start_date, end_date):
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)
        contributors = response.json()

        filtered_contributors = []
        for contributor in contributors:
            if start_date <= contributor['week'] <= end_date:
                filtered_contributors.append(contributor)

        commits = [contributor['total'] for contributor in filtered_contributors]

        fig = go.Figure(
            data=[go.Bar(x=[contributor['author']['login'] for contributor in filtered_contributors], y=commits)],
            layout_title_text="Total Commits by Contributor"
        )

        fig.show()
    except:
        print("Something wrong...Try later")

def dst_plot_issues(start_date, end_date):
    try:
        url = f"https://api.github.com/repos/ton-society/{repo}/issues"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"state": "all", "since": start_date, "until": end_date}

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


        open_issues = []
        closed_issues = []

        for issue in getting_issues:
            if issue["state"] == "open":
                open_issues.append(issue)
            elif issue["state"] == "closed":
                closed_issues.append(issue)

        fig = go.Figure(
            data=[go.Pie(labels=["Open Issues", "Closed Issues"], values=[len(open_issues), len(closed_issues)])],
            layout_title_text=f"Open vs. Closed Issues ({start_date} to {end_date})"
        )

        fig.show()
    except:
        print("Something wrong...Try later")

def dst_plot_pulls(start_date, end_date):
    try:
        url = f"https://api.github.com/repos/ton-society/{repo}/pulls"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"state": "all", "since": start_date, "until": end_date}

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
        fig = go.Figure(
            data=[go.Pie(labels=["Open Pull Requests", "Closed Pull Requests"], values=[len(open_pulls), len(closed_pulls)])],
            layout_title_text=f"Open vs. Closed Pull Requests ({start_date} to {end_date})"
        )

        fig.show()
    except:
        print("Something wrong...Try later")

def complex_dst_plot_pulls(start_date, end_date):
    url = "https://api.github.com/repos/ton-society/ton-footsteps/pulls"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"state": "all", "per_page": 100, "since": start_date, "until": end_date}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    authors = set()
    status_counts = {}
    for item in data:
        authors.add(item["user"]["login"])
        status = item["state"]
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = 1

    pulls_by_author = {}
    for author in authors:
        count = sum(1 for item in data if item["user"]["login"] == author)
        pulls_by_author[author] = count

    layout1 = go.Layout(title=f"Number of pull requests by author ({start_date} to {end_date})", xaxis_title="Author", yaxis_title="Number")
    fig1 = go.Figure(data=[go.Bar(x=list(pulls_by_author.keys()), y=list(pulls_by_author.values()))], layout=layout1)

    labels = list(status_counts.keys())
    values = list(status_counts.values())
    layout2 = go.Layout(title=f"Stats pull requests ({start_date} to {end_date})")
    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)], layout=layout2)

    df = pd.DataFrame.from_dict(pulls_by_author, orient="index", columns=["number"])
    df["author"] = df.index
    counts = df.groupby("author").sum().reset_index()
    x = counts["author"].tolist()
    y = counts["number"].tolist()
    layout3 = go.Layout(title=f"Number of pull requests made by each user ({start_date} to {end_date})", xaxis_title="User", yaxis_title="Number")
    fig3 = go.Figure(data=[go.Bar(x=x, y=y)], layout=layout3)

    fig1.show()
    fig2.show()
    fig3.show()

def complex_dst_plot_issues(start_date, end_date):
    url = "https://api.github.com/repos/ton-society/ton-footsteps/issues"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"state": "all", "per_page": 100, "since": start_date, "until": end_date}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    authors = set()
    status_counts = {}
    for item in data:
        authors.add(item["user"]["login"])
        status = item["state"]
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = 1

    issues_by_author = {}
    for author in authors:
        count = sum(1 for item in data if item["user"]["login"] == author)
        issues_by_author[author] = count

    layout1 = go.Layout(title=f"Number of issues by author ({start_date} to {end_date})", xaxis_title="Author", yaxis_title="Number")
    fig1 = go.Figure(data=[go.Bar(x=list(issues_by_author.keys()), y=list(issues_by_author.values()))], layout=layout1)

    labels = list(status_counts.keys())
    values = list(status_counts.values())
    layout2 = go.Layout(title=f"Stats issues ({start_date} to {end_date})")
    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)], layout=layout2)

    df = pd.DataFrame.from_dict(issues_by_author, orient="index", columns=["number"])
    df["author"] = df.index
    counts = df.groupby("author").sum().reset_index()
    x = counts["author"].tolist()
    y = counts["number"].tolist()
    layout3 = go.Layout(title=f"Number of issues made by each user ({start_date} to {end_date})", xaxis_title="User", yaxis_title="Number")
    fig3 = go.Figure(data=[go.Bar(x=x, y=y)], layout=layout3)

    fig1.show()
    fig2.show()
    fig3.show()

def complex_dst_plot_contributors(start_date, end_date):
    url = "https://api.github.com/repos/ton-society/ton-footsteps/stats/contributors"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"since": start_date, "until": end_date}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    contributors = set()
    commits_by_contributor = {}
    additions_by_contributor = {}
    deletions_by_contributor = {}
    for item in data:
        for contributor in item["author"]:
            contributors.add(contributor["login"])
            if contributor["login"] in commits_by_contributor:
                commits_by_contributor[contributor["login"]] += contributor["total"]
                additions_by_contributor[contributor["login"]] += contributor["weeks"][-1]["a"]
                deletions_by_contributor[contributor["login"]] += contributor["weeks"][-1]["d"]
            else:
                commits_by_contributor[contributor["login"]] = contributor["total"]
                additions_by_contributor[contributor["login"]] = contributor["weeks"][-1]["a"]
                deletions_by_contributor[contributor["login"]] = contributor["weeks"][-1]["d"]

    layout1 = go.Layout(title=f"Number of commits by contributor ({start_date} to {end_date})", xaxis_title="Contributor", yaxis_title="Number")
    fig1 = go.Figure(data=[go.Bar(x=list(commits_by_contributor.keys()), y=list(commits_by_contributor.values()))], layout=layout1)

    layout2 = go.Layout(title=f"Additions vs deletions by contributor ({start_date} to {end_date})", xaxis_title="Contributor", yaxis_title="Number")
    fig2 = go.Figure(data=[
        go.Bar(name='Additions', x=list(additions_by_contributor.keys()), y=list(additions_by_contributor.values())),
        go.Bar(name='Deletions', x=list(deletions_by_contributor.keys()), y=list(deletions_by_contributor.values()))
    ], layout=layout2)
    fig2.update_layout(barmode='stack')

    layout3 = go.Layout(title=f"Number of contributors ({start_date} to {end_date})")
    fig3 = go.Figure(data=[go.Pie(labels=['Contributors', 'Non-contributors'], values=[len(contributors), 1e6-len(contributors)])], layout=layout3)

    fig1.show()
    fig2.show()
    fig3.show()
