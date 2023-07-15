from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RouteViewSet, StationViewSet, TicketViewSet, TrainViewSet


router = DefaultRouter()
router.register(r'routes', RouteViewSet, 'route')
router.register(r'station', StationViewSet, 'station')
router.register(r'ticket', TicketViewSet, 'ticket')
router.register(r'train', TrainViewSet, 'train')
urlpatterns = [

]
urlpatterns += router.urls
