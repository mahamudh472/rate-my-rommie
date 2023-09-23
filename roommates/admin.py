from django.contrib import admin
from .models import UserProfile, SocialMedia, Address, AddressReview, RoommateReview, Attribute
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(SocialMedia)
admin.site.register(Address)
admin.site.register(AddressReview)
admin.site.register(RoommateReview)
admin.site.register(Attribute)