from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

handler404 = 'views.error_404'

router = routers.DefaultRouter()
router.register(r'ticks', TickView)


urlpatterns = [
    path('tests/', include(router.urls)),
    path('tick-sightings/time/', TickGetTimeView.as_view()),
    path('tick-sightings/location/<str:location>/', TickGetLocationView.as_view()),
    path('statistics/sightings-per-region', get_sightings_per_region, name='statistics-sightings-per-region'),
    path('statistics/trends/monthly', get_change_over_months, name='statistics-change-over-time')
]
