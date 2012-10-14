# coding=utf-8
from Scoreboard.models import Team, Flag, FlagLog, Task, Score, Category
from ipaddr import IPAddress, IPNetwork
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseNotAllowed,\
    HttpResponseNotFound
import simplejson as json
from django.db.models.aggregates import Sum

def addressInNetwork(ip,net):
    user_ip = IPAddress(ip)
    w_ip = IPNetwork(net)
    return user_ip in w_ip

def get_ip(request):
    """Returns the IP of the request, accounting for the possibility of being
    behind a proxy.
    """
    ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if ip:
        # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        ip = ip.split(", ")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip

def check_flag(team, task, sended_flag):
    log = FlagLog.objects.create(flag=sended_flag, team=team)
    log.save()
    try:
        try:
            Score.objects.get(team=team, task=task)
            return True
        except:
            Flag.objects.get(flag=sended_flag, task=task)
            score = Score.objects.create(team=team, task=task)
            score.save()
            return True
    except:
        return False
    
def send_check_flag(request):
    #if not request.is_ajax():
    #    return HttpResponseNotAllowed('Ajax')
    
    task_id = request.GET.get('task_id')
    team = get_team(get_ip(request))
    sended_flag = request.GET.get('flag')
    
    task = Task.objects.get(id=task_id)
    jsonDict = { "status": check_flag(team,task,sended_flag) }
    return HttpResponse( json.dumps( jsonDict ), mimetype="application/json" )

def task_info(request):
    if not request.is_ajax():
        return HttpResponseNotAllowed('Ajax')
    task_id = request.GET.get('task_id')
    task = Task.objects.get(id=task_id)
    jsonDict = {'task' : task.description, 'score' : task.score }
    return HttpResponse( json.dumps( jsonDict ), mimetype="application/json" )

def get_team(client_ip):
    for t in Team.objects.all():
        if addressInNetwork(client_ip,t.subnet):
            return t
    return None

def scoreboard(request):
    client_ip = get_ip(request)
    
    team = get_team(client_ip)
    
    teams = Team.objects.all()
    categories = Category.objects.all()
    scores = Score.objects.select_related()
    data = [
            {'team' : t,
             'total_score' : int( scores.filter(team=t).aggregate(s=Sum('task__score'))['s'] or 0 ),
             'category' : [ int( scores.filter(team=t, task__isnull=False, task__category=c).aggregate(s=Sum('task__score'))['s'] or 0 )
                             for c in categories]
             } for t in teams]
    
    return render_to_response('scoreboard.html',
                              {'team' : team, 
                               'user_address' : client_ip,
                               'data' : data,
                               'categories' : categories
                               }
                              )

def team(request, team_id):
    client_ip = get_ip(request)
    my_team = get_team(client_ip)
    team = Team.objects.get(id=team_id)
    categories = Category.objects.all()
    scores = Score.objects.filter(team=team)
    
    access_tasks = my_team is not None and team.id == my_team.id
    
    tasks = Task.objects.filter(visible=True)
    
    data = [ {'cat' :cat,
              'tasks' : tasks.filter(category=cat)} for cat in categories]
        
    if team is None:
        return HttpResponseNotFound()
    
    return render_to_response('team.html',
                              {'team' : team, 
                               'data' : data,
                               'user_address' : get_ip(request),
                               'access' : access_tasks
                               })