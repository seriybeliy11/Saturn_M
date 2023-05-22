import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import webbrowser

data_contributors = pd.read_csv('data_contributors.csv', usecols=['login', 'contributions'])
data_issues = pd.read_csv('data_issues.csv')
data_issues_sorted = pd.read_csv('issues_sorted.csv')
data_s = pd.read_csv('issues_data.csv')

labels_count = data_s['labels'].value_counts()

fig_p = px.pie(labels_count, values=labels_count.values, names=labels_count.index, color_discrete_sequence=px.colors.sequential.RdBu)
fig_p.update_traces(textposition='inside', textinfo='percent+label')

data = pd.read_csv('contributors.csv', parse_dates=['date'])
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

colorscale = [[0, 'rgb(0, 0, 255)'], [0.5, 'rgb(0, 255, 0)'], [1, 'rgb(255, 0, 0)']]
colors = {author: i for i, author in enumerate(data['name'].unique())}

fig = go.Figure()
for author, group in data.groupby('name'):
    fig.add_trace(go.Bar(x=group['date'], y=group['commits'],
                         marker={'color': colors[author]}, name=author))

data_issues_sorted['duration_days'] = pd.to_numeric(data_issues_sorted['duration'], errors='coerce')

app = dash.Dash(__name__)

fig_duration = px.bar(data_issues_sorted, x='number', y='duration', labels={'number': 'Issue Number', 'duration': 'Duration (days)'}, color_discrete_sequence=px.colors.sequential.RdBu)
fig_duration.update_layout(title='Time to get Footstep approved or declined')

app.layout = html.Div(style={'background': 'linear-gradient(to bottom right, #f7f7f7, #e8e8e8)'},
                      children=[
    html.H1(children='SaturiC - Ton-Footsteps', style={'textAlign': 'center'}),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Graph(id='contrib-graph', figure=fig_p),
            html.H4('Contributors', style={'textAlign': 'center'}),
            html.P('This graph shows the number of useful actions of each participant')
        ]),

        html.Div(className='six columns', children=[
            dcc.Graph(id='issues-state-graph', figure=fig_p),
            html.H4('Issues by State', style={'textAlign': 'center'}),
            html.P('The graph shows the ratio of open and closed issues (shape: pie chart)')
        ])
    ]),

    html.Div(className='row', children=[
        html.Div(className='twelve columns', children=[
            dcc.Graph(id='duration-graph', figure=fig_duration)
        ])
    ]),

    html.Div(className='row', children=[
        html.Div(className='eight columns', children=[
            dcc.Graph(id='histogram', figure=fig),
            html.H4('Commits Histogram', style={'textAlign': 'center'}),
            html.P('Two graphs: graph 1 - a graph of the duration of the existence of problems and general dynamics, graph 2 - a graph showing the moments of the participants actions, time intervals can be selected using the scroll bar')
        ]),
        html.Div(className='four columns', children=[
            dcc.RangeSlider(
                id='date-slider',
                min=data['date'].dropna().min().timestamp(),
                max=data['date'].dropna().max().timestamp(),
                step=86400,
                value=[data['date'].min().timestamp(), data['date'].max().timestamp()],
                marks={int(date.timestamp()): {'label': date.strftime('%d.%m.%Y'), 'style': {'font-size': '5px'}} for date in data['date'].unique()}
            )
        ])
    ]),

    html.Div(className='row', children=[
        html.Div(className='twelve columns', children=[
            dcc.Graph(id='labels-pie', figure=fig_p),
            html.H4('Labels', style={'textAlign': 'center'}),
            html.P('The pie chart shows the ratio of tags that exist within the project for task indexing')
        ])
    ])
])


@app.callback(
    [Output('contrib-graph', 'figure'), Output('issues-state-graph', 'figure'), Output('histogram', 'figure')],
    [Input('contrib-graph', 'clickData'), Input('date-slider', 'value')])
def update_graph(clickData, date_range):
    # Update contributors graph if a data point is clicked
    if clickData:
        login = clickData['points'][0]['label']
        dff = data_contributors[data_contributors.login == login]
        fig_contrib = px.line(dff, x='login', y='contributions', labels={'login': 'Contributor'}, color_discrete_sequence=px.colors.sequential.RdBu)
        fig_contrib.update_traces(mode='lines+markers')
        fig_contrib.update_layout(xaxis_title='Contributor', yaxis_title='Contributions')
    else:
        fig_contrib = px.bar(data_contributors, x='login', y='contributions', labels={'login': 'Contributor', 'contributions': 'Contributions'})
        fig_contrib.update_layout(xaxis_title='Contributor', yaxis_title='Contributions')

    fig_issues_state = px.pie(data_issues, names='state', hole=0.3, labels={'state': 'State'}, color_discrete_sequence=px.colors.sequential.RdBu)
    fig_issues_state.update_traces(textposition='inside', textinfo='percent+label')
    fig_issues_state.update_layout(title='Issues by State')

    filtered_data = data[(data['date'] >= pd.Timestamp.fromtimestamp(date_range[0])) &
                            (data['date'] <= pd.Timestamp.fromtimestamp(date_range[1]))]
    fig = go.Figure()
    for author, group in filtered_data.groupby('name'):
        fig.add_trace(go.Bar(x=group['date'], y=group['commits'],
                             marker={'color': colors[author]}, name=author))
    fig.update_layout(
        xaxis={'title': 'Date', 'tickfont': {'size': 6}},
        yaxis={'title': 'Commits'},
        coloraxis={'colorscale': colorscale, 'colorbar': {'title': 'Author'}}
    )

    return fig_contrib, fig_issues_state, fig


if __name__ == '__main__':
    app.run_server(debug=True)
    webbrowser.open_new('http://localhost:8050/')
