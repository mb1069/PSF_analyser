import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

DEV_MODE = True


def main():
    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY, dbc_css])

    app.layout = dbc.Container([
        html.H1('PSF analyser'),
        html.A(children=html.P('To home page'), href='/'),
        dash.page_container
    ])
    args = {
        # 'suppress_callback_exceptions': not DEV_MODE,
        'debug': DEV_MODE,
        'dev_tools_ui': DEV_MODE,
        'dev_tools_props_check': DEV_MODE
    }
    app.run(host='0.0.0.0', **args)


if __name__ == '__main__':
    main()
