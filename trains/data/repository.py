from datetime import datetime, timedelta
from django.conf import settings
from .models import Route, Station, Ticket, Train


class TrainRepository:
    @staticmethod
    def get_queryset():
        return Train.objects.all()

    @staticmethod
    def get(name):
        return Train.objects.get(name=name)

    @staticmethod
    def get_or_create(name, is_branded):
        train, created = Train.objects.get_or_create(
            name=name,
            is_branded=is_branded
        )
        return train


class StationRepository:
    @staticmethod
    def get_queryset():
        return Station.objects.all()

    @staticmethod
    def get(pk):
        return Station.objects.get(code=pk)

    @staticmethod
    def get_by_name(name):
        return Station.objects.get(name=name)

    @staticmethod
    def get_or_create(code, name):
        station, created = Station.objects.get_or_create(
            code=code,
            name=name
        )
        return station


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

    @staticmethod
    def get_or_create(origin_station: Station,
                      destination_station: Station, departure_datetime, arrival_datetime, train: Train):
        route, created = Route.objects.get_or_create(
            origin_station=origin_station,
            destination_station=destination_station,
            departure_datetime=departure_datetime,
            arrival_datetime=arrival_datetime,
            train=train
        )
        return route


class TicketRepository:
    @staticmethod
    def get_queryset():
        return Ticket.objects.all()

    @staticmethod
    def get_or_create(route: Route, service_class, service_price, finally_price, ml_price, count):
        ticket, created = Ticket.objects.get_or_create(
            route=route,
            service_class=service_class,
            service_price=service_price,
            finally_price=finally_price,
            ml_price=ml_price,
            count_of_bought=count
        )
        return ticket
