from django.db import models

# Create your models here.
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    phoneno = models.BigIntegerField(unique=True)
    emailid = models.EmailField(unique=True)
    password = models.CharField(max_length=15)
    secure_question = models.CharField(max_length=50)
    answer = models.CharField(max_length=45)
    earnings = models.IntegerField(default=0)
    images = models.CharField(max_length=100, default='user.png')

class Vehicles(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=100)
    capacity = models.CharField(max_length=2)
    is_available = models.BooleanField(default=True)
    rent = models.CharField(max_length=10)
    dealer_id = models.IntegerField()
    location = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=50)

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    total_rent = models.CharField(max_length=10)
    days = models.CharField(max_length=3)
    order_date = models.CharField(max_length=50)
    dealer_id = models.IntegerField()
    customer_id = models.IntegerField()
    status = models.CharField(max_length=25)
    location = models.CharField(max_length=50)
    vehicle_image = models.CharField(max_length=100)
    vehicle_name = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=15)
    vehicle_id = models.IntegerField()
    capacity = models.CharField(max_length=2)

class Contactus(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phoneno = models.BigIntegerField()
    emailid = models.EmailField()
    message = models.TextField()
