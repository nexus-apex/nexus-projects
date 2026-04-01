import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Project, Task, TimeEntry


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['project_count'] = Project.objects.count()
    ctx['project_planning'] = Project.objects.filter(status='planning').count()
    ctx['project_active'] = Project.objects.filter(status='active').count()
    ctx['project_on_hold'] = Project.objects.filter(status='on_hold').count()
    ctx['project_total_budget'] = Project.objects.aggregate(t=Sum('budget'))['t'] or 0
    ctx['task_count'] = Task.objects.count()
    ctx['task_to_do'] = Task.objects.filter(status='to_do').count()
    ctx['task_in_progress'] = Task.objects.filter(status='in_progress').count()
    ctx['task_review'] = Task.objects.filter(status='review').count()
    ctx['timeentry_count'] = TimeEntry.objects.count()
    ctx['timeentry_total_hours'] = TimeEntry.objects.aggregate(t=Sum('hours'))['t'] or 0
    ctx['recent'] = Project.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def project_list(request):
    qs = Project.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'project_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def project_create(request):
    if request.method == 'POST':
        obj = Project()
        obj.name = request.POST.get('name', '')
        obj.client = request.POST.get('client', '')
        obj.status = request.POST.get('status', '')
        obj.priority = request.POST.get('priority', '')
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.budget = request.POST.get('budget') or 0
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/projects/')
    return render(request, 'project_form.html', {'editing': False})


@login_required
def project_edit(request, pk):
    obj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.client = request.POST.get('client', '')
        obj.status = request.POST.get('status', '')
        obj.priority = request.POST.get('priority', '')
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.budget = request.POST.get('budget') or 0
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/projects/')
    return render(request, 'project_form.html', {'record': obj, 'editing': True})


@login_required
def project_delete(request, pk):
    obj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/projects/')


@login_required
def task_list(request):
    qs = Task.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'task_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def task_create(request):
    if request.method == 'POST':
        obj = Task()
        obj.title = request.POST.get('title', '')
        obj.project_name = request.POST.get('project_name', '')
        obj.assignee = request.POST.get('assignee', '')
        obj.status = request.POST.get('status', '')
        obj.priority = request.POST.get('priority', '')
        obj.due_date = request.POST.get('due_date') or None
        obj.estimated_hours = request.POST.get('estimated_hours') or 0
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/tasks/')
    return render(request, 'task_form.html', {'editing': False})


@login_required
def task_edit(request, pk):
    obj = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.project_name = request.POST.get('project_name', '')
        obj.assignee = request.POST.get('assignee', '')
        obj.status = request.POST.get('status', '')
        obj.priority = request.POST.get('priority', '')
        obj.due_date = request.POST.get('due_date') or None
        obj.estimated_hours = request.POST.get('estimated_hours') or 0
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/tasks/')
    return render(request, 'task_form.html', {'record': obj, 'editing': True})


@login_required
def task_delete(request, pk):
    obj = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/tasks/')


@login_required
def timeentry_list(request):
    qs = TimeEntry.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(task_name__icontains=search)
    status_filter = ''
    return render(request, 'timeentry_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def timeentry_create(request):
    if request.method == 'POST':
        obj = TimeEntry()
        obj.task_name = request.POST.get('task_name', '')
        obj.member = request.POST.get('member', '')
        obj.hours = request.POST.get('hours') or 0
        obj.date = request.POST.get('date') or None
        obj.billable = request.POST.get('billable') == 'on'
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/timeentries/')
    return render(request, 'timeentry_form.html', {'editing': False})


@login_required
def timeentry_edit(request, pk):
    obj = get_object_or_404(TimeEntry, pk=pk)
    if request.method == 'POST':
        obj.task_name = request.POST.get('task_name', '')
        obj.member = request.POST.get('member', '')
        obj.hours = request.POST.get('hours') or 0
        obj.date = request.POST.get('date') or None
        obj.billable = request.POST.get('billable') == 'on'
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/timeentries/')
    return render(request, 'timeentry_form.html', {'record': obj, 'editing': True})


@login_required
def timeentry_delete(request, pk):
    obj = get_object_or_404(TimeEntry, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/timeentries/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['project_count'] = Project.objects.count()
    data['task_count'] = Task.objects.count()
    data['timeentry_count'] = TimeEntry.objects.count()
    return JsonResponse(data)
