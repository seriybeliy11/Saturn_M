import requests
import pandas as pd
from plate import access_token

headers = {
    "Authorization": access_token,
    "Accept": "application/vnd.github.v3+json"
}

url_closed = "https://api.github.com/repos/ton-society/ton-footsteps/issues"

dates = [
    '2022-06-13T09:39:52Z',
    '2022-08-13T09:39:52Z',
    '2022-10-13T09:39:52Z',
    '2022-12-13T09:39:52Z',
    '2023-02-01T00:00:00Z',
    '2023-04-01T00:00:00Z',
    '2023-06-01T00:00:00Z'
]

data = []
for date in dates:
    params_closed = {
        "state": "closed",
        "per_page": 100,
        "page": 1,
        "since": date,
        "until": date
    }

    response_closed = requests.get(url_closed, headers=headers, params=params_closed)

    if response_closed.status_code == 200:
        closed_issues = response_closed.json()
        all_closed_issues = len(closed_issues)

        params_approved = {
            "state": "closed",
            "labels": "approved",
            "per_page": 100,
            "page": 1,
            "since": date,
            "until": date
        }

        response_approved = requests.get(url_closed, headers=headers, params=params_approved)
        if response_approved.status_code == 200:
            approved_issues = response_approved.json()
            closed_approved_issues = len(approved_issues)

            data.append({"Date": date, "Closed Approved Issues": closed_approved_issues, "Closed Issues": all_closed_issues})

        else:
            print("Failed to retrieve closed approved issues for date", date, ":", response_approved.status_code)

    else:
        print("Failed to retrieve closed issues for date", date, ":", response_closed.status_code)

df = pd.DataFrame(data)
df.to_csv("dates_data.csv", index=False)
