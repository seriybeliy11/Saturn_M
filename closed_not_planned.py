import requests
import pandas as pd
import plotly.graph_objects as go
from plate import *

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

    params_labels = {
        "state": "closed",
        "labels": "footstep,approved",
        "per_page": 100,
        "page": 1
    }

    response_labels = requests.get(url_closed, headers=headers, params=params_labels)
    if response_labels.status_code == 200:
        labeled_issues = response_labels.json()
        footstep_approved_issues = len(labeled_issues)

        data = {
            "Status": ["Closed with 'footstep' and 'approved' label", "All Closed Issues"],
            "Count": [footstep_approved_issues, all_closed_issues]
        }
        df = pd.DataFrame(data)
        fig = go.Figure(data=go.Pie(labels=df["Status"], values=df["Count"]))
        fig.update_layout(title="Ratio of closed issues labeled 'footstep' and 'approved' to all closed issues")

        fig.show()

    else:
        print("Failed to retrieve closed issues with labels:", response_labels.status_code)

else:
    print("Failed to retrieve closed issues:", response_closed.status_code)
