from django.shortcuts import render
from .models import LeopardTraces, Device
import pandas as pd
import plotly.express as px
import plotly.offline as opy
from dash import dash_table
from django_plotly_dash import DjangoDash
import dash_html_components as html
from datetime import datetime, timedelta, timezone

# Create your views here.
def LoadPage(request):
    leopard_traces = LeopardTraces.objects.all()
    data = list(leopard_traces.values())

    # Create a DataFrame from the list of dictionaries
    leopard_df = pd.DataFrame(data)
    if leopard_df.empty:
        return render(request, 'Main.html')
    leopard_df['lat'] = leopard_df['lat'].astype(float)
    leopard_df['long'] = leopard_df['long'].astype(float)

    device_traces = Device.objects.all()
    data = list(device_traces.values())

    # Create a DataFrame from the list of dictionaries
    device_df = pd.DataFrame(data)
    if device_df.empty:
        return render(request, 'Main.html')
    # Define the current time
    now = datetime.now(timezone.utc)

    # Define the threshold for activity (5 minutes)
    threshold = timedelta(minutes=5)
    device_df["last_active_on"] = pd.to_datetime(device_df['last_active_on'], utc=True)

    # Add the device_status column
    device_df["device_status"] = device_df["last_active_on"].apply(lambda x: "active" if now - x < threshold else "not active")

    context = {}


    fig = px.scatter_mapbox(leopard_df, lat="lat", lon="long", hover_name="area_code", hover_data=["type", "area_code", "confidence"],
                            color_discrete_sequence=["fuchsia"], zoom=3, height=600)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    div = opy.plot(fig, auto_open=False, output_type='div')

    context['graph'] = div

    app = DjangoDash('SimpleExample')

    app.layout = html.Div([
        html.Div([
            dash_table.DataTable(
                id='table1',
                columns=[{"name": i, "id": i} for i in leopard_df.columns],
                data=leopard_df.to_dict('records'),
                filter_action='native',
                sort_action='native',
                sort_mode='multi',
                page_size=20,
                style_table={'overflowY': 'auto'},
            )
        ]),
        html.Br(),  # Add a break between tables for spacing
        html.Div([
            dash_table.DataTable(
                id='table2',
                columns=[{"name": i, "id": i} for i in device_df.columns],
                data=device_df.to_dict('records'),
                filter_action='native',
                sort_action='native',
                sort_mode='multi',
                page_size=20,
                style_table={'overflowY': 'auto'},
            )
        ])
    ])
    context['leopard_traces'] = leopard_traces
    context['leopard_traces_count'] = leopard_traces.count()
    context['devices_count'] = device_df.shape[0]
    context['regions_monitored'] = len(list(set(leopard_df['area_code'].to_list())))


    return render(request, 'Main.html', context)
