from django.shortcuts import render, redirect
from roommates.models import UserProfile, Address, Attribute
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import json
# Create your views here.

def home(request):
    return render(request, 'main/index.html')


def profile(request):
    user = UserProfile.objects.get(user=request.user)
    attributes = Attribute.objects.filter(author=user)
    return render(request, 'main/roommatedetails.html', {'userp': user, 'attributes': attributes})


def profile_view(request, id):
    user = UserProfile.objects.get(id=id)
    all_attributes = Attribute.objects.all()
    attributes = Attribute.objects.filter(author=user)
    return render(request, 'main/roommatedetails.html', {'userp': user, 'attributes': attributes, 'all_attributes': all_attributes})


def search(request):
    roomate_key = request.GET.get('Roommate', None)
    address_key = request.GET.get('Address', None)
    if roomate_key:
        roommate = request.GET['Roommate']
        
        qs1 = UserProfile.objects.filter(user__username__icontains=roommate)
        qs2 = UserProfile.objects.filter(user__first_name__icontains=roommate)
        qs3 = UserProfile.objects.filter(user__last_name__icontains=roommate)
        qs4 = UserProfile.objects.filter(full_name__icontains=roommate)
        roommate_list = qs1 | qs2 | qs3 | qs4
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

def add_roommate(request):
    if request.method == "POST":
        full_name = request.POST['full-name']
        email = request.POST['email']
        phone = request.POST['phone']
        mobile = request.POST['mobile']
        address = request.POST['address']
        photo = request.FILES['picture__input']
        userprofile = UserProfile( full_name=full_name, email=email, phone=phone, mobile=mobile, address=address, photo=photo)
        userprofile.save()
        attributes = request.POST.get('attribute_list', None)
        if attributes:
            for i in json.loads(attributes):
                attr = userprofile.attribute_set.get_or_create(name=i[0], rating=i[1],)[0]
                attr.save()
        messages.success(request, 'Roommate added successfully')
        return render(request, 'main/addroommate.html')
    return render(request, 'main/addroommate.html')

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


def edit_profile(request):
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        mobile = request.POST.get('mobile', None)
        address = request.POST.get('address', None)
        if name:
            request.user.first_name = " ".join(name.split(' ')[:-1])
            request.user.last_name = name.split(' ')[-1]
        if email:
            request.user.email = email
        if phone:
            request.user.userprofile.phone = phone
        if mobile:
            request.user.userprofile.mobile = mobile
        if address:
            request.user.userprofile.address = address
        request.user.save()
        request.user.userprofile.save()
        
        website = request.POST.get('website', None)
        github = request.POST.get('github', None)
        twitter = request.POST.get('twitter', None)
        instagram = request.POST.get('instagram', None)
        facebook = request.POST.get('facebook', None)
        if website:
            request.user.userprofile.socialmedia.website = website
        if github:
            request.user.userprofile.socialmedia.github = github
        if twitter:
            request.user.userprofile.socialmedia.twitter = twitter
        if instagram:
            request.user.userprofile.socialmedia.instagram = instagram
        if facebook:
            request.user.userprofile.socialmedia.facebook = facebook
        request.user.userprofile.socialmedia.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('main:profile')

    return redirect("main:profile")


def address_view(request, pk):
    address = Address.objects.get(id=pk)
    # reviews = address.addressreview_set.all()
    return render(request, 'main/addressdetails.html', {'address': address})


def address_add_review(request, pk):
    address = Address.objects.get(id=pk)
    if request.method == "POST":
        address.addressreview_set.create(author=request.user, text=request.POST['review'], rating=request.POST['rate'])
        messages.success(request, 'Review added successfully')
        return render(request, 'main/addressdetails.html', {'address': address})
    return render(request, 'main/addressdetails.html', {'address': address})


def roommate_add_review(request, pk):
    roommate = UserProfile.objects.get(id=pk)
    if request.method == "POST":
        rev = roommate.roommatereview_set.create(author=request.user, text=request.POST['review'], rating=request.POST['rate'])
        rev.save()
        attributes = request.POST.get('attribute_list', None)
        if attributes:
            for i in json.loads(attributes):
                attr = roommate.attribute_set.get_or_create(name=i[0], rating=i[1],)[0]
                attr.review.add(rev)
                attr.save()
        messages.success(request, 'Review added successfully')
        print(request.POST['attribute_list'])
        return render(request, 'main/roommatedetails.html', {'userp': roommate})
    return render(request, 'main/roommatedetails.html', {'userp': roommate})