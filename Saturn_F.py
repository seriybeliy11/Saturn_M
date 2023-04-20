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

def dst_get_contributors():
    try:
        start_year = int(input("Enter the start year (e.g. 2022): "))
        start_month = int(input("Enter the start month (e.g. 1 for January): "))
        start_day = int(input("Enter the start day (e.g. 1): "))
        end_year = int(input("Enter the end year (e.g. 2022): "))
        end_month = int(input("Enter the end month (e.g. 12 for December): "))
        end_day = int(input("Enter the end day (e.g. 31): "))

        start_date = datetime.date(start_year, start_month, start_day)
        end_date = datetime.date(end_year, end_month, end_day)

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


def dst_get_issues():
    try:
        start_year = int(input("Enter the start year (e.g. 2022): "))
        start_month = int(input("Enter the start month (e.g. 1 for January): "))
        start_day = int(input("Enter the start day (e.g. 1): "))
        end_year = int(input("Enter the end year (e.g. 2022): "))
        end_month = int(input("Enter the end month (e.g. 12 for December): "))
        end_day = int(input("Enter the end day (e.g. 31): "))

        start_date = datetime.date(start_year, start_month, start_day)
        end_date = datetime.date(end_year, end_month, end_day)

        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"per_page": 30, "state": "all", "since": start_date.isoformat(), "until": end_date.isoformat()}

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
    except:
        print('Something wrong...')


import datetime

def dst_get_pulls():
    try:
        start_year = int(input("Enter the start year (e.g. 2022): "))
        start_month = int(input("Enter the start month (e.g. 1 for January): "))
        start_day = int(input("Enter the start day (e.g. 1): "))
        end_year = int(input("Enter the end year (e.g. 2022): "))
        end_month = int(input("Enter the end month (e.g. 12 for December): "))
        end_day = int(input("Enter the end day (e.g. 31): "))

        start_date = datetime.datetime(start_year, start_month, start_day)
        end_date = datetime.datetime(end_year, end_month, end_day)

        url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
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
            created_at = datetime.datetime.strptime(pull['created_at'], '%Y-%m-%dT%H:%M:%SZ')
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
    except:
        print('Something went wrong. Please try again later.')



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


def dst_plot_contributors():
    try:
        start_year = int(input("Введите год начала периода (например, 2022): "))
        start_month = int(input("Введите месяц начала периода (например, 1 для января): "))
        start_day = int(input("Введите день начала периода (например, 1): "))
        end_year = int(input("Введите год конца периода (например, 2022): "))
        end_month = int(input("Введите месяц конца периода (например, 12 для декабря): "))
        end_day = int(input("Введите день конца периода (например, 31): "))

        start_date = datetime.date(start_year, start_month, start_day).isoformat()
        end_date = datetime.date(end_year, end_month, end_day).isoformat()

        url = f"https://api.github.com/repos/ton-society/{repo}/stats/contributors"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"since": start_date, "until": end_date}

        response = requests.get(url, headers=headers, params=params)
        contributors = response.json()

        contributor_names = []
        commit_counts = []

        for contributor in contributors:
            contributor_names.append(contributor["author"]["login"])
            commit_counts.append(contributor["total"])

        fig = go.Figure(
            data=[go.Bar(x=contributor_names, y=commit_counts)],
            layout_title_text=f"Contributions ({start_date} to {end_date})"
        )

        fig.show()
    except:
        print("Something wrong...Try later")


def dst_plot_issues():
    try:
        start_year = int(input("Enter the start year (e.g. 2022): "))
        start_month = int(input("Enter the start month (e.g. 1 for January): "))
        start_day = int(input("Enter the start day (e.g. 1): "))
        end_year = int(input("Enter the end year (e.g. 2022): "))
        end_month = int(input("Enter the end month (e.g. 12 for December): "))
        end_day = int(input("Enter the end day (e.g. 31): "))

        start_date = datetime.date(start_year, start_month, start_day).isoformat()
        end_date = datetime.date(end_year, end_month, end_day).isoformat()

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


def dst_plot_pulls():
    try:
        start_date_str = input("Enter start date (YYYY-MM-DD): ")
        end_date_str = input("Enter end date (YYYY-MM-DD): ")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

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
            layout_title_text=f"Open vs. Closed Pull Requests ({start_date_str} to {end_date_str})"
        )

        fig.show()
    except:
        print("Something wrong...Try later")


def complex_dst_plot_pulls():
    try:
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

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
    except:
        print('Something wrong')


def complex_dst_plot_contributors():
    try:
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

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
    except:
        print('Something wrong')
