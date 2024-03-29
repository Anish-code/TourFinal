# Generated by Django 5.0 on 2024-02-28 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trek', models.CharField(max_length=100)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time', models.CharField(max_length=50)),
                ('trip_grade', models.CharField(default='moderate', max_length=50)),
                ('max_altitude', models.PositiveIntegerField()),
                ('accommodation', models.CharField(max_length=100)),
                ('best_travel_time', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=100)),
            ],
        ),
    ]
