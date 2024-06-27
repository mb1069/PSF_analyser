import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from flask import Flask
import threading
from werkzeug.serving import make_server
import time
DEV_MODE = True

keepPlot=True
def stop_execution():
    global keepPlot
    #stream.stop_stream()
    keepPlot=False
    # stop the Flask server
    server.shutdown()
    server_thread.join()
    print("Dash app stopped gracefully.")
    

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
# app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY, dbc_css])
server = Flask(__name__)
app = Dash(__name__, server=server, use_pages=True, external_stylesheets=[dbc.themes.DARKLY, dbc_css])


# Home page layout
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
    

if __name__ == '__main__':
    # create a server instance
    server = make_server("localhost", 8050, server)
    # start the server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    # start the Dash app in a separate thread
    def start_dash_app():
        app.run_server(debug=True, use_reloader=False)

    dash_thread = threading.Thread(target=start_dash_app)
    dash_thread.start()

    while keepPlot:
        time.sleep(1)  # keep the main thread alive while the other t