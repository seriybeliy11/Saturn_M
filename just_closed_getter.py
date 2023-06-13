import pandas as pd
import requests
import time
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
session = requests.Session()
session.headers.update(headers)

for date in date_list:
    page = 1
    per_page = 100
    closed_issues = 0

    while True:
        params_date = {
            "state": "closed",
            "per_page": per_page,
            "page": page,
            "since": pd.to_datetime(date),
            "until": pd.to_datetime(date) + pd.DateOffset(months=2)  # Получение данных за 3 месяца
        }

        try:
            response_date = session.get(url_closed, params=params_date)
            response_date.raise_for_status()

            issues = response_date.json()
            num_issues = len(issues)
            closed_issues += num_issues
            page += 1

            if num_issues < per_page:
                break  # достигнут конец списка проблем

            time.sleep(1)  # Задержка в 1 секунду между запросами

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data for {date}: {e}")
            break

    data.append([date, closed_issues])

# Создание DataFrame из полученных данных
df = pd.DataFrame(data, columns=["Date", "Closed Issues"])

# Сохранение DataFrame в CSV файл
df.to_csv("github_just_closed_issues.csv", index=False)
