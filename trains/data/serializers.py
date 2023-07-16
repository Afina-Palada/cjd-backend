from rest_framework import serializers

from .models import Route, Station, Ticket, Train
from .repository import RouteRepository, StationRepository


class TrainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Train
        fields = '__all__'


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    origin_station = serializers.PrimaryKeyRelatedField(queryset=StationRepository.get_queryset())
    destination_station = serializers.PrimaryKeyRelatedField(queryset=StationRepository.get_queryset())
    train = serializers.StringRelatedField()

    class Meta:
        model = Route
        fields = ('origin_station', 'destination_station', 'train', 'departure_datetime', 'arrival_datetime')


class TicketSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=RouteRepository.get_queryset())

    class Meta:
        model = Ticket
        fields = ('route', 'service_class', 'service_price', 'finally_price', 'ml_price', 'count_of_bought')


class GetRouteSerializer(serializers.ModelSerializer):
    origin_station = StationSerializer()
    destination_station = StationSerializer()
    train = TrainSerializer(required=False)
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ('pk', 'origin_station', 'destination_station', 'train', 'departure_datetime', 'arrival_datetime', 'tickets')
