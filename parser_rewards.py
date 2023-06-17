import csv
import os
import requests
import re

csv_file_path = 'rewards.csv'

if os.path.exists(csv_file_path):
    print("CSV file already exists. Skipping parsing step.")
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

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Issue Number', 'Rewards (th. $)'])

        base_url = 'https://github.com/ton-society/ton-footsteps/issues/'

        for page_number in page_numbers:
            url = base_url + str(page_number)
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.content
                text = html_content.decode('utf-8')

                regex_dollar = r'Total: \$(\d+)'
                rewards_dollar = re.findall(regex_dollar, text)

                for reward_dollar in rewards_dollar:
                    reward_amount = '{:.2f}'.format(float(reward_dollar) / 1000)
                    writer.writerow([page_number, reward_amount])

    print("Data Loaded")
