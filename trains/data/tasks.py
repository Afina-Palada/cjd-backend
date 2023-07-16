import datetime
import datetime as dt
import json

import pytz
from django.conf import settings
import requests

from .repository import TrainRepository, TicketRepository, StationRepository, RouteRepository
from trains.celery import app


@app.task
def get_routes_and_tickets_from_api(origin_code, destination_code):
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}
    start_date = dt.datetime(day=17, month=7, year=2023, tzinfo=pytz.timezone(settings.TIME_ZONE))

    date = start_date
    for i in range(110):
        print(date.strftime(settings.DATE_FORMAT))
        response = requests.post(
            url='https://ticket.rzd.ru/apib2b/p/Railway/V1/Search/TrainPricing',
            headers=headers,
            data=json.dumps({
                "Origin": origin_code,
                "Destination": destination_code,
                "DepartureDate": date.strftime(settings.DATE_FORMAT),
                "TimeFrom": 0,
                "TimeTo": 24,
                "CarGrouping": "DontGroup",
                "GetByLocalTime": True,
                "SpecialPlacesDemand": "StandardPlacesAndForDisabledPersons"
            }),
            cookies={
                "lang": "ru",
                "ClientUid": "0lzBiSK77q6deGg9pxREshrc67UASRvj",
                "AuthFlag": "false",
                "session-cookie": "1771cf7608fe3e4e91cb122e18991a24551fbadae6a82f0d549344302e90eff5840f2cf27c31357e472f90cee236fa7d"
            }
        )
        data = response.json()
        print(data)
        trains = data['Trains']
        for train in trains:
            train_obj = TrainRepository.get_or_create(train['TrainNumber'], train['IsBranded'])
            origin_station_json = train['OriginStationInfo']
            destination_station_json = train['DestinationStationInfo']
            station_origin = StationRepository.get_or_create(origin_station_json['StationCode'], origin_station_json['StationName'])
            station_destination = StationRepository.get_or_create(destination_station_json['StationCode'], destination_station_json['StationName'])
            route = RouteRepository.get_or_create(station_origin, station_destination, train["DepartureDateTime"], train["ArrivalDateTime"], train_obj)
            cars = train.get('CarGroups')
            if cars:
                for car in cars:
                    if car.get('MinPrice'):
                        if car["ServiceClasses"] != '':
                            print(type(route.departure_datetime), type(date))
                            req_data = {
                                    'days_to_departure': (datetime.datetime.strptime(train["DepartureDateTime"], settings.DATE_FORMAT).astimezone(pytz.timezone(settings.TIME_ZONE)) - date).days,
                                    'service_class': car['ServiceClasses'],
                                    'count_tickets': 1,
                                    'service_price': car['ServiceCosts'][0],
                                    'trip': train["TripDistance"]
                                }
                            ml_price = float(requests.get(settings.TRAINS_ANALYTIC_SERVICE_URL,
                                             params=req_data).text)
                            surge_coefficient = requests.get(settings.TRAINS_SURGE_SERVICE_URL, params={
                                'origin': origin_code,
                                'destination': destination_code
                            }).text

                            ml_price *= float(surge_coefficient)
                            ticket = TicketRepository.get_or_create(
                                route=route,
                                service_class=car['ServiceClasses'][0],
                                service_price=car['ServiceCosts'][0],
                                finally_price=car["MinPrice"],
                                ml_price=ml_price,
                                count=0
                            )
        date += dt.timedelta(days=1)
