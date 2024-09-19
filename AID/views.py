import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from AID.models import *


def home(request):
    ob=Driver.objects.filter(LOGIN__type='driver')
    return render(request, "home.html",{"val":ob})
def log(request):
    return render(request, "login.html")
def login_code(request):

    un=request.POST['username']
    pwd=request.POST['password']

    a=login_table.objects.filter(username=un,password=pwd)
    if a.exists():
        ob = login_table.objects.get(username=un, password=pwd)
        request.session['lid'] = ob.id
        if ob.type == "admin":
            return redirect('/admin')
        elif ob.type == "driver":
            ob1=Driver.objects.get(LOGIN__id=ob.id)
            request.session['image']=ob1.image.url
            return redirect('/driver')
        elif ob.type == "user":
            return redirect('/user_home')
        else:
            return HttpResponse('''<script>alert("invalid);window.location="/"</script>''')
    else:
        return HttpResponse('''<script>alert("invalid");window.location="/"</script>''')


def admin(request):
    a=Driver.objects.filter(LOGIN__type='driver')
    aa=a.count()
    request.session['driver']=aa

    u=User.objects.all()
    uu=u.count()
    request.session['user']=uu
    return render(request, "admin/admin.html",{'driver':aa,'user':user})

def driver(request):
    return render(request,"driver/dindex2.html")
def user(request):
    return render(request,"user.html")





def driver_reg(request):
    if 'submit' in request.POST:
        name=request.POST['name']
        contact=request.POST['contact']
        address=request.POST['address']
        email=request.POST['email']
        licence=request.POST['licence']
        img=request.FILES['img']
        fs=FileSystemStorage()
        fn=fs.save(img.name,img)
        # vehicle=request.POST['vehicle']
        # vehicletype=request.POST['vehicletype']
        password=request.POST['password']

        l=login_table()
        l.username=email
        l.password=password
        l.type='pending'
        l.save()

        d=Driver()
        d.LOGIN=l
        d.name=name
        d.contact=contact
        d.address=address
        d.email=email
        d.image=fn
        d.licence=licence
        # d.vehicle=vehicle
        # d.vehicletype=vehicletype
        d.status='pending'
        d.save()
        return redirect('/')
    return render(request,'driver/reg.html')



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
        return redirect('/')
    return render(request,'userreg.html')


def admin_view_user(request):
    a=User.objects.all()
    return render(request,'admin/view_user.html',{'data':a})


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
    return render(request,'driver/driver_edit.html',{'data':a})


def driver_edit_post(request):
    name = request.POST['name']
    contact = request.POST['contact']
    address = request.POST['address']
    email = request.POST['email']
    licence = request.POST['licence']
    # vehicle=request.POST['vehicle']
    # vehicletype=request.POST['vehicletype']
    status = request.POST['status']



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
    return redirect('/driver_profile')

def user_view_profile(request):
    profile = User.objects.get(LOGIN_id=request.session['lid'])
    return render(request, 'user/user_profile.html',{'profile':profile})
