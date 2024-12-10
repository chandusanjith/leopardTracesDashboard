# Generated by Django 4.2.1 on 2024-12-10 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("traces", "0006_alter_device_cpu_usage_alter_device_disk_usage_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Forest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("forest_id", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name="leopardtraces",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="leopard_images/"),
        ),
        migrations.AddField(
            model_name="leopardtraces",
            name="viewed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="device",
            name="forest",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="devices",
                to="traces.forest",
            ),
        ),
        migrations.AddField(
            model_name="leopardtraces",
            name="forest",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="leopard_traces",
                to="traces.forest",
            ),
        ),
    ]
