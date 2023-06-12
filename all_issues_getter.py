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
for date in date_list:
    parsed_date = isoparse(date)
    page = 1
    issues = []

    while True:
        params_date = {
            "state": "all",
            "per_page": 100,
            "page": page,
            "since": parsed_date.isoformat(),
            "until": parsed_date.isoformat()
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
            print(f"Failed to fetch data for {parsed_date}")
            break

    all_issues = len(issues)
    data.append([parsed_date, all_issues])

# Create a single list combining all the parsed dates
combined_list = [item for sublist in data for item in sublist]

# Create DataFrame from the combined list
df = pd.DataFrame(combined_list, columns=["Dates", "All Issues"])

# Save DataFrame to a CSV file
df.to_csv("github_all_issues_combined.csv", index=False)
