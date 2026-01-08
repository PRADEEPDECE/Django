from django.contrib import admin
from .models import CareerReport, Goal

@admin.register(CareerReport)
class CareerReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'completed', 'created_at')
    list_filter = ('completed',)
    search_fields = ('user__username', 'title')
