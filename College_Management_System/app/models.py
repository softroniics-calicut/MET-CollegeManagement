from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.utils import timezone

# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=200)
    details = models.CharField(max_length=255)
    def __str__(self):
        return self.department_name


class CustomUser(AbstractUser):
    usertype_choices= (
        ('Student','Student'),
        ('Teacher','Teacher'),
        ('Librarian','Librarian'),
    )
    phone_number = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    user_type = models.CharField(choices=usertype_choices, max_length=100,null=True, blank=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    pic=models.FileField(upload_to='userprofile')


class Book(models.Model):
     librarian_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
     bookname=models.CharField(max_length=100)
     author=models.CharField(max_length=100)
     description=models.CharField(max_length=1500)
     genre=models.CharField(max_length=100)
     image=models.FileField(upload_to='books')

     def __str__(self):
         return self.bookname


class Booking(models.Model):
    username=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    bookname=models.ForeignKey(Book,on_delete=models.CASCADE)
    issuedate=models.DateField(default=timezone.now,blank=False)


