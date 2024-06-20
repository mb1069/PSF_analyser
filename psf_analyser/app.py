import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

def main():
    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY, dbc_css])

    app.layout = dbc.Container([
        html.H1('Multi-page app with Dash Pages'),
        html.Div([
            html.Div(
                dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
            ) for page in dash.page_registry.values()
        ]),
        dash.page_container
    ])
    app.run(debug=True, host= 'ma-mdb119.ma.ic.ac.uk')

if __name__ == '__main__':
    main()