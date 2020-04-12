import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server # the Flask app

data = pd.read_csv('Dash App_data/RFM_Segmentation.csv')

# data for Chart "Revenue per Segment"
df = data.groupby('RFMScore')
df2 = data.groupby('F_Quartile')
df3 = data.groupby('M_Quartile')

best_customers_monetary = (df.get_group(111))['Monetary'].sum()
loyal_customers_monetary = (df2.get_group(1))['Monetary'].sum()
big_spenders_monetary = df3.get_group(1)['Monetary'].sum()
almost_lost_customers_monetary = (df.get_group(311))['Monetary'].sum()
lost_customers_monetary = (df.get_group(411))['Monetary'].sum()
lost_cheap_customers_monetary = (df.get_group(444))['Monetary'].sum()

revenues = [best_customers_monetary, loyal_customers_monetary, big_spenders_monetary,
            almost_lost_customers_monetary, lost_customers_monetary, lost_cheap_customers_monetary]

# data for Chart "Number of Customers per Segment"
BEST_CUSTOMERS = len(data[data['RFMScore'] == 111])
LOYAL_CUSTOMERS = len(data[data['F_Quartile'] == 1])
BIG_SPENDERS = len(data[data['M_Quartile'] == 1])
ALMOST_LOST = len(data[data['RFMScore'] == 311])
LOST_CUSTOMERS = len(data[data['RFMScore'] == 411])
LOST_CHEAP_CUSTOMERS = len(data[data['RFMScore'] == 444])

labels = ['Best Customers', 'Loyal Customers', 'Big Spenders', 'Almost Lost', 'Lost Customers', 'Lost Cheap Customers']
values = [BEST_CUSTOMERS, LOYAL_CUSTOMERS, BIG_SPENDERS, ALMOST_LOST, LOST_CUSTOMERS, LOST_CHEAP_CUSTOMERS]

# Data for Chart "Average Recency"
best_customers_recency = (df.get_group(111))['Recency'].mean()
loyal_customers_recency = (df2.get_group(1))['Recency'].mean()
big_spenders_recency = df3.get_group(1)['Recency'].mean()
almost_lost_customers_recency = (df.get_group(311))['Recency'].mean()
lost_customers_recency = (df.get_group(411))['Recency'].mean()
lost_cheap_customers_recency = (df.get_group(444))['Recency'].mean()

recency_avg = [best_customers_recency, loyal_customers_recency, big_spenders_recency,
               almost_lost_customers_recency, lost_customers_recency, lost_cheap_customers_recency]

fig2 = go.Figure(go.Bar(x=recency_avg, y=labels, orientation='h'))
fig2.update_layout(title={'text':'Avg Recency per Segment'})

app.layout = html.Div(children=[

    html.Div([

        html.H1(children='Customer Segmentation Project')],
    style={'textAlign': 'center'}),

    html.Div([

        dcc.Input(
            id='Best Customers',
            type='number',
            value=BEST_CUSTOMERS,
            style={'font-size': '12px', 'height': '30px', 'width': '90px', 'textAlign': 'left'}),

        html.Label('Best Customers',
                   style={"font-weight": "bold", 'textAlign': 'left', 'font-size': '12px'}),

        dcc.Input(
            id='Loyal Customers',
            type='number',
            value=LOYAL_CUSTOMERS,
            style={'font-size': '12px', 'height': '30px', 'width': '90px', 'textAlign': 'left'}),

        html.Label('Loyal Customers',
                   style={"font-weight": "bold", 'textAlign': 'left', 'font-size': '12px'}),

        dcc.Input(
            id='Big Spenders',
            type='number',
            value=BIG_SPENDERS,
            style={'font-size': '12px', 'height': '30px', 'width': '90px', 'textAlign': 'left'}),

        html.Label('Big Spenders',
                   style={"font-weight": "bold", 'textAlign': 'left', 'font-size': '12px'}),

        dcc.Input(
            id='Almost Lost',
            type='number',
            value=ALMOST_LOST,
            style={'font-size': '12px', 'height': '30px', 'width': '90px', 'textAlign': 'left'}),

        html.Label('Almost Lost ',
                   style={"font-weight": "bold", 'textAlign': 'left', 'font-size': '12px'}),

        dcc.Input(
            id='Lost Customers',
            type='number',
            value=LOST_CUSTOMERS,
            style={'font-size': '12px', 'height': '30px', 'width': '90px', 'textAlign': 'left'}),

        html.Label('Lost Customers ',
                   style={"font-weight": "bold", 'textAlign': 'left', 'font-size': '12px'}),

        dcc.Input(
            id='Lost Cheap Customers',
            type='number',
            value=LOST_CHEAP_CUSTOMERS,
            style={'font-size': '12px', 'height': '30px', 'width': '90px', 'textAlign': 'left'}),
        html.Label('Lost Cheap Customers ',
                   style={"font-weight": "bold", 'textAlign': 'left', 'font-size': '12px'}),

        ], className='one column', style={'margin-top': '100px'}
    ),

    html.Div([

        dcc.Graph(
            id='example-graph-1'
            , className='six columns')]),

    html.Div([

        dcc.Graph(
            id='graph-customers'
            , className='five columns'),

    ]),

    html.Div([

        html.Div([
            html.Label('Use ">[value]", "<[value]" or "=[value]" to filter columns in the table',
                       style={"font-weight": "bold", 'textAlign': 'center', 'font-size': '12px'}),

        ], className='one column', style={'width': '90px'}),

        dash_table.DataTable(
            id='table',
            columns=[
                {"name": i, "id": i} for i in data.columns
            ],
            data=data.to_dict('records'),
            style_data={'border': '1px solid blue'},
            style_header={'border': '1px solid black',
                         'backgroundColor': 'rgb(230, 230, 230)',
                         'fontSize': '13px',
                         'fontWeight': 'bold'},
            style_cell={'fontSize': '13px',
                       'minWidth': '30px',
                       'width': '40px',
                       'maxWidth': '180px'},
            style_cell_conditional=[
                            {'if': {'column_id': 'Monetary'},
                             'width': '25%'},
                            {'if': {'column_id': 'Recency'},
                             'width': '10%'},
                            {'if': {'column_id': 'RFMScore'},
                             'width': '10%'}
                        ],
            style_table={'overflowY': 'scroll',
                        'maxHeight': '300px',
                        'maxWidth': '650px',
                        'overflowX': 'scroll',
                        'margin-left': '125px',
                         'margin-top': '50px'},
            fixed_rows={'headers': True, 'data': 0},
            filter_action='native')
        ],
            className='six columns',
    ),

        html.Div([
            dcc.Graph(
                figure=fig2)],
            style={'paddingRight' : 10,
                   'paddingLeft' : 50},
            className='five columns')]
)

@app.callback(
    [Output('example-graph-1', 'figure')],
    [Input('Best Customers', 'value'), Input('Loyal Customers', 'value'),
     Input('Big Spenders', 'value'), Input('Almost Lost', 'value'),
     Input('Lost Customers', 'value'), Input('Lost Cheap Customers', 'value')])
def update_figure_customers(best, loyal, big, almost, lost, cheap):
    return [{
        'data': [
            {'x': ['Best Customers', 'Loyal Customers', 'Big Spenders', 'Almost Lost', 'Lost Customers',
              'Lost Cheap Customers'], 'y': [best, loyal, big, almost, lost, cheap],
             'type': 'bar'},
        ],
        'layout': {
            'title': 'Number of Customers per Segment',
        }
    }]


@app.callback(
    [Output('graph-customers', 'figure')],
    [Input('Best Customers', 'value'), Input('Loyal Customers', 'value'),
     Input('Big Spenders', 'value'), Input('Almost Lost', 'value'),
     Input('Lost Customers', 'value'), Input('Lost Cheap Customers', 'value')])
def update_figure_customers(best, loyal, big, almost, lost, cheap):
    return [{
        'data': [
            {'labels': ['Best Customers', 'Loyal Customers', 'Big Spenders', 'Almost Lost', 'Lost Customers',
              'Lost Cheap Customers'], 'values': [best, loyal, big, almost, lost, cheap],
             'type': 'pie', 'hole':.3},
        ],
        'layout': {
            'title': 'Revenue per Segment',
            # 'plot_bgcolor': colors['background'],
            #'paper_bgcolor': colors['background']
        }
    }]



if __name__ == '__main__':
    app.run_server(debug=True)
