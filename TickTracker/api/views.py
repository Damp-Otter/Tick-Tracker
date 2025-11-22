from django.shortcuts import render, redirect
from django.db.models import Min, Max
from django.views import generic
from django.http import HttpResponse
from datetime import *
from rest_framework import viewsets
from .models import TickModel
from .serializer import TickSerializer
from collections import OrderedDict
from dateutil import rrule

class TickView(viewsets.ModelViewSet):
    queryset = TickModel.objects.all().order_by('date').values()
    serializer_class = TickSerializer

class TickGetTimeView(generic.ListView):
    model = TickModel
    template_name = 'tick_time_list.html'

    def get_queryset(self):
        from_time = self.request.GET.get('from')
        to_time = self.request.GET.get('to')

        if (from_time == None):
            from_time = TickModel.objects.aggregate(Min('date'))['date__min']
        if (to_time == None):
            to_time = TickModel.objects.aggregate(Max('date'))['date__max']

        queryset = TickModel.objects.filter(
            date__range=[from_time, to_time]
            ).order_by('-date')
        return queryset

class TickGetLocationView(generic.ListView):
    model = TickModel
    template_name = 'tick_location_list.html'

    def get_queryset(self):
        location_param = self.kwargs['location']   
        species = self.request.GET.get('species')
        print(species)
        queryset = TickModel.objects.filter(location__icontains=location_param)
        if(species != None):
            queryset = queryset.filter(species__icontains=species)
       
        return queryset

def get_sightings_per_region(request, *args, **kwargs):
    species = request.GET.get('species')
    unique_locations = TickModel.objects.values_list('location', flat=True).distinct()
    ticks = [0] * int(unique_locations.count())
    locations = [""] * int(unique_locations.count())
    i = 0

    tick_set = TickModel.objects.all()

    if(species != None):
        tick_set = tick_set.filter(species__icontains=species)

    for region in unique_locations:
        ticks_in_location = tick_set.filter(location=region).count()
        ticks[i] = int(ticks_in_location)
        locations[i] = str(region)
        i = i + 1
    
    data = {
        'ticks': ticks,
        'locations': locations,
    }
    
    return render(request, 'sightings_per_region.html', data)

def get_change_over_months(request, *args, **kwargs):

    from_time = datetime.strptime(request.GET.get('from'), "%Y-%m-%dT%H:%M:%S")
    to_time = datetime.strptime(request.GET.get('to'), "%Y-%m-%dT%H:%M:%S")
    location = request.GET.get('location')
    species = request.GET.get('species')

    if (from_time == None):
        from_time = TickModel.objects.aggregate(Min('date'))['date__min']
    if (to_time == None):
        to_time = TickModel.objects.aggregate(Max('date'))['date__max']

    tick_set = TickModel.objects.filter(
        date__range=[from_time, to_time]
        ).order_by('date')
    
    if(species != None):
        tick_set = tick_set.filter(species__icontains=species)
    if(location != None):
        tick_set = tick_set.filter(location__icontains=location)

    print(from_time, to_time)

    month_year = []
    month_year_str= []
    for new_month in rrule.rrule(rrule.MONTHLY, dtstart=from_time, until=to_time):
        month_year.append(new_month.strftime('%m') + "," + new_month.strftime('%Y'))
        month_year_str.append(new_month.strftime('%B') + "," + new_month.strftime('%Y'))

    month_year = list(OrderedDict.fromkeys(month_year))
    month_year_str = list(OrderedDict.fromkeys(month_year_str))
    ticks = [0] * int(month_year.__len__())
    i = 0

    for m_y in month_year:
        current_m_y = m_y.split(',')
        ticks_in_location = tick_set.filter(date__month=int(current_m_y[0]), date__year=int(current_m_y[1])).count()
        ticks[i] = int(ticks_in_location)
        month_year[i] = str(month_year[i])
        i = i + 1

    data = {
        'ticks': ticks,
        'month_year': month_year_str,
    }

    return render(request, 'change_over_time.html', data)

def error_404(request, exception):
    return render(request, '404.html', status=404)
    