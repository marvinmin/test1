import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc
from app import app

df_raw = pd.read_csv('../data/unemply_df_year.csv', index_col=0)
year_options_1 = {year:str(year) for year in range(2000, 2011)}

def make_plot1(year_range=[2003,2005], stat = 'rate'): #Add in a default value to start with

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
    df = df_raw.pivot(index = 'industry', columns = 'year', values = 'total').reset_index()
    new_df = pd.DataFrame(df["industry"])

    if stat == "rate":
        new_df["rate"] = round((df[year_range[1]] - df[year_range[0]]) / df[year_range[0]], 2)
        cb = alt.Chart(new_df).mark_bar(size = 2).encode(
                    alt.X("rate:Q", title = "Percentage Change", 
                          axis = alt.Axis(tickCount=10, format = '%')),
                    alt.Y("industry:O", title = ''),
                    color = alt.condition(alt.datum.rate > 0, alt.value("forestgreen"), alt.value("red")),
                    tooltip = ["rate"])
        cp = alt.Chart(new_df).mark_point(size = 70, filled = True, opacity = 1).encode(
                    alt.X("rate:Q", title = "Percentage Change",
                          axis = alt.Axis(tickCount=10, format = '%')),
                    alt.Y("industry:O", title = ''),
                    color = alt.condition(alt.datum.rate > 0, alt.value("forestgreen"), alt.value("red")),
                    tooltip = ["rate"])
        
    if stat == "count":
        new_df["count"] = round(df[year_range[1]] - df[year_range[0]])
        cb = alt.Chart(new_df).mark_bar(size = 2).encode(
                    alt.X("count:Q", title = "Absolute Change"),
                    alt.Y("industry:O", title = ''),
                    color = alt.condition(alt.datum.count > 0, alt.value("forestgreen"), alt.value("red")),
                    tooltip = ["count"])
        cp = alt.Chart(new_df).mark_point(size = 70, filled = True, opacity = 1).encode(
                    alt.X("count:Q", title = "Absolute Change"),
                    alt.Y("industry:O", title = ''),
                    color = alt.condition(alt.datum.count > 0, alt.value("forestgreen"), alt.value("red")),
                    tooltip = ["count"])

    return (cb + cp).properties(
        width = 575,
        height = 450
    ).configure_legend(
        titleFontSize = 15,
        labelFontSize = 12
    )

content1 = html.Div([
                    dbc.Row([
                        dbc.Col(width = 1),
                        dbc.Col([
                            html.Br(),
                            html.Iframe(
                                sandbox='allow-scripts',
                                id='plot',
                                height='600',
                                width='900',
                                style={'border-width': '0'},
                                srcDoc=make_plot1().to_html()
                            )
                        ]),
                        dbc.Col([
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.H4('Choose Statistic:'),
                            html.Div(
                                dcc.RadioItems(
                                    id='dd-value',
                                    options=[
                                        {'label': 'Rate', 'value': 'rate'},
                                        {'label': 'Count', 'value': 'count'}
                                    ],
                                    value='rate',
                                    style=dict(width='100%',
                                            verticalAlign="middle")
                                ),
                            ),
                            html.H4('Choose Year Range:'),
                            html.Div([
                                dcc.RangeSlider(
                                    id='year_range',
                                    count=1,
                                    min=2000,
                                    max=2010,
                                    step=1,
                                    value=[2003, 2005],
                                    marks=year_options_1
                                )
                            ], 
                            style={"display": "grid", "grid-template-columns": "90%",
                                   "text-align":"center"}
                            ),
                            html.Br(),
                            html.Div(id='year_range-output')
                        ])
                    ])
                ])

#PLOT 1 CALL BACK  
@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('year_range', 'value'),
     dash.dependencies.Input('dd-value', 'value'),])
def update_plot1(year_range, value):
    updated_plot1 = make_plot1(year_range, value).to_html()
    return updated_plot1

# Tab 1 chosen year range call back
@app.callback(
    dash.dependencies.Output('year_range-output', 'children'),
    [dash.dependencies.Input('year_range', 'value')])
def update_output3(year_range):
    return 'You have selected from {} to {}.'.format(year_range[0], year_range[1])
