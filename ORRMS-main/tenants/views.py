from django.shortcuts import render, redirect
from add_property.models import PropertyFlat, Location, FlatImage, PropertyRoom, RoomImage
from .form import WatchlistForm
from .models import Watchlist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q


@login_required
def watchlist_delete(request, id):
    watchlist = Watchlist.objects.get(pk=id)
    watchlist.delete()
    return redirect('watchlist')


@login_required
def clear_watchlist(request, id):
    watchlist = Watchlist.objects.filter(user_id=id)
    for watch in watchlist:
        watch.date_added = datetime.now()
        watch.save()
    return redirect('watchlist')


@login_required
def watchlist(request):
    if request.method == 'POST':
        watchlist_form = WatchlistForm(request.POST)
        if watchlist_form.is_valid():
            watchlist_form = watchlist_form.save(commit=False)
            watchlist_form.user = request.user
            watchlist_form.save()
        messages.success(request, 'Watchlist added successfully')
        return redirect('watchlist')

    else:
        all_location = Location.objects.all()
        user = request.user.id
        watchlist_location = Watchlist.objects.filter(user_id=user)
        total = Location.objects.none()
        total_room = Location.objects.none()
        total_flat = Location.objects.none()
        for loc in all_location:
            for watch_loc in watchlist_location:
                if loc.state == watch_loc.state and loc.district == watch_loc.district and loc.ward_no == watch_loc.ward_no and watch_loc.property_type == 'R':
                    watchlist = PropertyRoom.objects.all().filter(
                        Q(location__state__iexact=watch_loc.state) &
                        Q(location__district__iexact=watch_loc.district) &
                        Q(location__municipality__iexact=watch_loc.municipality) &
                        Q(location__date_added__gte=watch_loc.date_added)
                    ).order_by('-date_added')

                    total_room = total | watchlist

                elif loc.state == watch_loc.state and loc.district == watch_loc.district and loc.ward_no == watch_loc.ward_no and watch_loc.property_type == 'F':
                    watchlist = PropertyFlat.objects.all().filter(
                        Q(location__state__iexact=watch_loc.state) &
                        Q(location__district__iexact=watch_loc.district) &
                        Q(location__municipality__iexact=watch_loc.municipality) &
                        Q(location__date_added__gte=watch_loc.date_added)
                    ).order_by('-date_added')

                    total_flat = total | watchlist

        if total_room or total_flat:
            property_list = Watchlist.objects.filter(user_id=user)
            return render(request, 'watchlist.html',
                          {'total_flat': total_flat, 'total_room': total_room, 'property_list': property_list})
        else:
            property_list = Watchlist.objects.filter(user_id=user)
            empty_watchlist = 'There are no property in your watchlist'
            return render(request, 'watchlist.html',
                          {'empty_watchlist': empty_watchlist, 'property_list': property_list})


def rent_view(request):
    property_flat = PropertyFlat.objects.all().order_by('-date_added')[:12]
    property_room = PropertyRoom.objects.all().order_by('-date_added')[:12]
    return render(request, 'rent_view.html', {'property_flat': property_flat, 'property_room': property_room})


def search(request):
    search_request = request.POST.get('search', False)
    if search_request:
        first = search_request[1:len(search_request)]
        first_half = search_request[0:len(search_request) // 2]
        second_half = search_request[len(search_request) // 2:]
        match = PropertyFlat.objects.all().filter(
            Q(price__icontains=search_request) |
            Q(location__state__icontains=search_request) |
            Q(location__district__icontains=search_request) |
            Q(price__icontains=first) |
            Q(location__state__icontains=first) |
            Q(location__district__icontains=first)
        ).order_by('-date_added')

        match_extra = PropertyFlat.objects.all().filter(
            Q(price__icontains=first_half) |
            Q(location__state__icontains=first_half) |
            Q(location__district__icontains=first_half) |
            Q(price__icontains=second_half) |
            Q(location__state__icontains=second_half) |
            Q(location__district__icontains=second_half)
        ).order_by('-date_added')

        if match:
            return render(request, 'search_result.html', {'searched_flat': match})

        elif match_extra:
            return render(request, 'search_result.html', {'searched_flat': match_extra})

        else:
            watchlist_form = WatchlistForm()
            match = PropertyFlat.objects.all().order_by('-date_added')[:8]
            error = 'No result found !'
            return render(request, 'search_result.html',
                          {'error': error, 'error_view_flat': match, 'watchlist_form': watchlist_form})

    elif search_request == '' or search_request == 'None':
        return redirect('/')

    else:
        price = request.POST.get('price', False)
        state = request.POST.get('state', False)
        district = request.POST.get('district', False)
        property = request.POST.get('property', False)
        if price == '' and state == '' and district == '':
            return redirect('/')

        else:
            if property == 'room':
                match = PropertyRoom.objects.all().filter(
                    Q(price__icontains=price) &
                    Q(location__state__icontains=state) &
                    Q(location__district__icontains=district)
                ).order_by('-date_added')
                if match:
                    return render(request, 'search_result.html', {'searched_room': match})
                else:
                    watchlist_form = WatchlistForm()
                    match = PropertyRoom.objects.all().order_by('-date_added')[:8]
                    error = 'No result found !'

                    return render(request, 'search_result.html',
                                  {'error': error, 'error_view_room': match, 'watchlist_form': watchlist_form})

            else:
                match = PropertyFlat.objects.all().filter(
                    Q(price__icontains=price) &
                    Q(location__state__icontains=state) &
                    Q(location__district__icontains=district)
                ).order_by('-date_added')
                if match:
                    return render(request, 'search_result.html', {'searched_flat': match})
                else:
                    watchlist_form = WatchlistForm()
                    match = PropertyFlat.objects.all().order_by('-date_added')[:8]
                    error = 'No result found !'

                    return render(request, 'search_result.html',
                                  {'error': error, 'error_view_flat': match, 'watchlist_form': watchlist_form})
