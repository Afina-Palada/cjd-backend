from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .repository import *
from .serializers import *

# Create your views here.


class TrainViewSet(ModelViewSet):
    serializer_class = TrainSerializer
    queryset = TrainRepository.get_queryset()
    permission_classes = [AllowAny]


class StationViewSet(ModelViewSet):
    serializer_class = StationSerializer
    queryset = StationRepository.get_queryset()
    permission_classes = [AllowAny]


class RouteViewSet(ModelViewSet):
    serializer_class = RouteSerializer
    queryset = RouteRepository.get_queryset()
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = RouteRepository.get_queryset()
        serializer = GetRouteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = TicketRepository.get_queryset()
    permission_classes = [AllowAny]


class AvailableTicketsListAPIView(ListAPIView):
    def list(self, request, *args, **kwargs):
        return TicketRepository.get_available_tickets_by_route(self.request.query_params)
