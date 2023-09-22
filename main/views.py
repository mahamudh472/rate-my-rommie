from django.shortcuts import render
from roommates.models import UserProfile, Address, SocialMedia, AddressReview, RoommateReview
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'main/index.html')

@login_required(login_url="{% url 'accounts:login' %}")
def profile(request):
    user = UserProfile.objects.get(user=request.user)
    return render(request, 'main/roommatedetails.html', {'userp': user})

@login_required(login_url="{% url 'accounts:login' %}")
def profile_view(request, username):
    user = UserProfile.objects.get(user=User.objects.get(username=username))
    return render(request, 'main/roommatedetails.html', {'userp': user})

@login_required(login_url="{% url 'accounts:login' %}")
def search(request):
    roomate_key = request.GET.get('Roommate', None)
    address_key = request.GET.get('Address', None)
    if roomate_key:
        roommate = request.GET['Roommate']
        current_user = UserProfile.objects.get(user=request.user)
        qs1 = UserProfile.objects.exclude(id=current_user.id).filter(user__username__icontains=roommate)
        qs2 = UserProfile.objects.exclude(id=current_user.id).filter(user__first_name__icontains=roommate)
        qs3 = UserProfile.objects.exclude(id=current_user.id).filter(user__last_name__icontains=roommate)
        roommate_list = qs1 | qs2 | qs3
        total = roommate_list.count()
        
        context = {
            'roommate_list': roommate_list,
            'total': total,
            'keyword': roommate,
            'key': 'Roommate',
            }
        return render(request, 'main/search.html', context)
    if address_key:
        address = request.GET['Address']
        qs1 = Address.objects.filter(name__icontains=address)
        qs2 = Address.objects.filter(location__icontains=address)
        address_list = qs1 | qs2
        total = address_list.count()
        
        context = {
            'address_list': address_list,
            'total': total,
            'keyword': address,
            'key': 'Address',
            }
        return render(request, 'main/searchaddress.html', context)
    return render(request, 'main/search.html')

@login_required(login_url="{% url 'accounts:login' %}")
def add_address(request):
    if request.method == "POST":
        name = request.POST['address-name']
        location = request.POST['address-location']
        description = request.POST['description']
        photo = request.FILES['picture__input']
        total_roommates = request.POST['total-roommates']
        address = Address(name=name, location=location, description=description, photo=photo, total_roommates=total_roommates)
        address.save()
        messages.success(request, 'Address added successfully')
        return render(request, 'main/addaddress.html')
    return render(request, 'main/addaddress.html')

@login_required(login_url="{% url 'accounts:login' %}")
def edit_profile(request):
    user = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        user.full_name = request.POST['full-name']
        user.phone = request.POST['phone']
        user.mobile = request.POST['mobile']
        user.address = request.POST['address']
        user.photo = request.FILES['picture__input']
        user.save()
        messages.success(request, 'Profile updated successfully')
        return render(request, 'main/roommatedetails.html', {'user': user})
    return render(request, 'main/editprofile.html', {'user': user})

@login_required(login_url="{% url 'accounts:login' %}")
def edit_social(request):
    user = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        user.socialmedia.website = request.POST['website']
        user.socialmedia.github = request.POST['github']
        user.socialmedia.twitter = request.POST['twitter']
        user.socialmedia.instagram = request.POST['instagram']
        user.socialmedia.facebook = request.POST['facebook']
        user.socialmedia.save()
        messages.success(request, 'Social media updated successfully')
        return render(request, 'main/roommatedetails.html', {'user': user})
    return render(request, 'main/editsocial.html', {'user': user})

@login_required(login_url="{% url 'accounts:login' %}")
def address_view(request, pk):
    address = Address.objects.get(id=pk)
    # reviews = address.addressreview_set.all()
    return render(request, 'main/addressdetails.html', {'address': address})

@login_required(login_url="{% url 'accounts:login' %}")
def address_add_review(request, pk):
    address = Address.objects.get(id=pk)
    if request.method == "POST":
        address.addressreview_set.create(author=request.user, text=request.POST['review'], rating=request.POST['rate'])
        messages.success(request, 'Review added successfully')
        return render(request, 'main/addressdetails.html', {'address': address})
    return render(request, 'main/addreview.html', {'address': address})