import requests
import re
import csv
import os
import plotly.graph_objects as go

csv_file_path = 'rewards.csv'
if os.path.exists(csv_file_path):
    print("Created yet. Good ! ")
else:
    api_url = 'https://api.github.com/repos/ton-society/ton-footsteps/issues'
    params = {
        'state': 'all',
        'per_page': 100
    }

    page_numbers = []
    has_next_page = True
    page = 1

    while has_next_page:
        params['page'] = page
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            issues = response.json()

            page_numbers.extend([issue['number'] for issue in issues])
            has_next_page = 'Link' in response.headers and 'rel="next"' in response.headers['Link']
            page += 1

        else:
            print(f"Error code: {response.status_code}")
            break

    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(['Number for issue', 'Rewards (th. $)'])

        base_url = 'https://github.com/ton-society/ton-footsteps/issues/'

        for page_number in page_numbers:
            url = base_url + str(page_number)
            response = requests.get(url)
            html_content = response.content
            text = html_content.decode('utf-8')

            regex_dollar = r'\$[\d,]+'
            rewards_dollar = re.findall(regex_dollar, text)

            for reward_dollar in rewards_dollar:
                reward_amount = reward_dollar.replace('$', '').replace(',', '')
                if reward_amount == '1':
                    reward_amount += '000'

                writer.writerow([page_number, reward_amount])

    print("Data Loaded")

issue_numbers = []
rewards = []
with open(csv_file_path, mode='r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    for row in reader:
        issue_numbers.append(row[0])
        rewards.append(float(row[1]) / 1000)

fig = go.Figure(data=[go.Bar(x=issue_numbers, y=rewards)])

fig.update_layout(
    xaxis_title="Number for issue",
    yaxis_title="Rewards (th. $)",
    title="Rewards Gramm"
)

fig.show()
