import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
from dash import dash_table
from natsort import natsorted

def get_bead_xy_scatter(data_handler, i):
    locs = data_handler.locs
    locs['selected'] = False
    locs['selected'][i] = True
    labels = {
        'x': 'x (pixel)',
        'y': 'y (pixel)'
    }
    fig = px.scatter(locs, x='x', y='y', color='selected', custom_data='point_id', labels=labels)
    fig.update_layout(clickmode='event')
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
    )
    # fname = locs['fname'][i]
    # print('Setting image')

    # fig.add_layout_image(
    #     dict(
    #         source=data_handler.key_frames[fname],
    #         xref="x",
    #         yref="y",
    #         x=locs['x'].min(),
    #         y=locs['y'].max(),
    #         sizex=1000,
    #         sizey=1000,
    #         sizing="stretch",
    #         opacity=1,
    #         layer="below")
    # )

    return fig

def gen_bead_table(data_handler, i):
    locs = data_handler.locs
    loc_data = locs[locs['point_id']==i].to_dict(orient='records')[0]
    # print(data_handler.locs)
    # loc_data = data_handler.locs.iloc[i].to_dict()
    loc_data['fname'] = loc_data['fname'].split('___')[-1]

    # Delete cols
    for c in ['rejected', 'frame', 'selected']:
        del loc_data[c]
    # Pixel cols
    for c in ['x', 'y', 'sx', 'sy', 'lpx', 'lpy']:
        loc_data[f'{c} (pixels)'] = loc_data.pop(c)

    # nm-scale cols
    for c in ['offset', 'fwhm_xy', 'fwhm_z']:
        loc_data[f'{c} (nm)'] = loc_data.pop(c)


    loc_data = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in loc_data.items()}

    data = [(k, loc_data[k]) for k in natsorted(loc_data.keys())]

    table_header = [
        html.Thead(html.Tr([html.Th("Variable"), html.Th("Value")]))
    ]
    rows = [html.Tr([html.Td(k), html.Td(v)]) for k, v in data]
    table_body = [html.Tbody(rows)]

    table = dbc.Table(table_header + table_body, bordered=True)

    return table

def get_ind_bead_view(data_handler, i):
    ind_bead_container = dbc.Row([
        dbc.Col(children=[
            html.Img(id='ind-bead-profile-img', src=data_handler.get_bead_profile_img(i), style={'width': '100%'}),
        ], width=4),
        dbc.Col(children=[
            dbc.Row(dcc.Graph(id='ind-bead-xy-scatter', figure=get_bead_xy_scatter(data_handler, i))),
            dbc.Row(id='bead-data-table', children=gen_bead_table(data_handler, i))
        ], width=8)
    ])

    return ind_bead_container
