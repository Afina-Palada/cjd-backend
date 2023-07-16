from django.db import models

# Create your models here.


class Train(models.Model):
    name = models.CharField(max_length=8, primary_key=True)
    is_branded = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Station(models.Model):
    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=64)


class Route(models.Model):
    origin_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='origin_station')
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination_station')
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    train = models.ForeignKey(Train, on_delete=models.SET_NULL, null=True)


class Ticket(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    service_class = models.CharField(max_length=8)
    service_price = models.FloatField()
    finally_price = models.FloatField()
    ml_price = models.FloatField()
    count_of_bought = models.IntegerField()
