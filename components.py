# components.py

from dash import dcc, html
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from datetime import datetime, timedelta

"""dropdown_options2 = [
    {'label': '訂製片', 'value': 'fig1'},
    {'label': '試賣', 'value': 'fig2'},
    {'label': '拋棄式', 'value': 'fig3'}
]
"""

"""dcc.Dropdown(id='search-input',
                             multi=False,
                             placeholder='Select Sale Type...',
                             options=dropdown_options2,
                             value='fig1', disabled=False, style={'color': 'black'}),
            """

"""html.H5("Select Input Feature files"),
        dcc.Slider(
            id='edge-slider',
            min=1,
            max=3,
            step=1,
            value=1,
            marks={
                1: {'label': '30'},
                2: {'label': '60'},
                3: {'label': '90'}
            }
        ),"""


current_date = datetime.now().date()
next_date = current_date + timedelta(days=1)


nav_content = html.Div([

    html.H2("Dashboard"),

    html.Hr(style={'backgroundColor': 'green'}),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.Button('Compute Analysis', id='update-button', n_clicks=None),
    html.Hr(style={'backgroundColor': 'green'}),


    #navigation controls
    html.H5("Navigations"),
    html.A("Pal & PU", href="#pal"),
    html.Br(),
    html.A("Pal & PU charts", href="#palc"),
    html.Br(),
    html.A("Spedition", href="#sped"),
    html.Br(),
    html.A("Spedition Charts", href="#spedc"),
    html.Br(),
    html.A("Vereint Data Tables", href="#ver"),
    html.Br(),
    html.A("Vereint data Charts", href="#verc"),
    html.Br(),
    html.A("Neue Update Charts", href="#neue"),
    html.Br(),
    html.A("personalisierte kundendaten", href="#per"),


    html.Hr(style={'backgroundColor': 'green'}),
    
])


