import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc
from tabs.mds_special import mds_special

# Read the data
df_raw = pd.read_csv('data/unemply_df_year.csv', index_col=0)

# Define year options for the range slider
year_options = {year: str(year) for year in range(2000, 2011)}


def make_plot(year_range=[2003, 2005], stat='rate'):

    # register the mds_special theme
    alt.themes.register('mds_special', mds_special)

    # enable the theme
    alt.themes.enable('mds_special')

    # Some data wrangling
    df = df_raw.pivot(index='industry',
                      columns='year',
                      values='total').reset_index()
    new_df = pd.DataFrame(df["industry"])

    # Make the rate plot
    if stat == "rate":
        new_df["rate"] = round((df[year_range[1]] -
                                df[year_range[0]]) / df[year_range[0]], 2)
        cb = alt.Chart(new_df).mark_bar(size=2).encode(
                    alt.X("rate:Q", title="Percentage Change",
                          axis=alt.Axis(tickCount=10, format='%')),
                    alt.Y("industry:O", title=''),
                    color=alt.condition(alt.datum.rate > 0,
                                        alt.value("forestgreen"),
                                        alt.value("red")),
                    tooltip=["rate"])
        cp = alt.Chart(new_df).mark_point(size=70,
                                          filled=True,
                                          opacity=1).encode(
                    alt.X("rate:Q", title="Percentage Change",
                          axis=alt.Axis(tickCount=10, format='%')),
                    alt.Y("industry:O", title=''),
                    color=alt.condition(alt.datum.rate > 0,
                                        alt.value("forestgreen"),
                                        alt.value("red")),
                    tooltip=["rate"])

    # Make the count plot
    if stat == "count":
        new_df["count"] = round(df[year_range[1]] - df[year_range[0]])
        cb = alt.Chart(new_df).mark_bar(size=2).encode(
                    alt.X("count:Q", title="Absolute Change"),
                    alt.Y("industry:O", title=''),
                    color=alt.condition(alt.datum.count > 0,
                                        alt.value("forestgreen"),
                                        alt.value("red")),
                    tooltip=["count"])
        cp = alt.Chart(new_df).mark_point(size=70,
                                          filled=True,
                                          opacity=1).encode(
                    alt.X("count:Q", title="Absolute Change"),
                    alt.Y("industry:O", title=''),
                    color=alt.condition(alt.datum.count > 0,
                                        alt.value("forestgreen"),
                                        alt.value("red")),
                    tooltip=["count"])

    return (cb + cp).properties(
        width=575,
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
                                id='plot',
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
                                    marks=year_options
                                )
                            ],
                                style={"display": "grid",
                                       "grid-template-columns": "90%",
                                       "text-align": "center"}
                            ),
                            html.Br(),
                            # Print the chosen range
                            html.Div(id='year_range-output')
                        ])
                    ])
                ])
