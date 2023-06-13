import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import csv
from plotly.subplots import make_subplots

# Create the Dash app
app = dash.Dash(__name__)

# Configuration
DATA_CONTRIBUTORS_FILE = 'data_contributors.csv'
DATA_ISSUES_FILE = 'data_issues.csv'
ISSUES_SORTED_FILE = 'issues_sorted.csv'
ISSUES_DATA_FILE = 'issues_data.csv'
CONTRIBUTORS_FILE = 'contributors.csv'
COMMIT_COUNTER_FILE = 'commit_counts.csv'
csv_file_path_rewards = 'rewards.csv'

file_names = [
    "issue_numbers_and_durations_2022_06_13_09_39_52.csv",
    "issue_numbers_and_durations_2022_08_13_09_39_52.csv",
    "issue_numbers_and_durations_2022_10_13_09_39_52.csv",
    "issue_numbers_and_durations_2022_12_13_09_39_52.csv",
    "issue_numbers_and_durations_2023_02_01_00_00_00.csv",
    "issue_numbers_and_durations_2023_04_01_00_00_00.csv",
    "issue_numbers_and_durations_2023_06_01_00_00_00.csv"
]

titles = [
    "June 2022",
    "August 2022",
    "October 2022",
    "December 2022",
    "February 2023",
    "April 2023",
    "June 2023"
]


# Clean CSV files from NaT values
csv_files = [DATA_CONTRIBUTORS_FILE, DATA_ISSUES_FILE, ISSUES_SORTED_FILE, ISSUES_DATA_FILE, CONTRIBUTORS_FILE, COMMIT_COUNTER_FILE]

issue_numbers = []
rewards = []

with open(csv_file_path_rewards, mode='r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    for row in reader:
        issue_numbers.append(row[0])
        rewards.append(float(row[1]) / 1000)



for file in csv_files:
    df = pd.read_csv(file)
    df = df.dropna(how='all', axis=1)  # Remove all columns containing only NaT values
    df = df.dropna(how='all', axis=0)  # Remove all rows containing only NaT values
    df.to_csv(file, index=False)

# Read data
data_contributors = pd.read_csv(DATA_CONTRIBUTORS_FILE, usecols=['login', 'contributions'])
data_issues = pd.read_csv(DATA_ISSUES_FILE)
data_issues_sorted = pd.read_csv(ISSUES_SORTED_FILE)
data_s = pd.read_csv(ISSUES_DATA_FILE)

data = pd.read_csv(CONTRIBUTORS_FILE, parse_dates=['date'])
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

colorscale = [[0, 'rgb(0, 0, 255)'], [0.5, 'rgb(0, 255, 0)'], [1, 'rgb(255, 0, 0)']]
colors = {author: i for i, author in enumerate(data['name'].unique())}

# Create the figures
labels_count = data_s['labels'].value_counts()
labels_pie_chart_figure = px.pie(labels_count, values=labels_count.values, names=labels_count.index,
                                 color_discrete_sequence=px.colors.sequential.RdBu,
                                 title='Visual labels report for issues')

duration_diagram_figure = px.bar(data_issues_sorted, x='number', y='duration',
                                 labels={'number': 'Issue Number', 'duration': 'Duration (days)'},
                                 color_discrete_sequence=px.colors.sequential.RdBu)
duration_diagram_figure.update_layout(title='Time to get Footstep approved or declined')

contribution_bar_figure = px.bar(data_contributors, x='login', y='contributions', labels={'login': 'Contributor', 'contributions': 'Contributions'})
contribution_bar_figure.update_layout(xaxis_title='Contributor', yaxis_title='Contributions')

issues_state_pie_figure = px.pie(data_issues, names='state', hole=0.3, labels={'state': 'State'}, color_discrete_sequence=px.colors.sequential.RdBu)
issues_state_pie_figure.update_traces(textposition='inside', textinfo='percent+label')
issues_state_pie_figure.update_layout(title='Issues by State')

fixue_commit_data = pd.read_csv(COMMIT_COUNTER_FILE)
fixue_dates = sorted(fixue_commit_data.columns[1:-1])

fixue_commit_figure = go.Figure()
fixue_commit_figure.add_trace(go.Bar(x=fixue_commit_data['login'], y=fixue_commit_data[fixue_dates[0]], name=fixue_dates[0], visible=True))

for fixue_date in fixue_dates[1:]:
    fixue_commit_figure.add_trace(go.Bar(x=fixue_commit_data['login'], y=fixue_commit_data[fixue_date], name=fixue_date, visible=False))

commits_histo_figure = go.Figure()
for author, group in data.groupby('name'):
    commits_histo_figure.add_trace(go.Bar(x=group['date'], y=group['commits'], marker={'color': colors[author]}, name=author))

total_fixue = fixue_commit_data['count']
fixue_commit_figure.add_trace(go.Bar(x=fixue_commit_data['login'], y=total_fixue, name='Total Counts', visible=False))

rewards_figure = go.Figure(data=[go.Scatter(x=issue_numbers, y=rewards, mode='lines', name='Rewards')])

data_unique_commenters = pd.read_csv('commentators.csv')

unique_commenters_figure = px.bar(data_unique_commenters, x='Number issue', y='Uniq Com',
             labels={'Number issue': 'Issue Number', 'Uniq Com': 'Unique Commentators'})


rewards_figure.update_layout(
    xaxis_title="Issue Number",
    yaxis_title="Rewards (th. $)",
    title="Rewards Graph"
)

fixue_commit_figure.update_layout(
    barmode='stack',
    xaxis=dict(title='Login'),
    yaxis=dict(title='Count'),
    sliders=[{
        'active': len(fixue_dates) - 1,
        'currentvalue': {'prefix': 'Date: '},
        'pad': {'t': 50},
        'steps': [{
            'label': fixue_date,
            'method': 'update',
            'args': [{'visible': [fixue_date == trace.name for trace in fixue_commit_figure.data]}, {'title': f'Commit Counts for {fixue_date}'}]
        } for fixue_date in fixue_dates] + [{
            'label': 'Total Counts',
            'method': 'update',
            'args': [{'visible': ['Total Counts' == trace.name for trace in fixue_commit_figure.data]}, {'title': 'Total Commit Counts'}]
        }]
    }]
)

fixue_commit_figure.update_layout(title=f"Commit Counts for {fixue_dates[-1]}")

approved_data = pd.read_csv("dates_data.csv", parse_dates=["Date"])

permonthdurate_figure = make_subplots(rows=1, cols=7, subplot_titles=titles, shared_yaxes=True)

colorus = ['rgba(100, 149, 237, 1)', 'rgba(70, 130, 180, 1)', 'rgba(0, 0, 128, 1)', 'rgba(0, 0, 205, 1)', 'rgba(0, 0, 255, 1)', 'rgba(30, 144, 255, 1)', 'rgba(135, 206, 235, 1)']

for i, file_name in enumerate(file_names):
    df = pd.read_csv(file_name)
    permonthdurate_figure.add_trace(go.Bar(x=df["number"], y=df["duration"], name=titles[i], marker=dict(color=colorus[i])), row=1, col=i+1)

permonthdurate_figure.update_xaxes(title_text="Issue Number", row=1, col=4)
permonthdurate_figure.update_yaxes(title_text="Duration (Days)", row=1, col=1)

permonthdurate_figure.update_layout(height=700, width=2300, showlegend=True, template='plotly_white')

closed_approved_data_issues = pd.read_csv("github_closed_approved_issues.csv")
closed_approved_data_issues['Date'] = pd.to_datetime(closed_approved_data_issues['Date'])

closed_approved_issues_figure = px.line(closed_approved_data_issues, x='Date', y='Closed Approved Issues', title='Closed Approved Issues over Time')

closed_data_issues = pd.read_csv("github_just_closed_issues.csv")

closed_data_issues['Date'] = pd.to_datetime(closed_data_issues['Date'])

closed_data_issues_figure = px.line(closed_data_issues, x='Date', y='Closed Issues', title='Just closed as not planned Issues over Time')


data_new_issues = pd.read_csv('github_all_issues.csv')

for column in data_new_issues.columns:
    column_data = data_new_issues[column]
    column_df = pd.DataFrame({column: column_data})
    column_df.to_csv(f'{column}.csv', index=False)


data_new_issues = pd.read_csv('All Issues.csv')

data_new_issues.sort_values('All Issues', inplace=True)

data_new_issues.to_csv('All Issues.csv', index=False)

data_new_issues_dates = pd.read_csv('Dates.csv')
data_new_issues_all_issues = pd.read_csv('All Issues.csv')
data_new_issues_combined = pd.concat([data_new_issues_dates, data_new_issues_all_issues], axis=1)

data_new_issues_combined.to_csv('github_all_issues.csv', index=False)

data_new_issues = pd.read_csv('github_all_issues.csv')

data_new_issues_figure = px.line(data_new_issues, x='Dates', y='All Issues', title='All Issues Over Time')

# Define the layout
app.layout = html.Div([
    html.H1("Issue's Metrics"),
    dcc.Graph(figure=labels_pie_chart_figure),
    dcc.Graph(figure=duration_diagram_figure),
    html.H2("Timelines:"),
    dcc.Graph(figure=permonthdurate_figure),
    dcc.Graph(figure=issues_state_pie_figure),
    dcc.Graph(id="pie-chart"),
    dcc.Slider(
        id="date-slider",
        min=0,
        max=len(approved_data) - 1,
        step=1,
        value=0,
        marks={i: str(approved_data["Date"].dt.strftime("%Y-%m-%d").iloc[i]) for i in range(len(approved_data))}
    ),
    dcc.Graph(figure=closed_approved_issues_figure),
    dcc.Graph(figure=closed_data_issues_figure),
    dcc.Graph(figure=data_new_issues_figure),
    html.H1("Contributions Stats"),
    dcc.Graph(figure=contribution_bar_figure),
    html.Div([
        html.H3("Commits Histogram"),
        dcc.Graph(id='commits-histogram', figure=commits_histo_figure),
        dcc.RangeSlider(
            id='date-slider-histogram',
            min=data['date'].dropna().min().timestamp(),
            max=data['date'].dropna().max().timestamp(),
            step=86400,
            value=[data['date'].min().timestamp(), data['date'].max().timestamp()],
            marks={int(date.timestamp()): {'label': date.strftime('%d.%m.%Y'), 'style': {'font-size': '5px'}}
                   for date in data['date'].dropna().unique()}
        ),
        dcc.Graph(figure=fixue_commit_figure),
    html.H1('Rewards Dynamic'),
    dcc.Graph(figure=rewards_figure),
    html.H1('Commentators Stats'),
    dcc.Graph(figure=unique_commenters_figure)
    ])
])

@app.callback(
    Output('commits-histogram', 'figure'),
    Input('date-slider-histogram', 'value')
)
def update_histogram(date_range):
    start_date = pd.to_datetime(date_range[0], unit='s').date()
    end_date = pd.to_datetime(date_range[1], unit='s').date()

    filtered_data = data[(data['date'].dt.date >= start_date) & (data['date'].dt.date <= end_date)]

    updated_histogram = go.Figure()
    for author, group in filtered_data.groupby('name'):
        updated_histogram.add_trace(go.Bar(x=group['date'], y=group['commits'], marker={'color': colors[author]}, name=author))

    return updated_histogram

@app.callback(
    Output("pie-chart", "figure"),
    Input("date-slider", "value")
)
def update_pie_chart(date_index):
    selected_data = approved_data.iloc[date_index]

    date = selected_data["Date"]
    closed_approved_issues = selected_data["Closed Approved Issues"]
    closed_issues = selected_data["Closed Issues"]

    percentage_ratio = closed_approved_issues / closed_issues * 100

    data = {
        "Status": ["Closed Approved Issues", "Closed Issues"],
        "Count": [closed_approved_issues, closed_issues]
    }

    figure_approved = px.pie(data_frame=data, names="Status", values="Count",
                             title=f"Date: {date}, Percentage Ratio: {percentage_ratio:.2f}%")

    return figure_approved

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
