import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from flask import Flask
import plotly.graph_objects as go
import webbrowser

data_contributors = pd.read_csv('data_contributors.csv', usecols=['login', 'contributions'])
data_issues = pd.read_csv('data_issues.csv')
data_issues_sorted = pd.read_csv('issues_sorted.csv')
data_s = pd.read_csv('issues_data.csv')

labels_count = data_s['labels'].value_counts()

fig_p = px.pie(labels_count, values=labels_count.values, names=labels_count.index, title='Distribution of labels', color_discrete_sequence=px.colors.sequential.RdBu)


data = pd.read_csv('contributors.csv', parse_dates=['date'])
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

colorscale = [[0, 'rgb(0, 0, 255)'], [0.5, 'rgb(0, 255, 0)'], [1, 'rgb(255, 0, 0)']]
colors = {author: i for i, author in enumerate(data['name'].unique())}

fig = go.Figure()
for author, group in data.groupby('name'):
    fig.add_trace(go.Bar(x=group['date'], y=group['commits'],
                         marker={'color': colors[author]}, name=author,
                         hovertemplate='Author: %{name}<br>Date: %{x}<br>Commits: %{y}<extra></extra>'))


data_issues_sorted['duration_days'] = pd.to_numeric(data_issues_sorted['duration'], errors='coerce')

app = dash.Dash(__name__)


fig_duration = px.bar(data_issues_sorted, x='number', y='duration', labels={'number': 'Issue Number', 'durations': 'Duration (days)'}, color_discrete_sequence=px.colors.sequential.RdBu)
fig_duration.update_layout(title='Time to get Footstep approved or declined')

app.layout = html.Div(children=[
    html.H1(children='SaturiC - Ton-Footsteps', style={'textAlign':'center'}),

    html.Div([
        html.Div([
            html.H2(children='Contribution chart', style={'textAlign':'center'}),
            dcc.Graph(id='contrib-graph', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
        ], className='six columns'),

        html.Div([
            html.H2(children='Issues state chart', style={'textAlign':'center'}),
            dcc.Graph(id='issues-state-graph', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
        ], className='six columns')
    ], className='row'),

    html.Div([
        html.H2(children='Distribution of project durations', style={'textAlign':'center'}),
        dcc.Graph(id='duration-graph', figure=fig_duration, style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
    ]),

    html.Div([
        html.H2(children='Distribution of Ton-Footsteps', style={'textAlign':'center'}),
        dcc.Graph(id='histogram', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
        dcc.RangeSlider(
            id='date-slider',
            min=data['date'].dropna().min().timestamp(),
            max=data['date'].dropna().max().timestamp(),
            step=86400,
            value=[data['date'].min().timestamp(), data['date'].max().timestamp()],
            marks={int(date.timestamp()): {'label': date.strftime('%d.%m.%Y'), 'style': {'font-size': '5px'}} for date in data['date'].unique()}
        )
    ]),

    html.Div([
        html.Div([
            html.H2(children='Proportion of labels assigned', style={'textAlign':'center'}),
            dcc.Graph(id='labels-pie', figure=fig_p, style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
    ])
])




@app.callback(
    [Output('contrib-graph', 'figure'), Output('issues-state-graph', 'figure'), Output('histogram', 'figure')],
    [Input('contrib-graph', 'clickData'), Input('date-slider', 'value')])

def update_graph(clickData, date_range):
    # Update contributors graph if a data point is clicked
    if clickData:
        login = clickData['points'][0]['x']
        dff = data_contributors[data_contributors.login == login]
        fig_contrib = px.line(dff, x='login', y='contributions', labels={'login': 'Contributor'}, color_discrete_sequence=px.colors.sequential.RdBu)
        fig_contrib.update_traces(mode='lines+markers')
        fig_contrib.update_layout(title=f'Contributions by {login}', xaxis_title='Contributor', yaxis_title='Contributions')
    else:
        fig_contrib = px.bar(data_contributors, x='login', y='contributions', labels={'login': 'Contributor', 'contributions': 'Contributions'})
        fig_contrib.update_layout(title='Contributions by Contributor', xaxis_title='Contributor', yaxis_title='Contributions', plot_bgcolor='#fff', paper_bgcolor='#fff', font=dict(size=12, color='#333'), colorway=px.colors.sequential.RdBu)


    # Update issues-state graph
    fig_issues_state = px.pie(data_issues, names='state', hole=.0, labels={'state': 'State'}, color_discrete_sequence=px.colors.sequential.RdBu)
    fig_issues_state.update_traces(marker=dict(colors=['#EF553B', '#00CC96']))
    fig_issues_state.update_layout(title='Issues by State')

    filtered_data = data[(data['date'] >= pd.Timestamp.fromtimestamp(date_range[0])) &
                            (data['date'] <= pd.Timestamp.fromtimestamp(date_range[1]))]
    fig = go.Figure()
    for author, group in filtered_data.groupby('name'):
        fig.add_trace(go.Bar(x=group['date'], y=group['commits'],
                             marker={'color': colors[author]}, name=author,
                             hovertemplate='Author: %{name}<br>Date: %{x}<br>Commits: %{y}<extra></extra>'))
    fig.update_layout(
        xaxis={'title': 'Date', 'tickfont': {'size': 6}},
        yaxis={'title': 'Commits'},
        coloraxis={'colorscale': colorscale, 'colorbar': {'title': 'Author'}}
    )

    return fig_contrib, fig_issues_state, fig


if __name__ == '__main__':
    app.run_server(debug=True)
    webbrowser.open_new('http://localhost:8050/')
