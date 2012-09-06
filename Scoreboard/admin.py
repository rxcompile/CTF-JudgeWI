'''
Created on 06.09.2012

@author: rxcompile
'''
from django.contrib import admin
from Scoreboard.models import *

admin.site.register(Team,TeamAdmin)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Score,ScoreAdmin)
admin.site.register(Flag,FlagAdmin)
admin.site.register(TeamMember,TeamMemberAdmin)
