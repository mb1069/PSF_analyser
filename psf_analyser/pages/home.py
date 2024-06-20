import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('To get started, go to "Prepare Data", and click submit'),
    html.A(title='Click here', href='/prepare-data')
])