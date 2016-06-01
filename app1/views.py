#coding=utf8
from django.shortcuts import render,render_to_response ,HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize


import commands,os
import json
import sys
import datetime
from app1.models import hosts

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# Create your views here.
@login_required
def index(request):
    return render_to_response('home.html',context_instance=RequestContext(request))

@login_required
def run_com(request):
    if request.method == 'POST':
        param  = request.POST['param']
        print param
        ip = request.POST['ip']
        print ip
        cmd = "ansible-playbook "+ param + " --extra-vars \"host=" + ip + "\""
        s = commands.getstatusoutput(cmd)
        data = []
        stat = s[0]
        result = s[1]
        result = "<pre>"+result+"</pre>"

        data = [cmd, stat, result]
        data = json.dumps(data)
        print data
        return HttpResponse(data)
    #else:
        #return HttpResponse("<h1>test</h1>")
    #return render(request, 'result.html', {'cmd': cmd,'stat': stat, 'result': result})


@login_required
def upload(request):
    if request.method == 'POST':
        path = request.POST.get('path')
        #print path
        handle_uploaded_file(request.FILES['file'], str(request.FILES['file']), str(path))
        return HttpResponse("Successful")
    return HttpResponse("Failed")

@login_required
def handle_uploaded_file(file, filename, path):
    today = datetime.date.today()
    today_str = today.strftime("%Y%m%d")
    upload_path = str('upload/' + path + '/' + today_str  +'/')
    print upload_path
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    with open(upload_path + filename, 'wb+'
                                      '') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your polls account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')


@login_required
def get_host_list(request):
    if request.method == 'POST':
        groupname = request.POST.get('groupname')
        hosts_list = serialize('json', hosts.objects.filter(groupname=groupname))
        hosts_list = json.loads(hosts_list)
        hosts_nums = len(hosts_list)
        pageSize = 10
        outputs=[]
        i = 0
        while (i < hosts_nums):
            hosts_obj = hosts_list[i]['fields']
            outputs.append(hosts_obj)
            i = i + 1
        hosts_lists = outputs
        print hosts_lists
        data = { "data": hosts_lists, 'page':{'pageSize':pageSize,'totalCount':hosts_nums}}
        data = json.dumps(data)
        print data
    return HttpResponse(data, content_type="application/json")

    #return JsonResponse(hosts_list)