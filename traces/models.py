from django.db import models

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    device_name = models.CharField(max_length=100, unique=True)
    last_active_on = models.DateTimeField()

    def __str__(self):
        return "{}-{}".format(self.device_id, self.device_name)

class LeopardTraces(models.Model):
    lat = models.TextField(default=1)
    long = models.TextField(default=1)
    place = models.TextField(default="n/a")
    description = models.TextField(default="n/a")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='leopard_traces', null=True, blank=True)
    traced_on = models.DateTimeField()

    def __str__(self):
        return "{}-{}".format(self.lat, self.place)
