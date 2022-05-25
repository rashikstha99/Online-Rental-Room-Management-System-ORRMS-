from django.contrib.auth.models import User
from django.contrib.gis.db import models

class Location(models.Model):
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    ward_no = models.IntegerField()
    date_added = models.DateTimeField('date published', auto_now_add=True)

    def natural_keys(self):
        return self.location

    def __str__(self):
        return "%s %s %s" % (self.state, self.district, self.municipality)


class FlatImage(models.Model):
    bedroom_img = models.ImageField(max_length=255)
    kitchen_img = models.ImageField(max_length=255)
    bathroom_img = models.ImageField(max_length=255)
    livingroom_img = models.ImageField(max_length=255)
    date_added = models.DateTimeField('date published', auto_now_add=True)

class RoomImage(models.Model):
    room_img = models.ImageField(max_length=255)
    date_added = models.DateTimeField('date published', auto_now_add=True)

class PropertyRoom(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_images = models.OneToOneField(RoomImage, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    price = models.IntegerField()
    size = models.DecimalField(max_digits=5, decimal_places=2)
    water_facility = models.BooleanField(default=False)
    electricity = models.BooleanField(default=False)
    Parking_facility = models.BooleanField(default=False)
    short_description = models.TextField(max_length=190)
    coordinates = models.PointField(geography=True)
    date_added = models.DateTimeField('date published', auto_now_add=True)


class PropertyFlat(models.Model):
    flat_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    flat_images = models.OneToOneField(FlatImage, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    price = models.IntegerField()
    bedroom_no = models.IntegerField()
    kitchen_no = models.IntegerField()
    bathroom_no = models.IntegerField()
    livingroom_no = models.IntegerField()
    water_facility = models.BooleanField(default=False)
    electricity = models.BooleanField(default=False)
    Parking_facility = models.BooleanField(default=False)
    short_description = models.TextField(max_length=190)
    coordinates = models.PointField(geography=True)
    date_added = models.DateTimeField('date published', auto_now_add=True)


class CommentsFlat(models.Model):
    flat = models.ForeignKey(PropertyFlat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "%s %s" % (self.user, self.body)


class CommentsRoom(models.Model):
    room = models.ForeignKey(PropertyRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "%s %s" % (self.user, self.body)
