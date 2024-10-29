from django.db import models

# Create your models here.
class login_table(models.Model):
    username=models.CharField(max_length=90)
    password=models.CharField(max_length=90)
    type=models.CharField(max_length=90)



class Driver(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=90)
    contact=models.CharField(max_length=90)
    address=models.CharField(max_length=90)
    email=models.CharField(max_length=90)
    licence=models.CharField(max_length=90)
    latitude=models.CharField(max_length=90)
    longitude=models.CharField(max_length=90)
    image=models.FileField()
    status=models.CharField(max_length=90)


class Driver_Availability(models.Model):
    DRIVER=models.ForeignKey(Driver,on_delete=models.CASCADE)
    from_date=models.DateField()
    to_date=models.DateField()

class User(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=90)
    contact=models.CharField(max_length=90)
    address=models.CharField(max_length=90)
    email=models.CharField(max_length=90)
    city=models.CharField(max_length=90)
    image=models.CharField(max_length=90)


class Complaint(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=90)
    date=models.CharField(max_length=90)
    reply=models.CharField(max_length=90)
    DRIVER=models.ForeignKey(Driver,on_delete=models.CASCADE)

class Feedback(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=90)
    date=models.CharField(max_length=90)
    rating=models.CharField(max_length=90)
    DRIVER=models.ForeignKey(Driver,on_delete=models.CASCADE)


class BookingTable(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    DRIVER=models.ForeignKey(Driver,on_delete=models.CASCADE)
    From_loc=models.CharField(max_length=90)
    To_loc=models.CharField(max_length=90)
    passengers=models.CharField(max_length=90)
    date=models.CharField(max_length=90)
    status=models.CharField(max_length=90)


class chat(models.Model):
    fromid=models.ForeignKey(login_table,on_delete=models.CASCADE,related_name="kk")
    toid=models.ForeignKey(login_table,on_delete=models.CASCADE,related_name="ll")
    msg = models.CharField(max_length=90)
    status = models.CharField(max_length=90)
    date = models.DateField()