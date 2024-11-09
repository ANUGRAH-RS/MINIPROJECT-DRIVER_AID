
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# Create your views here.
from AID.models import *
from DRIVER_AID import settings


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
            request.session['diber_suku']=ob1.name
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


def view_my_ratings(request):
    feed = Feedback.objects.filter(DRIVER=Driver.objects.get(LOGIN=request.session['lid']))
    return render(request, 'driver/my_feedbacks.html',{'feed':feed})


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
    a=Driver.objects.all().order_by('-id')
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


def manage_complaints(request):
    complaint = Complaint.objects.all()
    return render(request, 'admin/manage_complaints.html',{'complaint':complaint})

def reply_complaint(request,id):
    if request.method == 'POST':
        complaint = Complaint.objects.get(id=id)
        complaint.reply = request.POST['reply']
        complaint.save()
        return redirect('/manage_complaints')
    return render(request, 'admin/reply_complaint.html')


def user_home(request):
    a=Driver.objects.all()
    return render(request,'user/userindex.html',{'data':a})

def manage_complaint(request):
    complaints = Complaint.objects.filter(USER__LOGIN_id=request.session['lid']).order_by('-id')
    return render(request, 'user/manage_complaint.html',{'complaints':complaints})


from django.utils import timezone
def send_complaint(request):
    if request.method == 'POST':
        complaint_text = request.POST.get('complaint')
        did = request.POST.get('did')
        date = timezone.now().strftime('%Y-%m-%d')  # Get current date

        Complaint.objects.create(
            USER=User.objects.get(LOGIN_id=request.session['lid']),  # Assuming the user is logged in
            complaint=complaint_text,
            date=date,
            DRIVER=Driver.objects.get(id=did),
            reply='pending'  # Initialize with an empty reply
        )
        return redirect('/manage_complaint')  # Redirect back to the complaints page

    return render(request, 'user/manage_complaint.html')



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
    a = Driver.objects.all()  # Get all drivers
    dl = []  # List to store drivers and their calculated distances

    # Get latitude and longitude from the session, with default fallback to None
    user_lat = request.session.get('lat', None)
    user_lon = request.session.get('lon', None)

    # Ensure latitude and longitude are valid before proceeding
    if not user_lat or not user_lon:
        return render(request, 'user/view driver.html', {'error': 'Location data is missing from session'})

    try:
        user_lat = float(user_lat)
        user_lon = float(user_lon)
    except ValueError:
        user_lat=11.876543
        user_lon=75.34567
    for i in a:
        # Check if driver's latitude and longitude are not empty
        if not i.latitude or not i.longitude:
            continue  # Skip this driver if latitude or longitude is missing

        try:
            driver_lat = float(i.latitude)
            driver_lon = float(i.longitude)
        except ValueError:
            continue  # Skip this driver if latitude or longitude is invalid

        # Calculate distance using haversine function
        dis = haversine_distance(user_lat, user_lon, driver_lat, driver_lon)
        i.dis = float(dis)

        # Check driver availability
        oba = Driver_Availability.objects.filter(DRIVER__id=i.id)
        if len(oba) > 0:
            i.a = f"{oba[0].from_date} to {oba[0].to_date}"
        else:
            i.a = "Not available"

        dl.append(i.__dict__)  # Append the driver's data

    # Sort the list of drivers by distance
    sorted_data = sorted(dl, key=lambda x: x['dis'])

    print(sorted_data)  # Debugging output to check sorted data
    return render(request, 'user/view driver.html', {'data': sorted_data})

from datetime import datetime
#
# def send_request(request,id):
#     request.session['did']=id
#     obj = Driver.objects.get(id=id)
#
#     oba = Driver_Availability.objects.filter(DRIVER__id=id).order_by("-id")
#     if len(oba)>0:
#         fd=datetime.datetime.now().strftime("%Y-%m-%d")
#         fd = datetime.datetime.strptime(fd, '%Y-%m-%d').date()
#         if oba[0].from_date>fd:
#             fd=str(oba[0].from_date)
#
#
#         return render(request, 'user/bookin_page.html',{'obj':obj,"fd":str(fd),"td":str(oba[0].to_date),"s":"0"})
#     else:
#
#
#             return render(request, 'user/bookin_page.html', {'obj': obj,"s":"1"})

def send_request(request, id):
    request.session['did'] = id
    obj = Driver.objects.get(id=id)

    oba = Driver_Availability.objects.filter(DRIVER__id=id).order_by("-id")
    if len(oba) > 0:
        fd = datetime.now().strftime("%Y-%m-%d")
        fd = datetime.strptime(fd, '%Y-%m-%d').date()
        if oba[0].from_date > fd:
            fd = str(oba[0].from_date)

        return render(request, 'user/bookin_page.html', {'obj': obj, "fd": str(fd), "td": str(oba[0].to_date), "s": "0"})
    else:
        return render(request, 'user/bookin_page.html', {'obj': obj, "s": "1"})


def jquery_date_checking(request,date):
    xx = BookingTable.objects.filter(DRIVER=request.session['did'], date__exact=date)
    print(xx,"==================")
    if len(xx) > 0:
        return JsonResponse({"task": "yes"})
    else:
        return JsonResponse({"task": "no"})


def book_now(request):
    date = request.POST['bd']
    from_p = request.POST['from']
    to = request.POST['to']
    pas = request.POST['pas']

    # xx=BookingTable.objects.filter(DRIVER=request.session['did'],date__exact=date)
    # if len(xx)>0:
    #     return HttpResponse('''<script>alert("already booked....");window.location='/user_view_driver'</script>''')

    ob=BookingTable()
    ob.USER=User.objects.get(LOGIN__id=request.session['lid'])
    ob.DRIVER=Driver.objects.get(id=request.session['did'])
    ob.From_loc=from_p
    ob.To_loc=to
    ob.passengers=pas
    ob.date=date
    ob.status='pending'
    ob.save()
    return redirect("/userviewhistory#a")

def userviewhistory(request):
    history=BookingTable.objects.filter(USER__LOGIN__id=request.session['lid']).order_by("-id")
    return render(request,"user/booking_history.html",{"history":history})

from datetime import datetime
def add_review(request,id):
    if request.method == 'POST':
        feedback=request.POST['feedback']
        rating=request.POST['rating']

        feed = Feedback(
            USER=User.objects.get(LOGIN_id=request.session['lid']),
            feedback=feedback,
            date=datetime.now(),
            rating=rating,
            DRIVER=Driver.objects.get(id=id)
        )
        feed.save()
        return redirect('/userviewhistory')
    return render(request,"user/rating.html")



def sendcomp(request,id):
    request.session['did']=id

    return render(request,"user/complaint.html")

def driverviewhistory(request):
    history=BookingTable.objects.filter(DRIVER__LOGIN__id=request.session['lid']).exclude(status='pending').order_by("-id")
    return render(request,"driver/view_history.html",{"history":history})

def driverviewhistory2(request):
    history=BookingTable.objects.filter(DRIVER__LOGIN__id=request.session['lid']).exclude(status='pending').order_by("-id")
    return render(request,"driver/view_history2.html",{"history":history})


def view_request(request):
    history=BookingTable.objects.filter(DRIVER__LOGIN__id=request.session['lid'],status='pending').order_by("-id")
    return render(request,"driver/view_request.html",{"history":history})

def accept_ride(request,id):
    history=BookingTable.objects.get(id=id)
    history.status="Accepted"
    history.save()
    return redirect("/view_request")

def reject_ride(request,id):
    history=BookingTable.objects.get(id=id)
    history.status="Rejected"
    history.save()
    return redirect("/view_request")

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

        # Retrieve session lat/lon and ensure they are valid floats
        try:
            lat = float(request.session.get('lat', ''))
            lon = float(request.session.get('lon', ''))
        except ValueError:
            # Handle invalid or missing session data
            return render(request, 'error_page.html', {'error': 'Location data is missing or invalid.'})

        dl = []
        for i in a:
            try:
                # Calculate distance only if latitude and longitude are valid
                dis = haversine_distance(lat, lon, float(i.latitude), float(i.longitude))
                i.dis = dis
            except ValueError:
                # Handle any invalid driver latitude/longitude data
                i.dis = float('inf')  # Assign a high value or skip this entry if desired

            oba = Driver_Availability.objects.filter(DRIVER__id=i.id)
            i.a = f"{oba[0].from_date} to {oba[0].to_date}" if oba else "Not available"
            dl.append(i.__dict__)

        # Sort the data based on distance
        sorted_data = sorted(dl, key=lambda x: x['dis'])
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
        ob1=chat.objects.filter(toid__id=request.session['lid'],fromid__id=i.LOGIN.id).order_by("-date")
        name=i.name

        if len(ob1)>0:
            name=name+" ("+str(len(ob1))+")"
        r={"name":name,'photo':i.image,'email':i.email,'loginid':i.LOGIN.id,"c":len(ob1)}

        d.append(r)
    sorted_list = sorted(d, key=lambda x: x['c'], reverse=True)
    return JsonResponse(sorted_list, safe=False)




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
    distinct_users = chat.objects.filter(toid=request.session["lid"]).values('toid').distinct()
    print("====sss", distinct_users)
    # for i in distinct_users:
    ob = Driver.objects.all()
    d=[]
    for i in ob:
        ob1 = chat.objects.filter(toid__id=request.session['lid'], fromid__id=i.LOGIN.id).order_by("-date")
        name = i.name

        if len(ob1) > 0:
            name = name + " (" + str(len(ob1)) + ")"
        # r = {"name": name, 'photo': i.image, 'email': i.email, 'loginid': i.LOGIN.id, "c": len(ob1)}
        r = {"name": name, 'photo': i.image.url, 'email': i.email, 'loginid': i.LOGIN.id, "c": len(ob1)}
        d.append(r)
    sorted_list = sorted(d, key=lambda x: x['c'], reverse=True)

    return JsonResponse(sorted_list, safe=False)




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



def forget_password(request):
    return render(request,'ForgetPassword.html')


from django.core.mail import send_mail
def forget_password_post(request):
    em = request.POST['username']
    import random
    import string
    # password = random.randint(000000, 999999)
    log = login_table.objects.filter(username=em)

    length = 10 # Adjust the password length as needed
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))

    if log.exists():
        logg = login_table.objects.get(username=em)
        message = 'temporary Password  is!... ' + str(password)
        send_mail(
            'temporary...! Password',
            message,
            settings.EMAIL_HOST_USER,
            [em, ],
            fail_silently=False
        )
        logg.password = password
        logg.save()
        return HttpResponse('''
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                    <script>
                        document.addEventListener("DOMContentLoaded", function() {
                            Swal.fire({
                                icon: 'success',
                                title: 'Success...Please Check Your Mail!',
                                confirmButtonText: 'OK',
                                reverseButtons: true
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location = '/log';
                                }
                            });
                        });
                    </script>
                ''')



    else:
        return HttpResponse('''
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                    <script>
                        document.addEventListener("DOMContentLoaded", function() {
                            Swal.fire({
                                icon: 'error',
                                title: 'invalid!',
                                confirmButtonText: 'OK',
                                reverseButtons: true
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location = '/forget_password';
                                }
                            });
                        });
                    </script>
                ''')









def payment_view(request):
    success_message = None  # Initialize success message variable

    if request.method == 'POST':
        # Retrieve the booking ID from the form submission
        booking_id = request.POST.get('booking_id')

        # Check if the booking exists
        try:
            booking = BookingTable.objects.get(id=booking_id)
        except BookingTable.DoesNotExist:
            return HttpResponse("Booking not found.", status=404)

        # Process the payment (you can add your payment processing logic here)

        # If payment is successful, update the booking status
        booking.status = 'Paid'
        booking.save()

        # Set a success message
        success_message = "Your payment was successful............................"

    # Retrieve the booking to pass to the template if needed
    booking = BookingTable.objects.filter().last()  # Or another method to fetch the booking
    return render(request, 'user/payment.html', {'success_message': success_message, 'booking': booking})