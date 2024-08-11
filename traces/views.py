from django.shortcuts import render
from .models import LeopardTraces, Device
import pandas as pd
import plotly.express as px
import plotly.offline as opy
from datetime import datetime, timedelta, timezone
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
def LoadPage(request):
    leopard_traces = LeopardTraces.objects.all()
    data = list(leopard_traces.values())
    context = {}

    # Paginate the leopard traces
    paginator = Paginator(leopard_traces, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['leopards'] = page_obj

    # Create a DataFrame from the list of dictionaries
    leopard_df = pd.DataFrame(data)
    df = leopard_df.groupby(['type', 'area_code', 'lat', 'long']).size().reset_index(name='occurrence_count')

    # Create the bubble map
    fig = px.scatter_geo(df,
                         lat='lat',
                         lon='long',
                         text='area_code',  # Labels on the map
                         size='occurrence_count',  # Size of bubbles
                         scope='asia',
                         # title='Bubble Map of Maharashtra Cities',
                         center={'lat': 19.7515, 'lon': 75.7139},  # Center on Maharashtra
                         size_max=50,  # Maximum size of bubbles
                         height= 420
                         )

    # Update layout for a better map visualization
    fig.update_geos(
        visible=True,
        resolution=50,  # Higher resolution
        showcountries=True, countrycolor="Black",  # Country borders
        showsubunits=True, subunitcolor="Blue",  # Subunit borders (state/province)
        showcoastlines=True, coastlinecolor="Black",  # Coastlines
        showland=True, landcolor="lightgray",
        showocean=True, oceancolor="lightblue",
        showrivers=True, rivercolor="Blue",  # Rivers
        showlakes=True, lakecolor="Blue"  # Lakes
    )

    fig.update_layout(
        title=dict(x=0.5),  # Center title
        geo=dict(projection_scale=5)  # Zoom level
    )

    div = opy.plot(fig, auto_open=False, output_type='div')
    leopard_df = leopard_df.groupby(['type', 'area_code']).size().reset_index(name='occurrence_count')
    context['leopard_df_json'] = leopard_df.to_json(orient='records')

    context['graph'] = div

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

    context['leopard_traces'] = leopard_traces
    context['leopard_traces_count'] = leopard_traces.count()
    context['devices_count'] = device_df.shape[0]
    context['regions_monitored'] = len(list(set(leopard_df['area_code'].to_list())))
    context['devices'] = data


    return render(request, 'home/index.html', context)


def get_notifications(request):
    # Fetch the top 10 notifications ordered by the latest timestamp
    notifications = LeopardTraces.objects.filter(viewed=False).order_by('-traced_on')[:10]

    # Serialize the notifications into a JSON-friendly format
    notifications_data = [
        {'message': f"Leopard was detected on {n.traced_on.strftime('%Y-%m-%d %H:%M:%S')}, Area: {n.area_code}", 'timestamp': n.traced_on.strftime('%Y-%m-%d %H:%M:%S')}
        for n in notifications
    ]

    return JsonResponse(notifications_data, safe=False)
