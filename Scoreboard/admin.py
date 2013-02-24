'''
Created on 06.09.2012

@author: rxcompile
'''
from django.contrib import admin
from Scoreboard.models import Team, Category,Task, Score, Flag, FlagLog, TeamMember


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name','nick')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name','subnet','get_members_display')

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('team','task')
    
class FlagAdmin(admin.ModelAdmin):
    list_display = ('task','flag')
    
class FlagLogAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'task', 'team', 'file')
    list_filter = ('task', 'team', 'task__isFile')
    
admin.site.register(Team,TeamAdmin)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Score,ScoreAdmin)
admin.site.register(Flag,FlagAdmin)
admin.site.register(FlagLog,FlagLogAdmin)
admin.site.register(TeamMember,TeamMemberAdmin)
