from ipaddr import IPAddress, IPNetwork
from Scoreboard.models import *

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

def get_team(client_ip):
    for t in Team.objects.all():
        if addressInNetwork(client_ip,t.subnet):
            return t
    return None

def isSolveTask(team, task):
    try:
        #Throws exception if not found
        Score.objects.get(team=team, task=task)
        return True
    except:
        return False

def check_flag(team, task, sended_flag):
    #Logging to DB sended flag
    log = FlagLog.objects.create(flag=sended_flag, team=team)
    log.save()
    try:
        if not isSolveTask(team,task):
            #Special logic for files => no auto scores
            if not task.isFile:
                #Check if flag is equals to sended value
                #Throws exception if not
                Flag.objects.get(flag=sended_flag, task=task)
                #Increment scores for team
                score = Score.objects.create(team=team, task=task)
                score.save()
        return True
    except:
        return False

#Checking list for some value with delegate-function
def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False
