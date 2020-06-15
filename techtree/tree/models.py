from django.db import models

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
    course_code = models.CharField(max_length=20, unique=True)
    prerequisites = models.ManyToManyField("self", symmetrical=False, through="PrerequisiteData")
    
    def __str__(self):
        return "과목: %s %s"%(self.course_code, self.full_name)
    
    @property
    def academic_year(self):
        return self.course_number // 100
    
    @property
    def course_number(self):
        return int("".join(filter(str.isdigit, self.course_code)))
    
class Alias(models.Model):
    full_name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num_likes = models.PositiveSmallIntegerField();
    
    def __str__(self):
        return "별칭: %s %s ++%d"%(self.full_name, self.course.course_code, self.num_likes)
    
    class Meta:
        verbose_name_plural="Aliases"
        constraints=[
            models.UniqueConstraint(fields=['full_name', 'course'], name='unique_alias_for_course'),
        ]
    
class PrerequisiteData(models.Model):
    parent_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="prerequisite_dataset_as_parent")
    child_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="prerequisite_dataset_as_child")
    num_likes = models.PositiveSmallIntegerField();
    
    def __str__(self):
        return "선수과목 데이터: %s >>> %s ++%d"%(self.parent_course.course_code, self.child_course.course_code, self.num_likes)
    
    class Meta:
        verbose_name_plural="Prerequisite Dataset"
        constraints=[
            models.UniqueConstraint(fields=['parent_course', 'child_course'], name='unique_prerequisite_data'),
        ]
    