from django.urls import path
from . import views
urlpatterns=[path('',views.dashboard,name='dashboard'),path('courses/<int:pk>/',views.course_detail,name='course'),path('sessions/new/',views.create_session,name='create_session'),path('sessions/<int:pk>/',views.session_detail,name='session'),path('sessions/<int:pk>/mark/',views.mark_attendance,name='mark'),path('courses/<int:pk>/export/',views.export_csv,name='export')]
