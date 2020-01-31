from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    url="http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=00a0fa55c42f1467762889f0f648fea1"
    cities = City.objects.all()
    if request.method=='POST':
        form=CityForm(request.POST)
        form.save()
    form=CityForm()
    for city in cities:
        city_weather = requests.get(url.format(city)).json() 
        weather_data=[]
        for city in cities:
            city_weather=requests.get(url.format(city)).json()
            try:
                weather={
                    'city':city,
                    'temperature': round((city_weather['main']['temp'] - 32) * 5.0/9.0,2),
                    'description':city_weather['weather'][0]['description'],
                    'icon':city_weather['weather'][0]['icon']
                }
            except:
                print('Invalid City')
                continue
            weather_data.append(weather)
    context={'weather_data':weather_data,'form':form}
    return render(request,'weather/index.html',context)