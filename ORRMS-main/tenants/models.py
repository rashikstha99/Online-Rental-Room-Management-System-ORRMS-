from django.db import models
from django.contrib.auth.models import User

PROPERTY_CHOICES = (
   ('F', 'Flat'),
   ('R', 'Room')
)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    ward_no = models.IntegerField()
    date_added = models.DateTimeField('date published', auto_now_add=True)
    property_type = models.CharField(max_length=12, choices=PROPERTY_CHOICES)
    def __str__(self):
        return "%s %s %s" % (self.state, self.district, self.municipality)
