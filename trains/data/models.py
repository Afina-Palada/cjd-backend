from django.db import models

# Create your models here.


class Train(models.Model):
    name = models.CharField(max_length=8)
    is_branded = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Station(models.Model):
    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=64)


class Route(models.Model):
    origin_station = models.ForeignKey(Station, on_delete=models.CASCADE)
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    train = models.ForeignKey(Train, on_delete=models.SET_NULL, null=True)


class Ticket(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    service_class = models.CharField(max_length=8)
    service_price = models.FloatField()
    finally_price = models.FloatField()
    bought = models.BooleanField(default=False)
