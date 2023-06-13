import requests
import pandas as pd
from plate import access_token
import time

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
session = requests.Session()
session.headers.update(headers)

for date in dates:
    params_closed = {
        "state": "closed",
        "per_page": 100,
        "page": 1,
        "since": date,
        "until": date
    }

    try:
        response_closed = session.get(url_closed, params=params_closed)
        response_closed.raise_for_status()

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

        time.sleep(4)  # Задержка в 4 секунды между запросами

        try:
            response_approved = session.get(url_closed, params=params_approved)
            response_approved.raise_for_status()

            approved_issues = response_approved.json()
            closed_approved_issues = len(approved_issues)

            data.append({"Date": date, "Closed Approved Issues": closed_approved_issues, "Closed Issues": all_closed_issues})

        except requests.exceptions.RequestException as e:
            print("Failed to retrieve closed approved issues for date", date, ":", e)

    except requests.exceptions.RequestException as e:
        print("Failed to retrieve closed issues for date", date, ":", e)

df = pd.DataFrame(data)
df.to_csv("dates_data.csv", index=False)
