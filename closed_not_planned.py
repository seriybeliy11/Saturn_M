import requests
import pandas as pd
import plotly.graph_objects as go
from plate import access_token

headers = {
    "Authorization": access_token,
    "Accept": "application/vnd.github.v3+json"
}

url_closed = "https://api.github.com/repos/ton-society/ton-footsteps/issues"

params_closed = {
    "state": "closed",
    "per_page": 100,
    "page": 1
}

response_closed = requests.get(url_closed, headers=headers, params=params_closed)

if response_closed.status_code == 200:
    closed_issues = response_closed.json()
    all_closed_issues = len(closed_issues)

    params_approved = {
        "state": "closed",
        "labels": "approved",
        "per_page": 100,
        "page": 1
    }

    response_approved = requests.get(url_closed, headers=headers, params=params_approved)
    if response_approved.status_code == 200:
        approved_issues = response_approved.json()
        closed_approved_issues = len(approved_issues)

        data = {
            "Status": ["Closed Approved Issues", "Closed Issues"],
            "Count": [closed_approved_issues, all_closed_issues]
        }
        df = pd.DataFrame(data)
        fig = go.Figure(data=go.Pie(labels=df["Status"], values=df["Count"]))
        fig.update_layout(title="Ratio of Closed Approved Issues to Closed Issues")

        fig.show()

    else:
        print("Failed to retrieve closed approved issues: " + str(response_approved.status_code))

else:
    print("Failed to retrieve closed issues: " + str(response_closed.status_code))
