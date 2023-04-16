import requests
import json
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import statistics
import pandas as pd
import plotly.graph_objs as go
from openpyxl import Workbook
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import date


def get_contributors():
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
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

    return {
        'Number issues': len(issues_container),
        'Number closed issues': len(closed_issues),
        'Number open issues': len(open_issues)
    }


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

    return {
        'Number of pulls': len(closed_pulls) + len(open_pulls)
    }


def average_time_isseu():
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
    except:
        print("Something wrong...Try later")

def plot_issues():
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

        open_issues = []
        closed_issues = []

        for issue in getting_issues:
            if issue["state"] == "open":
                open_issues.append(issue)
            elif issue["state"] == "closed":
                closed_issues.append(issue)

        fig1 = go.Figure(
            data=[go.Pie(labels=["Open Issues", "Closed Issues"], values=[len(open_issues), len(closed_issues)])],
            layout_title_text="Open vs. Closed Issues"
        )
        fig1.show()

        open_days = [(datetime.datetime.utcnow() - datetime.datetime.fromisoformat(issue['created_at'][:-1])).days for issue in open_issues]
        fig2 = px.histogram(x=open_days, nbins=20, title='Distribution of Days for Open Issues')
        fig2.show()

        close_days = [(datetime.datetime.fromisoformat(issue['closed_at'][:-1]) - datetime.datetime.fromisoformat(issue['created_at'][:-1])).days for issue in closed_issues]
        fig3 = px.histogram(x=close_days, nbins=20, title='Distribution of Days to Close Issues')
        fig3.show()

        open_dates = [issue['created_at'][:-1] for issue in open_issues]
        df1 = pd.DataFrame({'date': open_dates, 'count': [1]*len(open_issues)})
        df1 = df1.groupby('date').sum().reset_index()
        fig4 = px.line(df1, x='date', y='count', title='Open Issues over Time')
        fig4.show()

        close_dates = [issue['closed_at'][:-1] for issue in closed_issues]
        df2 = pd.DataFrame({'date': close_dates, 'count': [1]*len(closed_issues)})
        df2 = df2.groupby('date').sum().reset_index()
        fig5 = px.line(df2, x='date', y='count', title='Closed Issues over Time')
        fig5.show()
    except:
        print('...')


def plot_pulls():
    try:
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

        fig = go.Figure(
            data=[go.Pie(labels=["Open Pull Requests", "Closed Pull Requests"], values=[len(open_pulls), len(closed_pulls)])],
            layout_title_text="Open vs. Closed Pull Requests"
        )

        fig.show()
    except:
        print("Something wrong...Try later")

def issues_x_pulls():
    try:
        issues_count = len(get_issues())
        pulls_count = len(get_pulls())
        fig = go.Figure(data=[go.Bar(x=['Issues'], y=[issues_count], name='Issues', marker_color='#8B008B'),
                              go.Bar(x=['Pull Requests'], y=[pulls_count], name='Pull Requests', marker_color='#A9A9A9')])

        fig.update_layout(title_text='Number of open tasks and merge requests')

        fig.update_xaxes(title_text="Type")
        fig.update_yaxes(title_text="Quantity")

        fig.show()
    except:
        print("Something wrong...Try later")
def viz_contributors():
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)
        contributors = response.json()

        authors = [contributor['author']['login'] for contributor in contributors]

        dates = []
        for contributor in contributors:
            for week in contributor['weeks']:
                if week['w'] not in dates:
                    dates.append(week['w'])

        values = []
        for author in authors:
            author_values = []
            for date in dates:
                total = 0
                for contributor in contributors:
                    if contributor['author']['login'] == author:
                        for week in contributor['weeks']:
                            if week['w'] == date:
                                total += week['a'] + week['d']
                author_values.append(total)
            values.append(author_values)

        traces = []
        for i in range(len(authors)):
            trace = go.Scatter(x=dates, y=values[i], mode='lines', name=authors[i])
            traces.append(trace)
        layout = go.Layout(title=f"Contributors to {owner}/{repo}", xaxis={'title': 'Date'}, yaxis={'title': 'Commits'})
        fig = go.Figure(data=traces, layout=layout)
        fig.show()
    except:
        print("Something wrong...Try later")

def complex_plot_contributors():
        url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            return

        contributors = response.json()

        names = [contributor["author"]["login"] for contributor in contributors]
        total_commits = [contributor["total"] for contributor in contributors]
        total_additions = [sum(week["a"] for week in contributor["weeks"]) for contributor in contributors]
        total_deletions = [sum(week["d"] for week in contributor["weeks"]) for contributor in contributors]
        total_changes = [sum(week["c"] for week in contributor["weeks"]) for contributor in contributors]

        fig = make_subplots(rows=1, cols=3, subplot_titles=("Total Commits", "Total Changes", "Total Additions vs. Deletions"))

        fig.add_trace(
            go.Scatter(
                x=total_commits,
                y=total_changes,
                mode="markers",
                marker=dict(
                    size=total_additions,
                    sizemode='area',
                    sizeref=2.0 * max(total_additions) / (50.0 ** 2),
                    sizemin=4
                ),
                text=names
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=names,
                y=total_commits,
                mode="lines",
                line=dict(color="purple")
            ),
            row=1, col=2
        )

        fig.add_trace(
            go.Histogram2dContour(
                x=total_additions,
                y=total_deletions,
                colorscale="Blues",
                reversescale=True,
                xaxis="x3",
                yaxis="y3"
            ),
            row=1, col=3
        )

        fig.update_layout(
            title_text="Contributors Statistics",
            showlegend=False,
            height=400,
            width=800,
            xaxis=dict(title="Total Commits", showgrid=False, zeroline=False),
            yaxis=dict(title="Total Changes", showgrid=False, zeroline=False),
            xaxis3=dict(title="Total Additions", showgrid=False, zeroline=False, domain=[0.55, 1]),
            yaxis3=dict(title="Total Deletions", showgrid=False, zeroline=False),
            margin=dict(l=50, r=50, t=50, b=50),
        )

        fig.show()

def complex_plot_issues():
    url = "https://api.github.com/repos/ton-society/ton-footsteps/issues"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"state": "all", "per_page": 100}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    counts_opened = {}
    counts_closed = {}
    labels = []
    assignees = {}
    for issue in data:
        date = issue["created_at"][:10]
        if issue["state"] == "open":
            counts_opened[date] = counts_opened.get(date, 0) + 1
        else:
            counts_closed[date] = counts_closed.get(date, 0) + 1

        for label in issue["labels"]:
            labels.append(label["name"])

        if issue["assignee"] is None:
            assignees["Unassigned"] = assignees.get("Unassigned", 0) + 1
        else:
            name = issue["assignee"]["login"]
            assignees[name] = assignees.get(name, 0) + 1

    x = list(counts_opened.keys())
    y1 = list(counts_opened.values())
    y2 = list(counts_closed.values())

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=x, y=y1, mode="lines+markers", name="Opened"))
    fig1.add_trace(go.Scatter(x=x, y=y2, mode="lines+markers", name="Closed"))
    fig1.update_layout(title="Number of Issues Opened and Closed Over Time", xaxis_title="Date", yaxis_title="Number of Issues")

    fig2 = px.histogram(labels, nbins=len(set(labels)), title="Distribution of Issues by Label")
    fig2.update_xaxes(title="Label")
    fig2.update_yaxes(title="Number of Issues")

    fig3 = px.pie(values=list(assignees.values()), names=list(assignees.keys()), title="Percentage of Issues by Assignee")

    fig1.show()
    fig2.show()
    fig3.show()

def complex_plot_pulls():
    url = "https://api.github.com/repos/ton-society/ton-footsteps/pulls"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"state": "all", "per_page": 100}
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

    layout1 = go.Layout(title="Number of pull requests by author", xaxis_title="Author", yaxis_title="Number")
    fig1 = go.Figure(data=[go.Bar(x=list(pulls_by_author.keys()), y=list(pulls_by_author.values()))], layout=layout1)

    labels = list(status_counts.keys())
    values = list(status_counts.values())
    layout2 = go.Layout(title="Stats pull requests")
    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)], layout=layout2)

    df = pd.DataFrame.from_dict(pulls_by_author, orient="index", columns=["number"])
    df["author"] = df.index
    counts = df.groupby("author").sum().reset_index()
    x = counts["author"].tolist()
    y = counts["number"].tolist()
    layout3 = go.Layout(title="Number of pull requests made by each user", xaxis_title="User", yaxis_title="Number")
    fig3 = go.Figure(data=[go.Bar(x=x, y=y)], layout=layout3)

    fig1.show()
    fig2.show()
    fig3.show()
