from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from .forms import CareerTestForm, GoalForm
from .models import CareerReport, Goal
from .utils import generate_report_pdf
from google import genai
from django.core.paginator import Paginator



@login_required
def dashboard(request):
    reports_count = CareerReport.objects.filter(user=request.user).count()
    goals = Goal.objects.filter(user=request.user, completed=False)[:3]
    return render(request, 'career/dashboard.html', {
        'reports_count': reports_count,
        'goals': goals,
    })






@login_required
def career_test(request):
    recommendation = None

    if request.method == "POST":
        interests = request.POST.get("interests")
        skills = request.POST.get("skills")
        education = request.POST.get("education")
        goals = request.POST.get("goals", "Not specified")

        # ✅ NEW: Work Preferences
        work_mode = request.POST.get("work_mode")
        work_location = request.POST.get("work_location", "No preference")

        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        prompt = f"""
You are an expert career counselor.

Student Details:
Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Work Preferences:
Preferred Work Mode: {work_mode}
Preferred Work Location: {work_location}

Based on the above profile and work preferences, suggest:
1. Suitable career paths
2. Required skills
3. Learning roadmap
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        recommendation = response.text

        # ✅ Save complete input for reports / PDF
        CareerReport.objects.create(
            user=request.user,
            input_data=(
                f"Interests: {interests}\n"
                f"Skills: {skills}\n"
                f"Education: {education}\n"
                f"Career Goals: {goals}\n"
                f"Work Mode: {work_mode}\n"
                f"Preferred Location: {work_location}"
            ),
            recommendation=recommendation
        )

    return render(
        request,
        "career/career_test.html",
        {"recommendation": recommendation}
    )



@login_required
def save_report(request):
    input_data = request.session.get('last_input_data')
    recommendation = request.session.get('last_recommendation')
    if input_data and recommendation:
        CareerReport.objects.create(
            user=request.user,
            input_data=input_data,
            recommendation=recommendation
        )
    return redirect('career_reports')

@login_required
def career_reports(request):
    reports = CareerReport.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'career/reports.html', {'reports': reports})

@login_required
def download_report_pdf(request, report_id):
    report = get_object_or_404(CareerReport, id=report_id, user=request.user)
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="career_report_{report.id}.pdf"'
    generate_report_pdf(response, report)
    return response

@login_required
def goals_page(request):
    goals = Goal.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals_page')
    else:
        form = GoalForm()
    return render(request, 'career/goals.html', {'goals': goals, 'form': form})

@login_required
def toggle_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.completed = not goal.completed
    goal.save()
    return redirect('goals_page')

@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.delete()
    return redirect('goals_page')


@login_required
def reports(request):
    report_list = CareerReport.objects.filter(user=request.user).order_by("-created_at")

    paginator = Paginator(report_list, 5)  # 5 reports per page
    page_number = request.GET.get("page")
    reports = paginator.get_page(page_number)

    return render(request, "reports.html", {"reports": reports})


@login_required
def delete_report(request, report_id):
    report = get_object_or_404(CareerReport, id=report_id, user=request.user)
    report.delete()
    return redirect("reports")
