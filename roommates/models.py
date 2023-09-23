from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile_photos', blank=True)

    def __str__(self):
        return self.user.username

class SocialMedia(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    website = models.CharField(max_length=20, null=True, blank=True)
    github = models.CharField(max_length=20, null=True, blank=True)
    twitter = models.CharField(max_length=20, null=True, blank=True)
    instagram = models.CharField(max_length=20, null=True, blank=True)
    facebook = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.full_name

class Address(models.Model):
    name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='address_photos', blank=True)
    total_roommates = models.IntegerField(default=0)

    def average_rating(self):
        if self.addressreview_set.count() == 0:
            return 0
        else:
            total = 0
            for review in self.addressreview_set.all():
                total += review.rating
            return round(total / self.addressreview_set.count(), 1)
    def __str__(self):
        return self.name

class AddressReview(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class RoommateReview(models.Model):
    roommate = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
class Attribute(models.Model):
    author = models.ManyToManyField(UserProfile, blank=True)
    review = models.ManyToManyField(RoommateReview, blank=True)
    name = models.CharField(max_length=100, blank=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name