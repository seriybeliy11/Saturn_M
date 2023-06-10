import pandas as pd
import plotly.graph_objects as go

df_v = pd.read_csv('commit_counts.csv')
dates = sorted(df_v.columns[1:-1], reverse=True)
fig_sg = go.Figure()
fig_sg.add_trace(go.Bar(x=df_v['login'], y=df_v[dates[0]], name=dates[0], visible=True))

for date in dates[1:]:
    fig_sg.add_trace(go.Bar(x=df_v['login'], y=df_v[date], name=date, visible=False))

total_count = df_v['count']
fig_sg.add_trace(go.Bar(x=df_v['login'], y=total_count, name='Total Counts', visible=False))

fig_sg.update_layout(
    barmode='stack',
    xaxis=dict(title='Login'),
    yaxis=dict(title='Count'),
    sliders=[{
        'active': len(dates) - 1,
        'currentvalue': {'prefix': 'Date: '},
        'pad': {'t': 50},
        'steps': [{
            'label': date,
            'method': 'update',
            'args': [{'visible': [date == trace.name for trace in fig_sg.data]}, {'title': f'Commit Counts for {date}'}]
        } for date in dates] + [{
            'label': 'Total Counts',
            'method': 'update',
            'args': [{'visible': ['Total Counts' == trace.name for trace in fig_sg.data]}, {'title': 'Total Commit Counts'}]
        }]
    }]
)

fig_sg.update_layout(title=f"Commit Counts for {dates[-1]}")

fig_sg.show()
