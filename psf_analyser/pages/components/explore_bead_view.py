from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px


def get_explore_bead_fig(df, x_axis, y_axis, hue_axis, graph):
    if graph == "line":
        fig = px.line(df, x=x_axis, y=y_axis, color=hue_axis, title="Line Chart")
    elif graph == "bar":
        fig = px.bar(df, x=x_axis, y=y_axis, color=hue_axis, title="Bar Chart")
    elif graph == "scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=hue_axis, title="Scatter Chart")
    elif graph == "2dhistogram":
        fig = px.density_heatmap(
            df,
            x=x_axis,
            y=y_axis,
            color=hue_axis, 
            nbinsx=20,
            nbinsy=20,
            color_continuous_scale="Viridis",
            title="2D Histogram Chart",
        )
    return fig


def get_explore_bead_view(locs):
    cols = list(locs)
    col_options = [{'value': c, 'label': c} for c in cols]

    x_col_sel = dcc.Dropdown(
        id='bead-explore-x-col-sel',
        options=col_options,
        value='x',
        clearable=False
    )
    y_col_sel = dcc.Dropdown(
        id='bead-explore-y-col-sel',
        options=col_options,
        value='y',
        clearable=False
    )
    hue_col_sel = dcc.Dropdown(
        id='bead-explore-hue-col-sel',
        options=col_options,
        value='y',
        clearable=True
    )
    type_sel = dcc.Dropdown(
        id="bead-explore-graph-type-sel",
        options=[
            {"value": "line", "label": "Line chart"},
            {"value": "bar", "label": "Bar chart"},
            {"value": "scatter", "label": "Scatter chart"},
            {"value": "2dhistogram", "label": "2d-histogram chart"},
        ],
        value='scatter',
        clearable=False,
    )
    sel_row = dbc.Row([
            dbc.Col(x_col_sel),
            dbc.Col(y_col_sel),
            dbc.Col(hue_col_sel),
            dbc.Col(type_sel),
        ], className='dbc'
    )
    plot_row = dbc.Row(dbc.Col(
        dcc.Graph(id="bead-explore-graph", figure={})
    ))
    return html.Div(children=[sel_row, plot_row])
