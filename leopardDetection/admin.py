from django.contrib import admin
from traces.models import LeopardTraces, Device

from django.apps import apps

class DynamicModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = [field.name for field in model._meta.get_fields() if field.concrete]

# Register models using the dynamic admin
class LeopardTracesAdmin(DynamicModelAdmin):
    pass

class DeviceAdmin(DynamicModelAdmin):
    pass

# Assuming your app is named 'myapp'
admin.site.register(apps.get_model('traces', 'LeopardTraces'), LeopardTracesAdmin)
admin.site.register(apps.get_model('traces', 'Device'), DeviceAdmin)