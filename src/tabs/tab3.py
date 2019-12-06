import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc

from app import app

df_raw = pd.read_csv('../data/unemply_df_month.csv', index_col=0)
industry_options = [{'label': industry, 'value': industry} for industry in df_raw.industry.unique()]
year_options_2 = {year:str(year) for year in range(2000, 2010)}

def make_plot3(industries = ["Agriculture", "Construction"], year = 2000, stat = "rate"): #Add in a default value to start with
    #THEME
    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300,
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0,
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)",
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0,
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)",
                    # titles are by default vertical left of axis so we need to hack this
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels
                },
            }
                }
    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)
    # enable the newly registered theme
    alt.themes.enable('mds_special')

    # Some data wrangling
    new_df = df_raw
    new_df = new_df.query('industry in @industries')
    new_df = new_df.query('year == @year')
    new_df = new_df.loc[:, ['month', 'industry', stat]]
    if stat == "rate":
        cl = alt.Chart(new_df).mark_line(size = 2).encode(
                    alt.X("month:O", axis = alt.Axis(title = "Month", labelAngle = 0)),
                    alt.Y("rate:Q", axis = alt.Axis(title = "Rate", tickCount = 5, format = '%')),
                    alt.Color("industry", title='Industry'),
                    tooltip = ["industry", "month", "rate"]).interactive()
        cp = alt.Chart(new_df).mark_point(size = 10).encode(
                    alt.X("month:O", axis = alt.Axis(title = "Month", labelAngle = 0)),
                    alt.Y("rate:Q", axis = alt.Axis(title = "Rate", tickCount = 5, format = '%')),
                    alt.Color("industry", legend = None),
                    tooltip = ["industry", "month", "rate"]).interactive()
    if stat == "count":
        cl = alt.Chart(new_df).mark_line(size = 2).encode(
                    alt.X("month:O", axis = alt.Axis(title = "Month", labelAngle = 0)),
                    alt.Y("count:Q", axis = alt.Axis(title = "Count")),
                    alt.Color("industry", title='Industry'),
                    tooltip = ["industry", "month", "count"]).interactive()
        cp = alt.Chart(new_df).mark_point(size = 10).encode(
                    alt.X("month:O", axis = alt.Axis(title = "Month", labelAngle = 0)),
                    alt.Y("count:Q", axis = alt.Axis(title = "Count")),
                    alt.Color("industry", legend = None),
                    tooltip = ["industry", "month", "count"]).interactive()
    return (cl + cp).properties(
        width = 600,
        height = 450
    ).configure_legend(
        titleFontSize = 15,
        labelFontSize = 12
    )

content3 = html.Div([
                    dbc.Row([
                        dbc.Col(width = 1),
                        dbc.Col([
                            html.Br(),
                            html.Iframe(
                            sandbox='allow-scripts',
                            id='plot3',
                            height='600',
                            width='900',
                            style={'border-width': '0'},
                            ################ The magic happens here
                            srcDoc=make_plot3().to_html()
                            ################ The magic happens here
                            )
                        ]), 
                        dbc.Col([
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.H4('Choose Statistic:'),
                            html.Div(
                                dcc.RadioItems(
                                    id='dd-value3',
                                    options=[
                                        {'label': 'Rate', 'value': 'rate'},
                                        {'label': 'Count', 'value': 'count'}
                                    ],
                                    value='rate',
                                    style=dict(width='40%',
                                            verticalAlign="middle")
                                )
                            ),
                            html.H4('Choose Industries:'),
                            html.Div(
                                dcc.Dropdown(
                                    id='industries_list3',
                                    options= industry_options,
                                    value=['Agriculture', 'Construction'],
                                    multi=True,
                                    style=dict(width='85%')                                    
                                ),
                            ),
                            html.H4('Choose Year:'),
                            html.Div([
                                dcc.Slider(
                                    id='year3',
                                    min=2000,
                                    max=2009,
                                    value=2000,
                                    marks=year_options_2
                                )
                            ], 
                            style={"display": "grid", "grid-template-columns": "90%",
                                   "text-align":"center"}
                            ),
                            html.Br(),
                            html.Div(id='year3-output')
                        ])
                    ])
                ])
#PLOT 3 CALL BACK  
@app.callback(
    dash.dependencies.Output('plot3', 'srcDoc'),
    [dash.dependencies.Input('industries_list3', 'value'),
     dash.dependencies.Input('year3', 'value'),
     dash.dependencies.Input('dd-value3', 'value'),])
def update_plot3(industries, year, value):
    updated_plot3 = make_plot3(industries, year, value).to_html()
    return updated_plot3

# Tab 3 chosen year call back
@app.callback(
    dash.dependencies.Output('year3-output', 'children'),
    [dash.dependencies.Input('year3', 'value')])
def update_output3(year):
    return 'You have selected Year: {}'.format(year)
