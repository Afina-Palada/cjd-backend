from datetime import datetime, timedelta
from django.conf import settings
from .models import Route, Station, Ticket, Train


class TrainRepository:
    @staticmethod
    def get_queryset():
        return Train.objects.all()


class StationRepository:
    @staticmethod
    def get_queryset():
        return Station.objects.all()

    @staticmethod
    def get_by_name(name):
        return Station.objects.get(name=name)


class RouteRepository:
    @staticmethod
    def get_queryset():
        return Route.objects.all()

    @staticmethod
    def get(pk):
        return Route.objects.get(pk=pk)

    @staticmethod
    def get_filtered_route(origin_station, destination_station, departure_datetime):
        return Route.objects.filter(
            origin_station=StationRepository.get_by_name(origin_station),
            destination_station=StationRepository.get_by_name(destination_station),
            departure_datetime__gte=departure_datetime,
            departure_datetime__lt=datetime.strptime(departure_datetime, settings.DATE_FORMAT) + timedelta(days=1)
        )


class TicketRepository:
    @staticmethod
    def get_queryset():
        return Ticket.Objects.all()

    @staticmethod
    def get_available_tickets_by_route(query_params):
        route_id = query_params['route_id']
        return Ticket.objects.filter(route=RouteRepository.get(pk=route_id), is_bought=False)
