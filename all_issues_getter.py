import pandas as pd
import requests
from plate import access_token
import time
from dateutil.parser import isoparse

date_list = [
    '2022-06-13T09:39:52Z',
    '2022-08-13T09:39:52Z',
    '2022-10-13T09:39:52Z',
    '2022-12-13T09:39:52Z',
    '2023-02-01T00:00:00Z',
    '2023-04-01T00:00:00Z',
    '2023-06-01T00:00:00Z'
]

headers = {
    "Authorization": access_token,
    "Accept": "application/vnd.github.v3+json"
}

url_issues = "https://api.github.com/repos/ton-society/ton-footsteps/issues"

data = []
for i in range(len(date_list) - 1):
    start_date = isoparse(date_list[i])
    end_date = isoparse(date_list[i + 1])
    page = 1
    issues = []

    while True:
        params_date = {
            "state": "all",
            "per_page": 100,
            "page": page,
            "since": start_date.isoformat(),
            "until": end_date.isoformat()
        }

        response_date = requests.get(url_issues, headers=headers, params=params_date)

        time.sleep(1)

        if response_date.status_code == 200:
            issues_page = response_date.json()
            issues.extend(issues_page)

            if len(issues_page) < 100:
                break
            else:
                page += 1
        else:
            print(f"Failed to fetch data for {start_date} - {end_date}")
            break

    all_issues = len(issues)
    data.append([start_date, all_issues])

# Add the last date from the list separately
last_date = isoparse(date_list[-1])
page = 1
issues = []

while True:
    params_date = {
        "state": "all",
        "per_page": 100,
        "page": page,
        "since": last_date.isoformat()
    }

    response_date = requests.get(url_issues, headers=headers, params=params_date)

    time.sleep(1)

    if response_date.status_code == 200:
        issues_page = response_date.json()
        issues.extend(issues_page)

        if len(issues_page) < 100:
            break
        else:
            page += 1
    else:
        print(f"Failed to fetch data for {last_date}")
        break

all_issues = len(issues)
data.append([last_date, all_issues])

# Create DataFrame from the obtained data
df = pd.DataFrame(data, columns=["Dates", "All Issues"])

# Save DataFrame to a CSV file
df.to_csv("github_all_issues.csv", index=False)
