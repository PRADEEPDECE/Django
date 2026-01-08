from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.career_test, name='career_test'),
    path('save-report/', views.save_report, name='save_report'),
    path('reports/', views.career_reports, name='career_reports'),
    path('reports/<int:report_id>/pdf/', views.download_report_pdf, name='download_report_pdf'),
    path('goals/', views.goals_page, name='goals_page'),
    path('goals/<int:goal_id>/toggle/', views.toggle_goal, name='toggle_goal'),
    path('goals/<int:goal_id>/delete/', views.delete_goal, name='delete_goal'),
    path("reports/", views.reports, name="reports"),
    path("reports/delete/<int:report_id>/", views.delete_report, name="delete_report"),

]
