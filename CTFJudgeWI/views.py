# coding=utf-8
from django.shortcuts import render_to_response
from Scoreboard.models import Flag, Category, Task

def check_flag(request):
    errors = []
    accepted = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append(u'Введите флаг.')
        else:
            try:
                Flag.objects.get(flag=q)
                accepted = True
            except Flag.DoesNotExist:
                errors.append(u'Неверный флаг.')
    return render_to_response('check_form.html', {'accepted': accepted, 'errors': errors})

def tasks_list(request):
    errors = []
    columns, rows = [], [[], [], [], [], []]

    try:
        categories = Category.objects.all()
        for category in categories:
            columns.append(category.name)
            tasks_tmp = Task.objects.filter(category=category)
            for i in range(0, 4):
                try:
                    rows[i].append(tasks_tmp[i])
                except IndexError:
                    break
    except Task.DoesNotExist, Category.DoesNotExist:
        errors.append(u'Не найдены категории или задания!')
    return render_to_response('task_list.html', {'errors': errors, 'columns': columns, 'rows': rows,})

def show_task(request, category, score):
    errors = []
    score = int(score)
    category = str(category)
    task = None

    try:
        category = Category.objects.get(name=category)
        task = Task.objects.get(category=category.id, score=score, visible=True)
    except Task.DoesNotExist:
        errors.append(u'Задание не существует или еще не открыто.')
    return render_to_response('show_task.html', {'errors': errors, 'task': task})

def index(request):
    return render_to_response('base.html')