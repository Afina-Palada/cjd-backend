from rest_framework import serializers

from .models import Route, Station, Ticket, Train


class TrainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Train
        fields = '__all__'


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    origin_station = serializers.PrimaryKeyRelatedField()
    destination_station = serializers.PrimaryKeyRelatedField()
    train = serializers.StringRelatedField()

    class Meta:
        model = Route
        fields = ('origin_station', 'destination_station', 'train', 'departure_datetime', 'arrival_datetime')


class TicketSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Ticket
        fields = ('route', 'service_class', 'service_price', 'finally_price', 'is_bought')


class GetRouteSerializer(serializers.ModelSerializer):
    origin_station = StationSerializer()
    destination_station = StationSerializer()
    train = TrainSerializer(required=False)
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ('origin_station', 'destination_station', 'train', 'departure_datetime', 'arrival_datetime')
