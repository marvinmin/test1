import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from tabs import tab1, tab2, tab3

app = dash.Dash(__name__, assets_folder='assets',
                external_stylesheets=[dbc.themes.CERULEAN])
server = app.server
app.title = 'Group112 Dash app: Unemployment'
app.config.suppress_callback_exceptions = True

# LAYOUT
app.layout = html.Div([
    html.H3("Unemployment Across Industries", className="display-4"),
            html.P(
                """These graphs display a framework for countries to examine
                their unemployment rates/counts across industries.""",
                className="display-5"
                    ),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Job Growth Across Industries', value='tab-1'),
        dcc.Tab(label='Unemployment Throughout The Years', value='tab-2'),
        dcc.Tab(label='Seasonal Unemployment', value='tab-3'),
    ]),
    html.Div(id='tabs-content')]
    )

# TABS FUNCTION
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1.content
    elif tab == 'tab-2':
        return tab2.content
    elif tab == 'tab-3':
        return tab3.content

# PLOT 1 CALL BACK
@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('year_range', 'value'),
     dash.dependencies.Input('dd-value', 'value')])
def update_plot1(year_range, value):
    updated_plot1 = tab1.make_plot(year_range, value).to_html()
    return updated_plot1

# Tab 1 chosen year range call back
@app.callback(
    dash.dependencies.Output('year_range-output', 'children'),
    [dash.dependencies.Input('year_range', 'value')])
def update_output1(year_range):
    return 'You have selected from {} to {}.'.format(year_range[0],
                                                     year_range[1])

# PLOT 2 CALL BACK
@app.callback(
    dash.dependencies.Output('plot2', 'srcDoc'),
    [dash.dependencies.Input('industries_list', 'value'),
     dash.dependencies.Input('dd-value2', 'value')])
def update_plot2(industries, value):
    updated_plot2 = tab2.make_plot(industries, value).to_html()
    return updated_plot2

# PLOT 3 CALL BACK
@app.callback(
    dash.dependencies.Output('plot3', 'srcDoc'),
    [dash.dependencies.Input('industries_list3', 'value'),
     dash.dependencies.Input('year3', 'value'),
     dash.dependencies.Input('dd-value3', 'value')])
def update_plot3(industries, year, value):
    updated_plot3 = tab3.make_plot(industries, year, value).to_html()
    return updated_plot3

# Tab 3 chosen year call back
@app.callback(
    dash.dependencies.Output('year3-output', 'children'),
    [dash.dependencies.Input('year3', 'value')])
def update_output3(year):
    return 'You have selected Year: {}'.format(year)

if __name__ == '__main__':
    app.run_server(debug=True)
