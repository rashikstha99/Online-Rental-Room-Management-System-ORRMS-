from django import forms
from django.contrib.gis import forms
from django.forms import Textarea
from .models import PropertyFlat, PropertyRoom, Location, FlatImage, RoomImage, CommentsFlat, CommentsRoom


class CommentsFlatForm(forms.ModelForm):
    class Meta:
        model = CommentsFlat
        fields = ('body',)

        widgets = {
            'body': Textarea(attrs={'cols': 80, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentsFlatForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = False


class CommentsRoomForm(forms.ModelForm):
    class Meta:
        model = CommentsRoom
        fields = ('body',)

        widgets = {
            'body': Textarea(attrs={'cols': 80, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentsRoomForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = False


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"


class AddFlatForm(forms.ModelForm):
    class Meta:
        model = PropertyFlat
        fields = (
        'bedroom_no', 'kitchen_no', 'livingroom_no', 'bathroom_no', 'water_facility', 'electricity', 'Parking_facility',
        'short_description', 'price', 'coordinates', 'phone_number')
        widgets = {
            'short_description': Textarea(attrs={'cols': 80, 'rows': 3}),
            'coordinates': forms.OSMWidget(attrs={'map_width': 450, 'map_height': 300})
        }
        labels = {
            'bedroom_no': 'Numbers of Bedrooms',
            'kitchen_no': 'Numbers of Kitchen',
            'livingroom_no': 'Number of Living Rooms',
            'bathroom_no': 'Numbers of Bathrooms',
            'water_facility': 'Water Availability',
            'electricity': 'Electricity Availability',
            'Parking_facility': 'Parking Availability',
            'short_description': 'Short Description',
            'phone_number': 'Contact Number',

        }


class AddRoomForm(forms.ModelForm):
    class Meta:
        model = PropertyRoom
        fields = (
        'price', 'size', 'water_facility', 'electricity', 'Parking_facility', 'short_description', 'coordinates',
        'phone_number')
        widgets = {
            'short_description': Textarea(attrs={'cols': 80, 'rows': 3}),
            'coordinates': forms.OSMWidget(attrs={'map_width': 450, 'map_height': 300})
        }
        labels = {
            'size': 'Size of Room',
            'water_facility': 'Water Availability',
            'electricity': 'Electricity Availability',
            'Parking_facility': 'Parking Availability',
            'short_description': 'Short Description',
            'phone_number': 'Contact Number',
        }


class FlatImageForm(forms.ModelForm):
    class Meta:
        model = FlatImage
        fields = ('livingroom_img', 'bedroom_img', 'kitchen_img', 'bathroom_img')
        labels = {
            'livingroom_img': 'Living Room',
            'bedroom_img': 'Bedroom',
            'kitchen_img': 'Kitchen',
            'bathroom_img': 'Bathroom',
        }


class RoomImageForm(forms.ModelForm):
    class Meta:
        model = RoomImage
        fields = "__all__"
        labels = {
            'room_img': 'Room Image'
        }
