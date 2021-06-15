import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime_util import datetime2str, timestamp2datetime
from finnhub_api import FinnHub_init, Finnhub
from datetime import datetime, timedelta
from joblib import load

app = dash.Dash(external_stylesheets=[dbc.themes.LITERA])

df = pd.read_csv('../data/news_all_api_07jun21-14jun21.csv')
df.drop('articles', axis=1, inplace=True)
df.rename(columns={'sent':'sentiment'}, inplace=True)
table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

def live_update_price(symbol):
    finnhub_key = load('../finnhub/finnhub_key.pkl', 'rb')
    start_date = datetime2str(datetime.now() - timedelta(minutes=60))
    end_date = datetime2str(datetime.now())
    symbol = symbol
    
    finhub_inst = Finnhub(finnhub_key, start_date, end_date, symbol)
    df = finhub_inst.stock_candles("1")
    df['date'] = df['date'].apply(lambda x: timestamp2datetime(x))
    df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
    return df

def graph_source_top10():
    source_top10 = df['source'].value_counts(sort=True).nlargest(10)
    fig = px.pie(source_top10,
                values='source',
                names=source_top10.index,
                title='Top 10 news source',
                color_discrete_sequence=px.colors.sequential.RdBu,
                width=800,
                height=600,
                labels=source_top10.index
                )

    fig.update_traces(hoverinfo='label+percent',
                    textfont_size=12,
                    textposition='inside',
                    textinfo='percent+label'
                    )
    return fig

def graph_price():
    fig = px.line(df1, x='date',y=['open' ,'close'])
    fig.update_layout(
                    height=400,
                    width=700,
                    margin={"r":0,"t":50,"l":0,"b":0},
                    paper_bgcolor='white',
                    title='Apple Price',
            xaxis=dict(
                    title='Date & Time',
                    linecolor='black',
                    titlefont_size=10,
                    tickfont_size=10,
                    showgrid=False
                    ),
            yaxis=dict(
                    title='Stock Price',
                    linecolor='black',
                    titlefont_size=10,
                    tickfont_size=10,
                    showgrid=False
                    ),
            legend=dict(
                    title='Prices',
                    x=1,
                    y=1,
                    bgcolor='rgba(255, 255, 255, 0)',
                    bordercolor='rgba(255, 255, 255, 0)'
                    )
                            )
    return fig

def graph_sentiment():
    sentiment = df['sentiment'].value_counts()
    fig = px.bar(sentiment,
              x=sentiment.index,
              y='sentiment',
              color='sentiment'
             )
    fig.update_layout(
                height=400,
                width=700,
                margin={"r":0,"t":50,"l":0,"b":0},
                paper_bgcolor='white',
                title='Sentiment Distribution',
                xaxis_zeroline=False, 
                yaxis_zeroline=False,
        xaxis=dict(
                title='Sentiment',
                linecolor=None,
                titlefont_size=15,
                tickfont_size=15,
                showgrid=False
                ),
        yaxis=dict(
                title='Sentiment Counts',
                linecolor=None,
                titlefont_size=15,
                tickfont_size=15,
                showgrid=False
                ),
        legend=dict(
                x=0,
                y=0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
                )
                        )
    return fig

stocks_style = {
        "position": "fixed",
        "top": 65,
        "left": 250,
        "bottom": 0,
        "width": "50rem",
        "overflow-x": "hidden",
        "padding": "2rem 2rem",
        "background-color": "white",
        }

fig_style = {
        "position": "fixed",
        "top": 225,
        "left": 250,
        "bottom": 0,
        "width": "50rem",
        "overflow-x": "hidden",
        "padding": "2rem 2rem",
        "background-color": "white",
        }

sidebar_style = {
    "position": "fixed",
    "top": 65,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "2rem 2rem",
    "background-color": "white",
    'font-size': '20px'
}

content_style = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Info", header=True),
                dbc.DropdownMenuItem("News Source", href="#"),
                dbc.DropdownMenuItem("Stock Market", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label='More'
        )
    ],
    brand="Stock Market Sentiment Analysis",
    brand_href="#",
    color="primary",
    dark=True,
    expand='xs',
    fluid=True,
    style={'font-size':'20px'}
)

sidebar=html.Div(
            [
                html.P('Stock Market'),
                dbc.Nav(
                        [
                dbc.NavLink("Home", href="/", id='home_link',active="exact"),
                dbc.NavLink("Sentiment Distribution", id='sentiment_link', href="/option1", active="exact"),
                dbc.NavLink("Top 10 News Sources", id='top10_link', href="/option2", active="exact"),
                dbc.NavLink("News Source Sentiment", id='news_link', href="/option3", active="exact")
                        ],
                vertical=True,
                pills=True,
                        )
            ],
            id='nav_bar',
            style=sidebar_style,
        )

def drawText(val):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2(val),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])

stocks = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                html.Div([html.H2("Open", id="open")], id="open_price", style={'textAlign': 'center'}),

                            ])
                        )
                    ]), 
                width=3),
                dbc.Col(
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                html.Div([html.H2("Close", id="close")], id="close_price", style={'textAlign': 'center'})
                            ])
                        )
                    ]), 
                width=3),
                dbc.Col(
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                html.Div([html.H2("High", id="high")], id="high_price", style={'textAlign': 'center'})
                            ])
                        )
                    ]), 
                width=3),
                dbc.Col(
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                html.Div([html.H2("Low", id="low")], id="low_price", style={'textAlign': 'center'})
                            ])
                        )
                    ]), 
                width=3),
            ]
        )
    ],
    style=stocks_style
)

# live_update = html.Div(
#     [
#         html.H2("Stock Price Live Update"),
#         html.Div(id="live_update_text"),
#         dcc.Graph(id="live_update_graph"),
#         dcc.Interval(id="interval1", interval=60*1000, n_intervals=0)
#     ]
# )

# content_style
content = html.Div(id="page-content", children=[], style=content_style)

app.layout = html.Div(
        [
        dcc.Location(id='url', refresh=False),
        navbar,
        sidebar,
        stocks,
        content,
        dcc.Interval(id="interval", interval=10*1000, n_intervals=0)
        ]
    )

@app.callback(
    [
        Output("open_price", "children"),
        Output("close_price", "children"),
        Output("high_price", "children"),
        Output("low_price", "children"),
    ],
    [Input('interval', 'n_intervals')]
    )
def update_interval(n):
    df = live_update_price('AAPL')
    return df.iloc[-1:].open, df.iloc[-1:].close, df.iloc[-1:].high, df.iloc[-1:].low
    # return n,n,n,n

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
    )
def update_content(pathname):

    if pathname == "/":
        return  [
                    html.Div(
                        [
                            html.P("root")
                            # dcc.Graph(id='graph',  style=fig_style)
                        ]
                    )
                ]
    if pathname == "/option1":
        return  [
                    html.Div(
                        [
                            dcc.Graph(id='graph', figure=graph_sentiment(), style=fig_style)
                        ]
                    )
                ]
    elif pathname == "/option2":
        return  [
                    html.Div(
                        [
                            dcc.Graph(id='graph', figure=graph_source_top10(), style=fig_style)
                        ]
                    )
                ]

if __name__=='__main__':
    app.run_server(debug=True, port=8050)