#coding=utf8
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
import json

# Create your models here.
class Groups(models.Model):
    groupname = models.CharField(max_length=50, unique=True)
    groupdesc = models.CharField(max_length=100)
    actionstart = models.CharField(max_length=200, null=True, blank=True)
    actionstop = models.CharField(max_length=200, null=True, blank=True)
    actionrestart = models.CharField(max_length=200, null=True, blank=True)
    actiondeploy = models.CharField(max_length=200, null=True, blank=True)
    actionbackup = models.CharField(max_length=200, null=True, blank=True)
    def __unicode__(self):
        return self.groupname
        #return self.groupdesc
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('groupname','groupdesc','actionstart','actionstop','actionrestart','actiondeploy','actionbackup')

class hosts(models.Model):
    group = models.ForeignKey(Groups)
    groupname = models.CharField(max_length=50)
    hostip = models.CharField(max_length=50, unique=True)
    actionstart = models.CharField(max_length=200, null=True, blank=True)
    actionstop = models.CharField(max_length=200, null=True, blank=True)
    actionrestart = models.CharField(max_length=200, null=True, blank=True)
    actiondeploy = models.CharField(max_length=200, null=True, blank=True)
    actionbackup = models.CharField(max_length=200, null=True, blank=True)
    def __unicode__(self):
        #return self.hostip
        return unicode(self.hostip) or u''

    def toJSON(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

    class Meta:
        ordering = ['-hostip']


class hostsAdmin(admin.ModelAdmin):
    list_display = ('group','groupname','hostip','actionstart','actionstop','actionrestart','actiondeploy','actionbackup')

admin.site.register(Groups, GroupsAdmin)
admin.site.register(hosts, hostsAdmin)