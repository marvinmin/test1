import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Group112 Dash app: Unemployment'

app.config.suppress_callback_exceptions = True
