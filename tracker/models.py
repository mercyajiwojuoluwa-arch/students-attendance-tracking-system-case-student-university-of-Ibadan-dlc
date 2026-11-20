from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
class Student(models.Model):
 matric_no=models.CharField(max_length=30,unique=True)
 full_name=models.CharField(max_length=150)
 email=models.EmailField(blank=True)
 def __str__(self): return f'{self.matric_no} — {self.full_name}'
class Course(models.Model):
 code=models.CharField(max_length=20,unique=True)
 title=models.CharField(max_length=150)
 lecturer=models.ForeignKey(User,on_delete=models.PROTECT,related_name='courses')
 students=models.ManyToManyField(Student,related_name='courses',blank=True)
 def __str__(self): return f'{self.code}: {self.title}'
class Session(models.Model):
 course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='sessions')
 date=models.DateField()
 topic=models.CharField(max_length=200)
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta:
  constraints=[models.UniqueConstraint(fields=['course','date','topic'],name='unique_course_date_topic')]
 def __str__(self): return f'{self.course.code} — {self.date} — {self.topic}'
class Attendance(models.Model):
 session=models.ForeignKey(Session,on_delete=models.CASCADE,related_name='records')
 student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='records')
 present=models.BooleanField(default=False)
 recorded_at=models.DateTimeField(auto_now=True)
 class Meta:
  constraints=[models.UniqueConstraint(fields=['session','student'],name='one_record_per_student_session')]
