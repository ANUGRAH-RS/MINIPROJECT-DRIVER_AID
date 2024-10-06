import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from AID.models import *


def home(request):
    ob=Driver.objects.filter(LOGIN__type='driver')
    # return render(request, "sample_loc.html",{"val":ob})
    return render(request, "home.html",{"val":ob})
def log(request):
    return render(request, "login.html")
def login_code(request):

    un=request.POST['username']
    pwd=request.POST['password']
    lat=request.POST['lat']
    lon=request.POST['lon']
    request.session['lat']=lat
    request.session['lon']=lon
    a=login_table.objects.filter(username=un,password=pwd)
    if a.exists():
        ob = login_table.objects.get(username=un, password=pwd)
        request.session['lid'] = ob.id
        print(ob)
        if ob.type == "admin":
            return redirect('/admin')
        elif ob.type == "driver":
            ob1=Driver.objects.get(LOGIN__id=ob.id)
            ob1.latitude=lat
            ob1.longitude=lon
            ob1.save()
            request.session['image']=ob1.image.url
            return redirect('/driver')
        elif ob.type == "user":
            return redirect('/user_home')
        else:
            if not login_table.objects.filter(username=un).exists():
                messages.error(request, "Username does not exist.")
            else:
                messages.error(request, "Incorrect password.")
            return render(request, 'login.html')  # Render the login page with the error message
    else:
        if not login_table.objects.filter(username=un).exists():
            messages.error(request, "Username does not exist.")
        else:
            messages.error(request, "Incorrect password.")
        return render(request, 'login.html')
    return render(request, 'login.html')

def admin(request):
    a=Driver.objects.filter(LOGIN__type='driver')
    aa=a.count()
    request.session['driver']=aa

    u=User.objects.all()
    uu=u.count()
    request.session['user']=uu

    cc = Complaint.objects.all()
    ccco = cc.count()
    request.session['ccco'] = ccco
    ff = Feedback.objects.all()
    ffco = ff.count()
    request.session['ffco'] = ffco
    return render(request, "admin/admin.html",{'driver':aa,'user':user,'ccco':ccco,'ffco':ffco})

def driver(request):
    return render(request,"driver/dindex2.html")
def user(request):
    return render(request,"user.html")


def driver_reg(request):
    if 'submit' in request.POST:
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']
        email = request.POST['email']
        licence = request.POST['licence']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        img = request.FILES['img']
        fs = FileSystemStorage()
        fn = fs.save(img.name, img)
        password = request.POST['password']

        # Check if username already exists
        if login_table.objects.filter(username=email).exists():
            messages.error(request, "Username already exists.")
            return redirect('/driver_reg')

        # Create a new login entry
        l = login_table()
        l.username = email
        l.password = password
        l.type = 'pending'
        l.save()

        # Create a new driver entry
        d = Driver()
        d.LOGIN = l
        d.name = name
        d.contact = contact
        d.address = address
        d.latitude = latitude
        d.longitude = longitude
        d.email = email
        d.image = fn
        d.licence = licence
        d.status = 'pending'
        d.save()

        # Add success message
        messages.success(request, "Registration successful! Redirecting to login page...")
        return render(request, 'driver/reg.html', {'redirect_to_login': True})

    return render(request, 'driver/reg.html')



def admin_verify_accept(request,id):
    v=login_table.objects.filter(id=id).update(type='driver')
    vv=Driver.objects.filter(LOGIN_id=id).update(status='Available')
    return redirect('/admin')
def reject_verify_accept(request,id):
    ob=login_table.objects.get(id=id)
    ob.delete()
    # v=login_table.objects.filter(id=id).update(type='Rejected')
    # vv=Driver.objects.filter(LOGIN_id=id).update(status='Rejected')
    return redirect('/admin')
def block_driver(request,id):
    ob=login_table.objects.get(id=id)
    v=login_table.objects.filter(id=id).update(type='blocked')
    vv=Driver.objects.filter(LOGIN_id=id).update(status='blocked')
    return redirect('/admin')
def unblock_driver(request,id):
    ob=login_table.objects.get(id=id)
    v=login_table.objects.filter(id=id).update(type='driver')
    vv=Driver.objects.filter(LOGIN_id=id).update(status='Available')
    return redirect('/admin')

def verify_driver(request):
    a=Driver.objects.all()
    return render(request,'admin/verify_driver.html',{'data':a})



def verify_driver_search(request):
    name=request.POST['name']
    a=Driver.objects.filter(name__icontains=name)
    return render(request,'admin/verify_driver.html',{'data':a})



def user_reg(request):
    if 'submit' in request.POST:
        name=request.POST['name']
        contact=request.POST['contact']
        address=request.POST['address']
        email=request.POST['email']
        city=request.POST['city']
        image=request.FILES['image']

        password=request.POST['password']

        fs=FileSystemStorage()
        date=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jpg'
        fs.save(date,image)
        path=fs.url(date)

        if login_table.objects.filter(username=email).exists():
            messages.error(request, "Username already exists.")
            return redirect('/user_reg')

        l=login_table()
        l.username=email
        l.password=password
        l.type='user'
        l.save()

        d=User()
        d.LOGIN=l
        d.name=name
        d.contact=contact
        d.address=address
        d.email=email
        d.city=city
        d.image=path

        d.save()
        messages.success(request, "Registration successful! Redirecting to login page...")
        return render(request, 'userreg.html', {'redirect_to_login': True})
    return render(request,'userreg.html')


def admin_view_user(request):
    a=User.objects.all()
    return render(request,'admin/view_user.html',{'data':a})


def admin_view_user_search(request):
    s=request.POST['s']
    a=User.objects.filter(name__istartswith=s)
    return render(request,'admin/view_user.html',{'data':a,"s":s})


def user_home(request):
    a=Driver.objects.all()
    return render(request,'user/userindex.html',{'data':a})


def viewmore_driver(request,id):
    a=Driver.objects.get(id=id)
    return render(request,'admin/viewmore_driver.html',{'data':a})


def viewmore_user(request,id):
    a=User.objects.get(id=id)
    print(a.image,"======")
    return render(request,'admin/viewmore_user.html',{'data':a})

def driver_profile(request,):
    a=Driver.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'driver/profile.html',{'data':a})


def driver_edit_profile(request,):
    a=Driver.objects.get(LOGIN_id=request.session['lid'])
    oba=Driver_Availability.objects.filter(DRIVER__id=a.id)
    fd=''
    td=''
    if len(oba)>0:
        fd=str(oba[0].from_date)
        td=str(oba[0].to_date)
    return render(request,'driver/driver_edit.html',{'data':a,"f":fd,"t":td})


def driver_edit_post(request):
    name = request.POST['name']
    contact = request.POST['contact']
    address = request.POST['address']
    email = request.POST['email']
    licence = request.POST['licence']
    # vehicle=request.POST['vehicle']
    # vehicletype=request.POST['vehicletype']
    status = request.POST['status']
    fd=request.POST['fd']
    td=request.POST['td']



    d = Driver.objects.get(LOGIN_id=request.session['lid'])
    d.name = name
    d.contact = contact
    d.address = address
    d.email = email
    d.licence = licence
    if 'img' in request.FILES:
        img=request.FILES['img']
        fs=FileSystemStorage()
        fn=fs.save(img.name,img)
        d.image=fn
        request.session['image']="/media/"+fn
    # d.vehicle=vehicle
    # d.vehicletype=vehicletype
    d.status = status
    d.save()
    oba=Driver_Availability.objects.filter(DRIVER__id=d.id)
    if len(oba)>0:
        oba=oba[0]
        oba.from_date=fd
        oba.to_date=td
        oba.save()
    else:
        oba=Driver_Availability()
        oba.DRIVER=d
        oba.from_date=fd
        oba.to_date=td
        oba.save()
    return redirect('/driver_profile')

def user_view_profile(request):
    profile = User.objects.get(LOGIN_id=request.session['lid'])
    return render(request, 'user/user_profile.html',{'user':profile})

def user_edit_profile(request):
    user = User.objects.get(LOGIN_id=request.session['lid'])
    return render(request, 'user/edit_profile.html',{'user':user})

# def user_edit_profile_post(request):
#     name = request.POST['name']
#     phone = request.POST['phone']
#     address = request.POST['address']
#     email = request.POST['email']
#     city = request.POST['city']
#
#
#     user_profile = User.objects.get(LOGIN_id=request.session['lid'])
#     if 'img' in request.FILES:
#         img = request.FILES['img']
#         fs = FileSystemStorage()
#         fn = fs.save(img.name, img)
#         user_profile.image = fn
#         # request.session['image'] = "/media/" + fn
#
#     user_profile.name = name
#     user_profile.contact = phone
#     user_profile.address = address
#     user_profile.email = email
#     user_profile.city = city
#     user_profile.save()
#     return redirect('/user_view_profile')


def user_edit_profile_post(request):
    name = request.POST['name']
    phone = request.POST['phone']
    address = request.POST['address']
    email = request.POST['email']
    city = request.POST['city']

    user_profile = User.objects.get(LOGIN_id=request.session['lid'])

    if 'image' in request.FILES:  # Ensure 'image' is the correct field name in the form
        # img = request.FILES['image']
        # fs = FileSystemStorage()
        # fn = fs.save(img.name, img)
        # user_profile.image = fn  # Update the profile image
        # request.session['image'] = "/media/" + fn

        fs = FileSystemStorage()
        img = request.FILES['image']

        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.jpg'
        fs.save(date, img)
        path = fs.url(date)
        user_profile.image = path

    user_profile.name = name
    user_profile.contact = phone
    user_profile.address = address
    user_profile.email = email
    user_profile.city = city

    user_profile.save()

    return redirect('/user_view_profile')



def user_view_driver(request):
    a=Driver.objects.all()
    dl=[]
    for i in a:
        dis=haversine_distance(float(request.session['lat']),float(request.session['lon']),float(i.latitude),float(i.longitude))
        i.dis=float(dis)
        oba=Driver_Availability.objects.filter(DRIVER__id=i.id)
        if len(oba)>0:
            i.a=""+str(oba[0].from_date)+" to "+str(oba[0].to_date)
        else:
            i.a="Not available"
        dl.append(i.__dict__)
    sorted_data = sorted(dl, key=lambda x: x['dis'])
    print(sorted_data)
    return render(request,'user/view driver.html',{'data':sorted_data})

def send_request(request,id):
    obj = Driver.objects.get(id=id)
    return render(request, 'user/bookin_page.html',{'obj':obj})





# def user_view_driver_search(request):
#     name=request.POST['name']
#     a=Driver.objects.filter(name__icontains=name)
#     return render(request,'user/view driver.html',{'data':a})


import math

from django.shortcuts import render
from .models import Driver


# Haversine formula to calculate the distance between two points
def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c  # Distance in kilometers


def user_view_driver_search(request):
    if request.method == "POST":
        search_name = request.POST.get('name', '')
        a = Driver.objects.filter(name__icontains=search_name)

        dl = []
        for i in a:
            dis = haversine_distance(float(request.session['lat']), float(request.session['lon']), float(i.latitude),
                                     float(i.longitude))
            i.dis = float(dis)
            oba = Driver_Availability.objects.filter(DRIVER__id=i.id)
            if len(oba) > 0:
                i.a = ""+str(oba[0].from_date) + " to " + str(oba[0].to_date)
            else:
                i.a = "Not available"
            dl.append(i.__dict__)
        sorted_data = sorted(dl, key=lambda x: x['dis'])
        print(sorted_data)
        context = {'data': sorted_data}
        return render(request, 'user/view driver.html', context)

    return render(request, 'user/view driver.html')


import math


def haversine_distance(lat1, lon1, lat2, lon2):


    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Compute differences between latitudes and longitudes
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula to calculate the great-circle distance
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance
    distance = R * c

    return distance




def chatwithuser(request):
    ob = User.objects.all()
    print(ob,"jjjjjjjjjjj")
    return render(request,"driver/fur_chat.html",{'val':ob})




def chatview(request):
    ob = User.objects.all()
    d=[]
    for i in ob:
        r={"name":i.name,'photo':i.image,'email':i.email,'loginid':i.LOGIN.id}
        d.append(r)
    return JsonResponse(d, safe=False)




def coun_insert_chat(request,msg,id):
    print("===",msg,id)
    ob=chat()
    ob.fromid=login_table.objects.get(id=request.session['lid'])
    ob.toid=login_table.objects.get(id=id)
    ob.msg=msg
    ob.status="pending"
    ob.date=datetime.datetime.now().strftime("%Y-%m-%d")
    ob.save()

    return JsonResponse({"task":"ok"})
    # refresh messages chatlist



def coun_msg(request,id):

    ob1=chat.objects.filter(fromid__id=id,toid__id=request.session['lid'])
    ob2=chat.objects.filter(fromid__id=request.session['lid'],toid__id=id)
    combined_chat = ob1.union(ob2)
    combined_chat=combined_chat.order_by('id')
    res=[]
    for i in combined_chat:
        res.append({"from_id":i.fromid.id,"msg":i.msg,"date":i.date,"chat_id":i.id})

    obu=User.objects.get(LOGIN__id=id)


    return JsonResponse({"data":res,"name":obu.name,"photo":obu.image,"user_lid":obu.LOGIN.id})



def chatwithuserdr(request):
    ob = Driver.objects.all()
    print(ob,"jjjjjjjjjjj")
    return render(request,"user/user chat with dr.html",{'val':ob})




def chatviewdr(request):
    ob = Driver.objects.all()
    d=[]
    for i in ob:
        r={"name":i.name,'photo':i.image.url,'email':i.email,'loginid':i.LOGIN.id}
        d.append(r)
    return JsonResponse(d, safe=False)




def coun_insert_chatdr(request,msg,id):
    print("===",msg,id)
    ob=chat()
    ob.fromid=login_table.objects.get(id=request.session['lid'])
    ob.toid=login_table.objects.get(id=id)
    ob.msg=msg
    ob.status="pending"
    ob.date=datetime.datetime.now().strftime("%Y-%m-%d")
    ob.save()

    return JsonResponse({"task":"ok"})
    # refresh messages chatlist



def coun_msgdr(request,id):

    ob1=chat.objects.filter(fromid__id=id,toid__id=request.session['lid'])
    ob2=chat.objects.filter(fromid__id=request.session['lid'],toid__id=id)
    combined_chat = ob1.union(ob2)
    combined_chat=combined_chat.order_by('id')
    res=[]
    for i in combined_chat:
        res.append({"from_id":i.fromid.id,"msg":i.msg,"date":i.date,"chat_id":i.id})

    obu=Driver.objects.get(LOGIN__id=id)


    return JsonResponse({"data":res,"name":obu.name,"photo":obu.image.url,"user_lid":obu.LOGIN.id})
