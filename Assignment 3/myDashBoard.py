# Student ID: 1852137
# Name: 张艺腾
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()
# open file
df = pd.read_csv('googleplaystore.csv')
df = df.dropna(axis=0, how="any")

# get each category's name
name = df['Category'].unique()

# calculate each category's apps' install times
installs = []
for n in name:
    total = 0
    # print(n)
    dff = df[df['Category'] == n]['Installs']
    for d in dff:
        d = d[0:-1]
        d = d.replace(',', '')
        d = int(d)
        total += d
    # print(total)
    installs.append(total)

# draw the category-install Pie graph
categoryInstallPie = go.Figure(data=go.Pie(
    labels=name,
    values=installs,
    hoverinfo='label+value+percent',
    textinfo='none',
    rotation=220,
    customdata=name
),
    layout=go.Layout(
        title='Each Category\'s Installs'
    )
)

# calculate the count of each rating's apps
rateCount = df.Rating.value_counts()
maxCount = max(rateCount)
rateCount = {'Rating': rateCount.index, 'Count': rateCount.values}
dfRateCount = pd.DataFrame(rateCount)
dfRateCount = dfRateCount.sort_values(by="Rating", ascending=True)


def get_color(temp):
    return 'rgb({r}, {g}, {b})'.format(
        r=int(temp/maxCount*200),
        g=int((1-temp/maxCount)*200),
        b=int((1-temp/maxCount)*200)
    )

# draw the category-count Bar graph
barFig = go.Figure(
    data=go.Bar(
        x=dfRateCount.Rating,
        y=dfRateCount['Count'].astype(int),
        customdata=dfRateCount.Count,
        marker={
            'color': [get_color(count) for count in dfRateCount['Count'].astype(int)]
        }
    ),
    layout=go.Layout(
        yaxis={
            'title': 'Count of App',
        },
        xaxis={
            'title': 'Rating',
        },
        title='Each Rating\'s App Count',
    )
)

# html
app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.RadioItems(
                id='type',
                options=[{'label': type, 'value': type} for type in ['Linear', 'Log']],
                value='Log',
                labelStyle={'display': 'inline-block', 'margin-left': '80%'}
            )
        ],
            style={'width': '45%', 'display': 'inline-block', 'margin-left': '45%'})
    ],
        style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }
    ),
    html.Div(
        dcc.Graph(
            id='circleGraph',
            figure=categoryInstallPie,
            hoverData={'points': [{'customdata': 'ART_AND_DESIGN'}]}
        ),
        style={'display': 'inline-block', 'width': '49%'}
    ),
    html.Div(
        [dcc.Graph(id='graph1'),
         dcc.Graph(id='graph2')],
        style={'display': 'inline-block', 'width': '49%'}
    ),

    html.Div(
        dcc.Graph(
            id='Graph',
            figure=barFig,
        ),
        style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}
    )
])

# change the installs-rating scatter graph when hover on one category of the Pie graph
@app.callback(
    Output('graph1', 'figure'),
    [
        Input('type', 'value'),
        Input('circleGraph', 'hoverData')
    ]
)
def updateGraph1(type, hoverData):
    dff = df[df['Category'] == hoverData['points'][0]['customdata']]
    ydata = dff['Installs']
    yData = []
    for yd in ydata:
        yd = yd[0:-1]
        yd = yd.replace(',', '')
        yd = int(yd)
        yData.append(yd)
    s = dff['Size']
    size = []
    for _s in s:
        if _s == 'Varies with device':
            size.append(0)
            continue
        if 'M' in _s:
            _s = _s.split('M')[0]
            _s = float(_s)
        elif 'k' in _s:
            _s = _s.split('k')[0]
            _s = float(_s) / 1024
        size.append(_s / 2)
    return {
        'data': [go.Scatter(
            x=dff['Rating'].astype(float),
            y=yData,
            mode='markers',
            text=dff['App'] + '<br> Last updated: ' + dff['Last Updated'] + '<br>Size: ' + dff['Size'],
            customdata=dff['App'],
            marker={
                'size': size,
                'opacity': 0.5,
                'color': 'green',
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': {
            'margin': {'l': 50, 'b': 30, 'r': 10, 't': 10},
            'height': 225,
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': hoverData['points'][0]['customdata']
            }],
            'yaxis': {
                'title': 'Installs',
                'type': 'linear' if type == 'Linear' else 'log'
            },
            'xaxis': {
                'title': 'Rating',
                'showgrid': True
            },
            'hovermode': 'closest'
        }
    }

# change the reviews-rating scatter graph when hover on one category of the Pie graph
@app.callback(Output('graph2', 'figure'),
              [Input('circleGraph', 'hoverData'),
               Input('type', 'value')])
def updateGraph2(hoverData, type):
    dff = df[hoverData['points'][0]['customdata'] == df['Category']]
    return {
        'data': [go.Scatter(
            x=dff['Rating'].astype(float),
            y=dff['Reviews'].astype(int),
            mode='markers',
            text=dff['App'] + '<br> Last updated: ' + dff['Last Updated'] + '<br>Size: ' + dff['Size'],
            customdata=dff['App'],
            marker={
                'size': 10,
                'opacity': 0.5,
                'color': '#ffa15a',
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': {
            'margin': {'l': 50, 'b': 30, 'r': 10, 't': 10},
            'height': 225,
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': hoverData['points'][0]['customdata']
            }],
            'yaxis': {
                'title': 'Reviews',
                'type': 'linear' if type == 'Linear' else 'log'
            },
            'xaxis': {
                'title': 'Rating',
                'showgrid': True
            },
            'hovermode': 'closest'
        }
    }


if __name__ == '__main__':
    app.run_server()
