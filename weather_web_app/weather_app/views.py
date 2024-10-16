import requests
from django.shortcuts import render, redirect
from decouple import config
from .models import City
from .forms import CityForm
# Create your views here.

api_key = config('OPENWEATHER_API_KEY')

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            if City.objects.filter(name=city_name).exists():
                form.add_error('name', 'City already exists in the database.')
            else:
                form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city,api_key)).json()

        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon']
        }

        weather_data.append(weather)

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')