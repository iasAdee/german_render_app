import pandas as pd
import plotly.graph_objs as go
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from dash import dcc, html
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import re

class DataPreprocessing:
	def __init__(self, data):
		self.data = data

	def clac_2(self):
		data_req = self.data[["SalesOrder", "Werk", "KomplettLF_KZ", "Summe von BrGew_Offen", "WE_PLZ"]]
		ls = []
		for i in range(len(data_req)):
		    x = data_req["KomplettLF_KZ"][i]
		    so = data_req["SalesOrder"][i]
		    we = data_req["WE_PLZ"][i]
		    wr = data_req["Werk"][i]

		    if(x == "X"):
		        dat = data_req[data_req["SalesOrder"] == so]
		        sum_tocheck = sum(dat["Summe von BrGew_Offen"])
		        if(wr == "DE01" or we == "DE10"):
		            if(sum_tocheck < 50):
		                ls.append("TOF")
		            if(sum_tocheck > 50 and sum_tocheck < 2500):
		                ls.append("Dachser")
		            if(sum_tocheck > 2500):
		                ls.append("Direkt")
		        else:
		            if(sum_tocheck < 80):
		                ls.append("TOF")
		            if(sum_tocheck > 80 and sum_tocheck < 2500):
		                ls.append("Dachser")
		            if(sum_tocheck > 2500):
		                ls.append("Direkt")
		    else:
		        sum_tocheck = self.data["Summe von BrGew_Offen"][i]

		        if(wr == "DE01" or we == "DE10"):
		            if(sum_tocheck < 50):
		                ls.append("TOF")
		            if(sum_tocheck > 50 and sum_tocheck < 2000):
		                ls.append("Dachser")
		            if(sum_tocheck > 2000):
		                ls.append("Direkt")
		        else:
		            if(sum_tocheck < 80):
		                ls.append("TOF")
		            if(sum_tocheck > 80 and sum_tocheck < 2000):
		                ls.append("Dachser")
		            if(sum_tocheck > 2000):
		                ls.append("Direkt")

		data_req["new_col"] = ls


		ls = []
		ls.append(html.Div([
		dash_table.DataTable(
		    style_table={'height': '500px', 'overflowY': 'auto', 'width':'98%', 'margin-left':'4px'},
		    data=data_req.to_dict('records'),
		    columns=[{"name": i, "id": i} for i in data_req.columns],
		    #editable=True,
		    filter_action="native",
		    sort_action="native",
		    #page_action="native",
		    style_header={
		        'backgroundColor': 'blue',
		        'color': 'white',
		        'fontWeight': 'bold',
		        'textAlign': 'center',
		        'border': '1px solid black'
		    }),html.Hr()])
		)

		fig = go.Figure()

		value_counts = data_req['new_col'].value_counts()

		#color_mapping = {'TOF': 'blue', 'Dachser': 'orange', 'Direkt': 'green'}
		#data_req['color'] = data_req['new_col'].map(color_mapping)

		# Create the bar plot with Plotly
		fig = go.Figure(data=[
		    go.Bar(
		        x=value_counts.index,  # Bar labels
		        y=value_counts.values,  # Bar heights
		        #color='color',
		        text=value_counts.values,  # Text annotations on bars
		        textposition='outside'  # Position annotations outside the bars
		    )
		])

		# Update layout to match the styling of the Matplotlib plot
		fig.update_layout(
		    title='Picks Distribution',
		    xaxis_title='Selected values',
		    yaxis_title='Count',
		    template='plotly_white'
		)


		return data_req, ls, fig




	def get_calculated_results(self):

		def get_number(sentence):
		    match1 = re.search(r'\((\d+)\)\s*KG', sentence)
		    if match1:
		        number1 = match1.group(1)
		        return int(number1)
		    else:
		        match2 = re.search(r'HO(\d+)KG', sentence)
		        if match2:
		            number2 = match2.group(1)
		            return int(number2)
		        else:
		            return 0

		def get_number2(sentence):
		    pattern = r'(\d+)x(\d+)'
		    matches1 = re.findall(pattern, sentence)
		    for match in matches1:
		        return match[0], match[1]
		    else:
		        return 0, 0

		def make_sender_dict(data):
		    all_senders = set(data["AG-ID"])
		    sender_dict = {}
		    for sender in all_senders:
		        first = data[data["AG-ID"] == sender]

		        recivers =first["WE-ID"]
		        same_occurances = list(recivers).count(sender)
		        total_recivers = len(recivers)
		        other = abs(total_recivers - same_occurances)

		        sender_dict[sender] = [other, same_occurances]
			    
		    return sender_dict


		data_required = self.data[["Auftragsmenge_Offen", "AME", "BME", "BereitStellDat", "Zähler",
		                     "SKU_Zähler", "MatBez", "MatNr", "Auftragsmenge_bereits_geliefert",
		                     "SalesOrder", "Werk", "KomplettLF_KZ", "Summe von BrGew_Offen", "WE_PLZ"]]

		data_collection = []
		data_collection2 = []
		ls2 = []

		for i in range(len(data_required)):
		    ame = data_required["AME"][i]
		    bme = data_required["BME"][i]
		    order = data_required["Auftragsmenge_Offen"][i]

		    pallet = data_required["Zähler"][i]
		    date = data_required["BereitStellDat"][i]
		    SKU_Zähler = data_required["SKU_Zähler"][i]
		    MatBez = data_required["MatBez"][i]
		    MatNr = data_required["MatNr"][i]


		    ls = []
		    nodata = False

		    if(ame == "ST" and bme == "ST"):
		        order = data_required["Auftragsmenge_Offen"][i]
		        pallet = data_required["Zähler"][i]
		        com = data_required['Auftragsmenge_bereits_geliefert'][i]

		        if(pd.isna(order) or pd.isna(pallet) or pd.isna(pallet)):
		            continue
		        if(order < pallet):
		            ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, order, 0])
		        else:
		            pallet_ = int(order / pallet)
		            pieces = abs(int(order / pallet) * pallet - order)

		            ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, pieces, pallet_])
		        data_collection2.append(ls[0].copy())
		        nodata = True
		    if(ame == "KAR" and bme == "ST"):
		        order = data_required["Auftragsmenge_Offen"][i]
		        pallet = data_required["Zähler"][i]
		        com = data_required['Auftragsmenge_bereits_geliefert'][i]
		        pallet_val = data_required["SKU_Zähler"][i]

		        if(pd.isna(order) or pd.isna(pallet) or pd.isna(pallet_val)):
		            continue

		        comparison = pallet / pallet_val
		        if(order < comparison):
		            ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, order, 0])
		        else:
		            pallet_ = int(order / comparison)
		            pieces = abs(int(order / comparison) * comparison - order)

		            ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, pieces, pallet_])
		        data_collection2.append(ls[0].copy())
		        nodata = True
		    if(ame == "KG" and bme == "KG"):
		        order = data_required["Auftragsmenge_Offen"][i]
		        pallet = data_required["Zähler"][i]
		        com = data_required['Auftragsmenge_bereits_geliefert'][i]
		        if(pd.isna(order) or pd.isna(pallet)):
		            continue

		        text = data_required["MatBez"][i]
		        kg = get_number(text)
		        if(kg == 0):
		            continue
		        else:
		            order_actual = order / kg
		            pallet_actual = pallet / kg

		            if(order_actual < pallet_actual):
		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, order_actual, 0])
		            else:
		                pallet_ = int(order_actual / pallet_actual)
		                pieces = abs(int(order_actual / pallet_actual) * pallet_actual - order_actual)

		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, pieces, pallet_])
		        data_collection2.append(ls[0].copy())
		        nodata = True
		    if(ame == "KG" and bme == "ST"):
		        order = data_required["Auftragsmenge_Offen"][i]
		        pallet = data_required["Zähler"][i]
		        com = data_required['Auftragsmenge_bereits_geliefert'][i]
		        if(pd.isna(order) or pd.isna(pallet)):
		            continue

		        text = data_required["MatBez"][i]
		        kg = get_number(text)
		        if(kg == 0):
		            continue
		        else:
		            req_num = pallet * kg
		            if(order < req_num):
		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, order, 0])
		            else:
		                pallet_ = int(order / req_num)
		                pieces = abs(int(order / req_num) * req_num - order)

		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, pieces, pallet_])

		        data_collection2.append(ls[0].copy())
		        nodata = True
		    if(ame == "L" and bme == "ST"):
		        order = data_required["Auftragsmenge_Offen"][i]
		        com = data_required['Auftragsmenge_bereits_geliefert'][i]
		        pallet = data_required["Zähler"][i]

		        text = data_required["MatBez"][i]
		        n1, n2 = get_number2(text)

		        if(com != 0):
		            num = int(order / com)
		            if(num < pallet):
		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, int(num), 0])
		            else:
		                pallet_ = int(num / pallet)
		                pieces = abs(int(num / pallet) * pallet - num)

		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, pieces, pallet_])
		            data_collection2.append(ls[0])

		        elif(n1 != 0 and n2 != 0):
		            nu = (int(n1) * int(n2)) / 1000
		            num = int(order / nu)
		            pallet1 = pallet / nu
		            if(num < pallet1):
		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, int(num), 0])
		            else:
		                pallet_ = int(num / pallet)
		                pieces = abs(int(num / pallet) * pallet - num)

		                ls.append([ame, bme, com, order, pallet, date, SKU_Zähler, MatBez, MatNr, pieces, pallet_])
		            data_collection2.append(ls[0].copy())
		            nodata = True


		    if(nodata == True):
		        #nls = ls[0].copy()
		        #data_collection2.append(nls)

		        x = data_required["KomplettLF_KZ"][i]
		        so = data_required["SalesOrder"][i]
		        we = data_required["WE_PLZ"][i]
		        wr = data_required["Werk"][i]


		        if(x == "X"):
		            dat = data_required[data_required["SalesOrder"] == so]
		            sum_tocheck = sum(dat["Summe von BrGew_Offen"])
		            if(wr == "DE01" or we == "DE10"):
		                if(sum_tocheck < 50):
		                    ls[0].extend([x, so, we, wr,"TOF"])
		                if(sum_tocheck > 50 and sum_tocheck < 2500):
		                    ls[0].extend([x, so, we, wr,"Dachser"])
		                if(sum_tocheck > 2500):
		                    ls[0].extend([x, so, we, wr,"Direkt"])
		            else:
		                if(sum_tocheck < 80):
		                    ls[0].extend([x, so, we, wr,"TOF"])
		                if(sum_tocheck > 80 and sum_tocheck < 2500):
		                    ls[0].extend([x, so, we, wr,"Dachser"])
		                if(sum_tocheck > 2500):
		                    ls[0].extend([x, so, we, wr,"Direkt"])
		        else:
		            sum_tocheck = self.data["Summe von BrGew_Offen"][i]

		            if(wr == "DE01" or we == "DE10"):
		                if(sum_tocheck < 50):
		                    ls[0].extend([x, so, we, wr,"TOF"])
		                if(sum_tocheck > 50 and sum_tocheck < 2000):
		                    ls[0].extend([x, so, we, wr,"Dachser"])
		                if(sum_tocheck > 2000):
		                    ls[0].extend([x, so, we, wr,"Direkt"])
		            else:
		                if(sum_tocheck < 80):
		                    ls[0].extend([x, so, we, wr,"TOF"])
		                if(sum_tocheck > 80 and sum_tocheck < 2000):
		                    ls[0].extend([x, so, we, wr,"Dachser"])
		                if(sum_tocheck > 2000):
		                    ls[0].extend([x, so, we, wr,"Direkt"])

		        data_collection.append(ls[0])

		#print(data_collection2)
		datahalf = pd.DataFrame(data_collection2, columns=["AME", "BME", "com", "Auftragsmenge_Offen",
		                                                      "Zähler", "BereitStellDat", "SKU_Zähler",
		                                                      "MatBez", "MatNr", "Picks", "Pallets"])

		datextracted = pd.DataFrame(data_collection, columns=["AME", "BME", "com", "Auftragsmenge_Offen",
		                                                      "Zähler", "BereitStellDat", "SKU_Zähler",
		                                                      "MatBez", "MatNr", "Picks", "Pallets", "KomplettLF_KZ", "SalesOrder", "WE_PLZ", "Werk", "new_col"])

		ls = []
		ls.append(html.Div([
		dash_table.DataTable(
		    style_table={'height': '500px', 'overflowY': 'auto', 'width':'98%', 'margin-left':'4px'},
		    data=datahalf.to_dict('records'),
		    columns=[{"name": i, "id": i} for i in datahalf.columns],
		    #editable=True,
		    filter_action="native",
		    sort_action="native",
		    #page_action="native",
		    style_header={
		        'backgroundColor': 'blue',
		        'color': 'white',
		        'fontWeight': 'bold',
		        'textAlign': 'center',
		        'border': '1px solid black'
		    }),html.Hr()])
		)


		ls2 = []
		ls2.append(html.Div([
		dash_table.DataTable(
		    style_table={'height': '500px', 'overflowY': 'auto', 'width':'98%', 'margin-left':'4px'},
		    data=datextracted.to_dict('records'),
		    columns=[{"name": i, "id": i} for i in datextracted.columns],
		    #editable=True,
		    filter_action="native",
		    sort_action="native",
		    #page_action="native",
		    style_header={
		        'backgroundColor': 'blue',
		        'color': 'white',
		        'fontWeight': 'bold',
		        'textAlign': 'center',
		        'border': '1px solid black'
		    }),html.Hr()])
		)

		fig = go.Figure()

		value_counts = datahalf['AME'].value_counts()

		# Create the bar plot with Plotly
		fig = go.Figure(data=[
		    go.Bar(
		        x=value_counts.index,  # Bar labels
		        y=value_counts.values,  # Bar heights
		        text=value_counts.values,  # Text annotations on bars
		        textposition='outside'  # Position annotations outside the bars
		    )
		])

		# Update layout to match the styling of the Matplotlib plot
		fig.update_layout(
		    title='AME Distribution',
		    xaxis_title='Selected values',
		    yaxis_title='Count',
		    template='plotly_white'
		)


		fig2 = go.Figure()

		value_counts = datahalf['BME'].value_counts()

		# Create the bar plot with Plotly
		fig2 = go.Figure(data=[
		    go.Bar(
		        x=value_counts.index,  # Bar labels
		        y=value_counts.values,  # Bar heights
		        text=value_counts.values,  # Text annotations on bars
		        textposition='outside'  # Position annotations outside the bars
		    )
		])

		# Update layout to match the styling of the Matplotlib plot
		fig2.update_layout(
		    title='BME Distribution',
		    xaxis_title='Selected values',
		    yaxis_title='Count',
		    template='plotly_white'
		)


		datahalf["date"] = pd.to_datetime(datahalf["BereitStellDat"])
		datahalf = datahalf.sort_values(by="date")

		# Create a bar chart using Plotly Express
		fig3 = px.bar(
			datahalf, 
			x="date", 
			y="Picks", 
			labels={"date": "Date", "Picks": "Total Pick Values"},
			title="Picks Bar Chart"
		)

		# Update layout to adjust x-axis labels
		fig3.update_layout(
			xaxis_tickformat="%Y-%m-%d", # Format for the date display
			xaxis_tickangle=45           # Rotate x-axis labels by 45 degrees
		)


		# Create a bar chart using Plotly Express
		fig4 = px.bar(
			datahalf, 
			x="date", 
			y="Pallets", 
			labels={"date": "Date", "Picks": "Total Pick Values"},
			title="Pallets Bar Chart"
		)

		# Update layout to adjust x-axis labels
		fig4.update_layout(
			xaxis_tickformat="%Y-%m-%d", # Format for the date display
			xaxis_tickangle=45           # Rotate x-axis labels by 45 degrees
		)

		return ls, ls2 , fig, fig2, fig3, fig4



