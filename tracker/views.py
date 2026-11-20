import csv
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count,Q
from django.http import HttpResponse,HttpResponseForbidden
from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from .models import Course,Session,Attendance,Student
from .forms import SessionForm

def permitted(user,course): return user.is_superuser or course.lecturer_id==user.id
@login_required
def dashboard(request):
 courses=Course.objects.all() if request.user.is_superuser else Course.objects.filter(lecturer=request.user)
 return render(request,'tracker/dashboard.html',{'courses':courses,'session_count':Session.objects.filter(course__in=courses).count(),'student_count':Student.objects.filter(courses__in=courses).distinct().count()})
@login_required
def course_detail(request,pk):
 course=get_object_or_404(Course,pk=pk)
 if not permitted(request.user,course): return HttpResponseForbidden('Access denied')
 sessions=course.sessions.order_by('-date','-id')
 total=sessions.count()
 stats=[]
 for student in course.students.order_by('matric_no'):
  present=Attendance.objects.filter(session__course=course,student=student,present=True).count()
  stats.append((student,present,round(present*100/total,1) if total else 0))
 return render(request,'tracker/course.html',{'course':course,'sessions':sessions,'stats':stats,'total':total})
@login_required
def create_session(request):
 form=SessionForm(request.POST or None,user=request.user)
 if request.method=='POST' and form.is_valid():
  session=form.save();messages.success(request,'Session created');return redirect('session',pk=session.pk)
 return render(request,'tracker/form.html',{'form':form})
@login_required
def session_detail(request,pk):
 session=get_object_or_404(Session.objects.select_related('course'),pk=pk)
 if not permitted(request.user,session.course):return HttpResponseForbidden('Access denied')
 records={r.student_id:r.present for r in session.records.all()}
 students=[(s,records.get(s.id,False)) for s in session.course.students.order_by('matric_no')]
 return render(request,'tracker/session.html',{'session':session,'students':students})
@login_required
@require_POST
def mark_attendance(request,pk):
 session=get_object_or_404(Session.objects.select_related('course'),pk=pk)
 if not permitted(request.user,session.course):return HttpResponseForbidden('Access denied')
 student=get_object_or_404(session.course.students,pk=request.POST.get('student_id'))
 Attendance.objects.update_or_create(session=session,student=student,defaults={'present':request.POST.get('present')=='yes'})
 messages.success(request,'Attendance saved');return redirect('session',pk=pk)
@login_required
def export_csv(request,pk):
 course=get_object_or_404(Course,pk=pk)
 if not permitted(request.user,course):return HttpResponseForbidden('Access denied')
 response=HttpResponse(content_type='text/csv');response['Content-Disposition']=f'attachment; filename="{course.code}_attendance.csv"'
 writer=csv.writer(response);writer.writerow(['Matric No','Student','Session Date','Topic','Present'])
 for session in course.sessions.order_by('date'):
  records={r.student_id:r.present for r in session.records.all()}
  for student in course.students.order_by('matric_no'):
   writer.writerow([student.matric_no,student.full_name,session.date,session.topic,'Yes' if records.get(student.id,False) else 'No'])
 return response
