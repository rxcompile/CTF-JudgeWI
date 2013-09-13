# coding=utf-8
'''
Проект моделей базы данных
'''

from django.db import models
import os

class TeamMember(models.Model):
    name = models.CharField(u'ФИО', max_length=50)
    nick = models.CharField(u'Никнейм', max_length=30, blank=True)

    class Meta:
        verbose_name_plural = u"Участники"
        verbose_name = u"Участник"

    def __unicode__(self):
        return self.name

class Team(models.Model):
    def GetFilename(instance,filename):
        # used to generate random unique id
        import uuid
        uid = uuid.uuid4()
        return os.path.join(u'team-icons', unicode(uid)) + ".jpg"

    name = models.CharField(u'Название команды', max_length=50)
    image = models.ImageField(u'Иконка', blank=True, upload_to=GetFilename)
    subnet = models.CharField(u'Подсеть', max_length=18)

    members = models.ManyToManyField(TeamMember, blank=True)

    class Meta:
        verbose_name_plural = u"Команды"
        verbose_name = u"Команда"

    def get_members_display(self):
        return u', '.join([i.name for i in self.members.all()])
    get_members_display.short_description = u"Участники"


    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(u'Название', max_length=40)
    tip = models.TextField(u'Подсказка', blank=True)

    class Meta:
        verbose_name_plural = u"Категории"
        verbose_name = u"Категория"

    def __unicode__(self):
        return self.name

SCORE_CHOICES = (
    (100,'100'),
    (200,'200'),
    (300,'300'),
    (400,'400'),
    (500,'500'),
)

class Task(models.Model):
    category = models.ForeignKey(Category)
    description = models.TextField(u'Описание')
    score = models.PositiveSmallIntegerField(u'Очки',choices=SCORE_CHOICES)
    visible = models.BooleanField(u'Открыт')
    isFile = models.BooleanField(u'Загрузка файла')

    class Meta:
        verbose_name_plural = u"Задания"
        verbose_name = u"Задание"

    def __unicode__(self):
        return u'%s-%s' % (self.category, self.score)

class Score(models.Model):
    team = models.ForeignKey(Team)
    task = models.ForeignKey(Task,related_name='task')

    class Meta:
        verbose_name_plural = u"Набранные очки"
        verbose_name = u"Набрано"

    def __unicode__(self):
        return u'%s scores %s from %s' % (self.team, self.task.score, self.task)

class FlagLog(models.Model):
    def GetFilename(instance,filename):
        # used to generate random unique id
        import uuid
        uid = uuid.uuid4()
        return os.path.join(u'log-uploads', unicode(instance.team), unicode(instance.task), unicode(uid)) + ".jpg"

    team = models.ForeignKey(Team)
    task = models.ForeignKey(Task)
    flag = models.CharField(u'Отправленный флаг', max_length=20)
    file = models.FileField(u'Файл', upload_to=GetFilename, blank=True)
    date = models.DateTimeField(u'Отправлен', auto_now_add=True)

    class Meta:
        verbose_name_plural = u"Отправленные флаги"
        verbose_name = u"Отправленный флаг"

    def __unicode__(self):
        return u'%s send %s' % (self.team, self.flag)


class Flag(models.Model):
    task = models.ForeignKey(Task)
    flag = models.CharField(u'Флаг',max_length=20)

    class Meta:
        verbose_name_plural = u"Флаги"
        verbose_name = u"Флаг"

    def __unicode__(self):
        return u'%s %s' % (self.flag, self.task)
