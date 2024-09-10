# app.py

import dash
from dash import html
from dash.dependencies import Input, Output

from styles import external_stylesheets, nav_style
from components import nav_content
from dash import dcc

import pandas as pd

from collections import Counter
import numpy as np
from dash import dcc, html
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback



from data_processing import DataPreprocessing
#from EDA import eda
import base64
import io

import warnings
warnings.filterwarnings('ignore') 


@callback(
    Output('inflation-plot', 'figure'),
    Output('output-data-upload2', 'children'),
    Output('plot1', 'figure'),
    Output('plot2', 'figure'),
    Output('plot3', 'figure'),
    Output('plot4', 'figure'),
    Output('output-data-upload3', 'children'),

    Output('output-data-upload4', 'children'),
    #Output('stored-data2', 'data'),
    Output('update-button', 'n_clicks'),

    Input('stored-data', 'data'),
    Input('update-button', 'n_clicks'),
    
)

def update_graph(data, n_clicks):
	
	if(n_clicks == None):
		return {}, html.Div(),{},{},{},{}, html.Div(),html.Div(),None
	else:

		df = pd.DataFrame(data)
		#print(df.head())
		
		data_preprocessor2 = DataPreprocessing(df)
		data_req, ls, fig = data_preprocessor2.clac_2()

		ls2, ls3, fig2, fig3, fig4, fig5 = data_preprocessor2.get_calculated_results()


		return fig, ls ,fig2, fig3,fig4, fig5, ls2 ,ls3, n_clicks


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(children=filename,style={'text-align': 'center'}),
        #html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            style_table={'height': '300px', 'overflowY': 'auto'},
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line
    ]), df

@callback(
    #Output('output-data-upload', 'children'),
    Output('stored-data', 'data'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified')]
)
def update_output(list_of_contents, list_of_names, list_of_dates):

    #print(list_of_contents)
    #print(list_of_names)
    #print(list_of_dates)

    if list_of_contents is not None:
        children = []
        df_combined = pd.DataFrame()
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            child, df = parse_contents(c, n, d)
            children.append(child)
            df_combined = pd.concat([df_combined, df], ignore_index=True)
        return df_combined.to_dict('records')
    return {}



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# App layout
app.layout = html.Div(
	className="app-container", 

	children=[
	html.Div(style=nav_style, children=[nav_content]),
	dcc.Store(id='stored-data'),


	#dascher etc
	html.Div(id='sped',children = [
		html.H2("Spedition Table"),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),
	html.Div(id='output-data-upload2',
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),

	html.Div(id='spedc',children = [
		html.H2("Spedition Chart"),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),
	dcc.Graph(id='inflation-plot',
		style={"height": "80%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),


	#pal and picks tables
	html.Div(id='pal',children = [
		html.H2("Pal & PU Table"),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),
	html.Div(id='output-data-upload3',
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),
	html.Div(id='palc',children = [
		html.H2("Pal & PU Chart"),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),

	html.Div(
		id="basic_details2",
		className="outer-container1",
		children=[
		html.Div(
		className="plots-container",
		children=[
		# Plot 1
		html.Div(
		    className="left-container",
		    children=[
		        html.Div(
		            dcc.Graph(id='plot1',
		                #figure=fig3
		                ),
		            className="plot4",
		            style={"height": "100%", 'width': '50%', 'float': 'left','padding': '10px'}
		        ),]

		        ),

		html.Div(
		    className="left-container",
		    children=[
		        html.Div(
		            dcc.Graph(id='plot2',
		                #figure=fig4
		                ),
		            
		            style={"height": "100%", 'width': '50%', 'float': 'right','padding': '10px'}
		        ),]

		        ),
		])
		],
		style={"height": "50%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
	),

	dcc.Graph(id='plot3',
		style={"height": "80%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),

	dcc.Graph(id='plot4',
		style={"height": "80%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),


	##combined
	html.Div(id='ver',children = [
		html.H2("Vereint Data Tables"),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),
	html.Div(id='output-data-upload4',
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),
	html.Div(id='verc',children = [
		html.H2("Vereint Data  Chart"),
		],
		style={"height": "100%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),
	dcc.Graph(id='inflation-plot-4',
		style={"height": "80%", 'width': '80%', 'float': 'right', 'backgroundColor': '#F2FfF2'}
		),




	    ],
	id="theme_change"
	)

app.css.append_css({
    'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'
})
if __name__ == '__main__':
    app.run_server(debug=True)




