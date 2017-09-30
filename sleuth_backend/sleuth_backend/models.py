from django.db import models

### Course Related Data
class Subject(models.Model):
    '''
    Subject data
    '''
    code = models.CharField(max_length=4)
    title = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)

class Course(models.Model):
    '''
    Course data of a Subject
    '''
    subject = models.ForeignKey("sleuth_backend.Subject", related_name="courses")
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    prereqs = models.CharField(max_length=500)

class Sections(models.Model):
    '''
    Section data of a Course
    '''
    course = models.ForeignKey("sleuth_backend.Course", related_name="sections")
    code = models.CharField(max_length=20)
    activity = models.CharField(max_length=20)
    credits = models.CharField(max_length=2)
    status = models.CharField(max_length=100)
    term = models.CharField(max_length=1)
    day = models.CharField(max_length=20)
    time = models.CharField(max_length=30)
    room = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    # more? possibly break into submodels
    
