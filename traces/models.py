from django.db import models

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    device_name = models.CharField(max_length=100, unique=True)
    cpu_usage = models.CharField(max_length=100)
    memory_usage = models.CharField(max_length=100)
    disk_usage = models.CharField(max_length=100)
    temperature = models.CharField(max_length=100)
    last_active_on = models.DateTimeField()

    def __str__(self):
        return "{}-{}".format(self.device_id, self.device_name)

class LeopardTraces(models.Model):
    type = models.TextField(default=1)
    lat = models.TextField(default=1)
    long = models.TextField(default=1)
    area_code = models.TextField(default="n/a")
    confidence = models.TextField(default="n/a")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='leopard_traces', null=True, blank=True)
    traced_on = models.DateTimeField()
    viewed = models.BooleanField(default=False)
    image = models.ImageField(upload_to='leopard_images/', null=True, blank=True)  # New image field

    def __str__(self):
        return "{}-{}".format(self.lat, self.area_code)
