import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc
from tabs.mds_special import mds_special

# Read the data
df_raw = pd.read_csv('data/unemply_df_month.csv', index_col=0)

# Define industry options for the dropdown list
industry_options = [{'label': industry, 'value': industry}
                    for industry in df_raw.industry.unique()]

# Define year options for the slider
year_options_2 = {year: str(year) for year in range(2000, 2010)}


def make_plot(industries=["Agriculture", "Construction"],
              year=2000, stat="rate"):

    # register the mds_special theme
    alt.themes.register('mds_special', mds_special)
    # enable the theme
    alt.themes.enable('mds_special')

    # Some data wrangling
    new_df = df_raw
    new_df = new_df.query('industry in @industries')
    new_df = new_df.query('year == @year')
    new_df = new_df.loc[:, ['month', 'industry', stat]]

    # Make the rate plot
    if stat == "rate":
        cl = alt.Chart(new_df).mark_line(size=2).encode(
                    alt.X("month:O", axis=alt.Axis(title="Month",
                                                   labelAngle=0)),
                    alt.Y("rate:Q", axis=alt.Axis(title="Rate",
                                                  tickCount=5,
                                                  format='%')),
                    alt.Color("industry", title='Industry'),
                    tooltip=["industry", "month", "rate"]).interactive()
        cp = alt.Chart(new_df).mark_point(size=10).encode(
                    alt.X("month:O", axis=alt.Axis(title="Month",
                                                   labelAngle=0)),
                    alt.Y("rate:Q", axis=alt.Axis(title="Rate",
                                                  tickCount=5,
                                                  format='%')),
                    alt.Color("industry", legend=None),
                    tooltip=["industry", "month", "rate"]).interactive()

    # Make the count plot
    if stat == "count":
        cl = alt.Chart(new_df).mark_line(size=2).encode(
                    alt.X("month:O", axis=alt.Axis(title="Month",
                                                   labelAngle=0)),
                    alt.Y("count:Q", axis=alt.Axis(title="Count")),
                    alt.Color("industry", title='Industry'),
                    tooltip=["industry", "month", "count"]).interactive()
        cp = alt.Chart(new_df).mark_point(size=10).encode(
                    alt.X("month:O", axis=alt.Axis(title="Month",
                                                   labelAngle=0)),
                    alt.Y("count:Q", axis=alt.Axis(title="Count")),
                    alt.Color("industry", legend=None),
                    tooltip=["industry", "month", "count"]).interactive()
    return (cl + cp).properties(
        width=600,
        height=450
    ).configure_legend(
        titleFontSize=15,
        labelFontSize=12
    )

# Make the content for the tab
content = html.Div([
                    dbc.Row([
                        # Add space to the left of the dash board
                        dbc.Col(width=1),
                        dbc.Col([
                            # Add some space on the top of the plot
                            html.Br(),
                            html.Iframe(
                                sandbox='allow-scripts',
                                id='plot3',
                                height='600',
                                width='900',
                                style={'border-width': '0'},
                                srcDoc=make_plot().to_html()
                            )
                        ]),
                        dbc.Col([
                            # Add more space to the top of the radio buttons
                            html.Br(),
                            html.Br(),
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
                                    options=industry_options,
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
                                style={"display": "grid",
                                       "grid-template-columns": "90%",
                                       "text-align": "center"}
                            ),
                            html.Br(),
                            # Print the chosen year
                            html.Div(id='year3-output')
                        ])
                    ])
                ])
