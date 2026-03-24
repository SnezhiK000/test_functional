from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=50)

class Course(models.Model):
    name = models.CharField(max_length=50)

class Student(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    course = models.ManyToManyField(Course, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    last_login = models.DateField(null=True, blank=True)