import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Group112 Dash app: Unemployment'

app.config.suppress_callback_exceptions = True
from tabs import tab1, tab2, tab3
#LAYOUT
app.layout = html.Div([ 
    
    html.H3("Unemployment Across Industries", className="display-4"),
                html.P(
                    "These graphs display a framework for countries to examine their unemployment rates/counts across industries",
                    className="display-5"
                ),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Job Growth Across Industries', value='tab-1'),
        dcc.Tab(label='Unemployment Throughout The Years', value='tab-2'),
        dcc.Tab(label='Seasonal Unemployment', value='tab-3'), 
    ]),
    html.Div(id='tabs-content')]
    )  

#TABS FUNCTION
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])              
def render_content(tab):
    if tab == 'tab-1':
        return tab1.content1
    elif tab == 'tab-2':
        return tab2.content2
    elif tab == 'tab-3':
        return tab3.content3

if __name__ == '__main__':
    app.run_server(debug=True)
