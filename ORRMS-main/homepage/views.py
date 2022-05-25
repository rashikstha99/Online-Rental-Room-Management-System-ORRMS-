from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from add_property.models import PropertyRoom, PropertyFlat



def home_page(request):
        property_flat = PropertyFlat.objects.all()[:3]
        property_room = PropertyRoom.objects.all()[:3]
        return render(request,'homepage.html', {'property_flat': property_flat, 'property_room': property_room})
