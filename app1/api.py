#coding=utf8
from tastypie.resources import ModelResource
from app1.models import Groups,hosts

class GroupsResource(ModelResource):
    class Meta:
        queryset = Groups.objects.all()
        allowed_methods = ['get']

class HostsResource(ModelResource):
    class Meta:
        queryset = hosts.objects.all()
        allowed_methods = ['get']