from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    full_name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    alphabet_short_name = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return "학과: %s"%self.full_name
    
class CourseType(models.Model):
    full_name = models.CharField(max_length=30, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return "과목 형태: %s"%self.full_name
    
class Course(models.Model):
    full_name = models.CharField(max_length=100)
    course_type = models.ForeignKey(CourseType, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    course_number = models.PositiveSmallIntegerField()
    prerequisites = models.ManyToManyField("self", symmetrical=False, through="PrerequisiteData")
    
    def __str__(self):
        return "과목: %s%d %s"%(self.department.alphabet_short_name, self.course_number, self.full_name)
    
    @property
    def academic_year(self):
        return self.course_number // 100
    
    @property
    def course_code(self):
        return "%s%d"%(self.department.alphabet_short_name, self.course_number)
    
class Alias(models.Model):
    full_name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="written_aliases")
    liked_users = models.ManyToManyField(User, related_name="liked_aliases")
    
    def __str__(self):
        return "별칭: %s %s"%(self.full_name, self.course.course_code)
    
class PrerequisiteData(models.Model):
    parent_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="prerequisite_dataset_as_parent")
    child_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="prerequisite_dataset_as_child")
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="written_prerequisites")
    liked_users = models.ManyToManyField(User, related_name="liked_prerequisites")
    