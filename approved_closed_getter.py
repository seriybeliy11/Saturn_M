import pandas as pd
import requests
from plate import access_token

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

url_closed = "https://api.github.com/repos/ton-society/ton-footsteps/issues"

data = []
for date in date_list:
    page = 1
    per_page = 100
    closed_approved_issues = 0

    while True:
        params_date = {
            "state": "closed",
            "labels": "approved",
            "per_page": per_page,
            "page": page,
            "since": pd.to_datetime(date),
            "until": pd.to_datetime(date) + pd.DateOffset(months=2)  # Получение данных за 3 месяца
        }

        response_date = requests.get(url_closed, headers=headers, params=params_date)

        if response_date.status_code == 200:
            issues = response_date.json()
            num_issues = len(issues)
            closed_approved_issues += num_issues
            page += 1

            if num_issues < per_page:
                break  # достигнут конец списка проблем

        else:
            print(f"Failed to fetch data for {date}")
            break

    data.append([date, closed_approved_issues])

# Создание DataFrame из полученных данных
df = pd.DataFrame(data, columns=["Date", "Closed Approved Issues"])

# Сохранение DataFrame в CSV файл
df.to_csv("github_closed_approved_issues.csv", index=False)
