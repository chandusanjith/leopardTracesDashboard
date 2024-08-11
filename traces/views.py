from django.shortcuts import render
from .models import LeopardTraces, Device
import pandas as pd
import plotly.express as px
import plotly.offline as opy
from datetime import datetime, timedelta, timezone
from django.core.paginator import Paginator

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
    leopard_df = leopard_df.groupby(['type', 'area_code']).size().reset_index(name='occurrence_count')
    context['leopard_df_json'] = leopard_df.to_json(orient='records')

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
