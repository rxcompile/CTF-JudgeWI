# coding=utf-8
from Scoreboard.models import Team, Flag, FlagLog, Task, Score
from ipaddr import IPAddress, IPNetwork
from django.shortcuts import render_to_response

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
    flag = Flag.objects.get(flag=sended_flag, task=task)
    if flag is not None:
        score = Score.objects.create(team=team, task=task)
        score.save()
        return True
    else:
        return False
    
def send_check_flag(task_id,team_id,sended_flag):
    task = Task.objects.get(id=task_id)
    team = Team.objects.get(id=team_id)
    return check_flag(team,task,sended_flag)

def get_team(client_ip):
    for t in Team.objects.all():
        if addressInNetwork(client_ip,t.subnet):
            team = t
            break
    return team

def scoreboard(request):
    client_ip = get_ip(request)
    
    team = get_team(client_ip)
    return team_taskpage(request,team)
    
def team_taskpage(request,team):
    team_name = team.name if team is not None else "Anonimous"
    
    return render_to_response('scoreboard.html',
                              {'team_name' : team_name, 
                               'user_address' : get_ip(request),}
                              )
    
    #return HttpResponse(u'%s %s %s' % (get_ip(request), team.name, team.subnet))
