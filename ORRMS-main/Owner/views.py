from django.shortcuts import render
from add_property.models import PropertyFlat, Location, FlatImage, PropertyRoom, RoomImage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def property_list(request, id):
    flat = PropertyFlat.objects.filter(user_id=id)
    room = PropertyRoom.objects.filter(user_id=id)
    context = {}
    context['flat_list'] = flat
    context['room_list'] = room

    return render(request, 'property_list.html', context)
