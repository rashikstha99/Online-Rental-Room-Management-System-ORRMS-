from django.shortcuts import render, redirect
from .forms import AddFlatForm, AddRoomForm, LocationForm, FlatImageForm, RoomImageForm, CommentsFlatForm, CommentsRoomForm
from .models import PropertyFlat, PropertyRoom, Location, FlatImage, RoomImage, CommentsFlat, CommentsRoom
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponse
from django.contrib.auth.models import User


def location_flat(request):
    locationDataFlat = serialize('geojson', PropertyFlat.objects.all())
    return HttpResponse(locationDataFlat, content_type='geojson')


def location_room(request):
    locationDataRoom = serialize('geojson', PropertyRoom.objects.all())
    return HttpResponse(locationDataRoom, content_type='geojson')


def location_single_flat(request, id):
    locationSingle = serialize('geojson', PropertyFlat.objects.all().filter(flat_id=id))
    return HttpResponse(locationSingle, content_type='geojson')


def location_single_room(request, id):
    locationSingle = serialize('geojson', PropertyRoom.objects.all().filter(pk=id))
    return HttpResponse(locationSingle, content_type='geojson')



@login_required
def flat_delete(request, id):
    property = PropertyFlat.objects.get(pk=id)
    location = Location.objects.get(pk=property.location_id)
    images = FlatImage.objects.get(pk=property.flat_images_id)
    property.delete()
    location.delete()
    images.delete()
    return redirect('property_list' ,id = request.user.id)

@login_required
def room_delete(request, id):
    property = PropertyRoom.objects.get(pk=id)
    location = Location.objects.get(pk=property.location_id)
    images = RoomImage.objects.get(pk=property.room_images_id)
    property.delete()
    location.delete()
    images.delete()
    return redirect('property_list' ,id = request.user.id)


@login_required
def flat_details(request, id):
    if request.method == "POST":
        property = PropertyFlat.objects.get(pk=id)
        comment_form = CommentsFlatForm(request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.user = request.user
            comment_form.flat = property
            comment_form.save()
        return redirect('property_details', id=id)
    else:
        property = PropertyFlat.objects.get(pk=id)
        comment_form = CommentsFlatForm()
        context = {'property_list': PropertyFlat.objects.all().filter(pk=id),
                    'image_list': FlatImage.objects.all().filter(pk=property.flat_images_id),
                    'comment_list': CommentsFlat.objects.all().filter(flat_id=id).order_by('-date_added'),
                    'comment_form': comment_form,
                    'flat_list':PropertyFlat.objects.all().order_by('-date_added')[:4]
                    }
        return render(request, 'property_details.html', context)


@login_required
def room_details(request, id):
    if request.method == "POST":
        property = PropertyRoom.objects.get(pk=id)
        comment_form = CommentsRoomForm(request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.user = request.user
            comment_form.room = property
            comment_form.save()
        return redirect('room_details', id=id)
    else:
        property = PropertyRoom.objects.get(pk=id)
        comment_form = CommentsRoomForm()
        context = {'property_list': PropertyRoom.objects.all().filter(pk=id),
                   'location_list': Location.objects.all().filter(pk=property.location_id),
                   'image_list': RoomImage.objects.all().filter(pk=property.room_images_id),
                   'comment_list': CommentsRoom.objects.all().filter(room_id=id).order_by('-date_added'),
                   'comment_form': comment_form,
                   'room_list': PropertyRoom.objects.all().order_by('-date_added')[:4]
                   }
        return render(request, 'room_details.html', context)








@login_required
def add_property_flat(request, id=0):
    if request.method == 'POST':
        if id == 0:
            add_flat_form = AddFlatForm(request.POST)
            location_form = LocationForm(request.POST)
            flat_image_form = FlatImageForm(request.POST, request.FILES)
        else:
            property = PropertyFlat.objects.get(pk=id)
            location = Location.objects.get(pk=property.location_id)
            images = FlatImage.objects.get(pk=property.flat_images_id)
            add_flat_form = AddFlatForm(request.POST, instance=property)
            location_form = LocationForm(request.POST, instance=location)
            flat_image_form = FlatImageForm(request.POST, request.FILES, instance=images)

        if add_flat_form.is_valid() and location_form.is_valid() and flat_image_form.is_valid():
            flat_images = flat_image_form.save()
            location = location_form.save()
            flat = add_flat_form.save(commit=False)
            flat.user = request.user
            flat.location = location
            flat.flat_images = flat_images
            flat.save()

        return redirect('property_list' ,id = request.user.id)

    else:
        if id == 0:
            add_flat_form = AddFlatForm()
            location_form = LocationForm()
            flat_image_form = FlatImageForm()
        else:
            property = PropertyFlat.objects.get(pk=id)
            location = Location.objects.get(pk=property.location_id)
            images = FlatImage.objects.get(pk=property.flat_images_id)
            add_flat_form = AddFlatForm(instance=property)
            location_form = LocationForm(instance=location)
            flat_image_form = FlatImageForm(instance=images)

    args = {}
    args['add_flat_form'] = add_flat_form
    args['location_form'] = location_form
    args['flat_image_form'] = flat_image_form
    return render(request, 'add_property_flat.html', args)


@login_required
def add_property_room(request, id=0):
    if request.method == 'POST':
        if id == 0:
            location_form = LocationForm(request.POST)
            add_room_form = AddRoomForm(request.POST)
            room_image_form = RoomImageForm(request.POST, request.FILES)
        else:
            property = PropertyRoom.objects.get(pk=id)
            location = Location.objects.get(pk=property.location_id)
            images = RoomImage.objects.get(pk=property.room_images_id)
            add_room_form = AddRoomForm(request.POST, instance=property)
            location_form = LocationForm(request.POST, instance=location)
            room_image_form = RoomImageForm(request.POST, request.FILES, instance=images)

        if add_room_form.is_valid() and location_form.is_valid() and room_image_form.is_valid():
            room_images = room_image_form.save()
            location = location_form.save()
            room = add_room_form.save(commit=False)
            room.user = request.user
            room.location = location
            room.room_images = room_images
            room.save()

        return redirect('property_list' ,id = request.user.id)

    else:
        if id == 0:
            add_room_form = AddRoomForm()
            location_form = LocationForm()
            room_image_form = RoomImageForm()
        else:
            property = PropertyRoom.objects.get(pk=id)
            location = Location.objects.get(pk=property.location_id)
            images = RoomImage.objects.get(pk=property.room_images_id)
            add_room_form = AddRoomForm(instance=property)
            location_form = LocationForm(instance=location)
            room_image_form = RoomImageForm(instance=images)

    args = {}
    args['add_room_form'] = add_room_form
    args['location_form'] = location_form
    args['room_image_form'] = room_image_form
    return render(request, 'add_property_room.html', args)

