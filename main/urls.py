from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>', views.profile_view, name="profile_view"),
    path('search/', views.search, name='search'),
    path('addaddress/', views.add_address, name='add_address'),
    path('address/<int:pk>', views.address_view, name='address_view'),
    path('address-add-review/<int:pk>', views.address_add_review, name='address_add_review'),
    path('edit-profile', views.edit_profile, name="edit-profile"),
    path('roommate-add-review/<int:pk>', views.roommate_add_review, name='roommate_add_review'),
] 