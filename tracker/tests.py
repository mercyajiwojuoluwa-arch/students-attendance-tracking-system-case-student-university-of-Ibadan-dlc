from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from .models import Student,Course,Session,Attendance
class AttendanceTests(TestCase):
 def setUp(self):
  self.lecturer=User.objects.create_user('lecturer',password='StrongTestPass123!')
  self.other=User.objects.create_user('other',password='StrongTestPass123!')
  self.student=Student.objects.create(matric_no='DLC001',full_name='Test Student')
  self.course=Course.objects.create(code='CSC101',title='Introduction',lecturer=self.lecturer)
  self.course.students.add(self.student)
  self.session=Session.objects.create(course=self.course,date=date(2026,11,20),topic='Week 1')
 def test_login_required(self):
  self.assertEqual(self.client.get(reverse('dashboard')).status_code,302)
 def test_lecturer_can_mark_attendance(self):
  self.client.force_login(self.lecturer)
  response=self.client.post(reverse('mark',args=[self.session.pk]),{'student_id':self.student.pk,'present':'yes'})
  self.assertEqual(response.status_code,302)
  self.assertTrue(Attendance.objects.get().present)
 def test_cannot_duplicate_record(self):
  self.client.force_login(self.lecturer)
  url=reverse('mark',args=[self.session.pk])
  self.client.post(url,{'student_id':self.student.pk,'present':'yes'})
  self.client.post(url,{'student_id':self.student.pk,'present':'no'})
  self.assertEqual(Attendance.objects.count(),1)
  self.assertFalse(Attendance.objects.get().present)
 def test_other_lecturer_denied(self):
  self.client.force_login(self.other)
  self.assertEqual(self.client.get(reverse('course',args=[self.course.pk])).status_code,403)
 def test_csv_export(self):
  self.client.force_login(self.lecturer)
  response=self.client.get(reverse('export',args=[self.course.pk]))
  self.assertEqual(response.status_code,200)
  self.assertIn(b'DLC001',response.content)
