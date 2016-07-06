#coding=utf8
from django.shortcuts import render,render_to_response ,HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
import commands,os
import json
import sys
import logging
import datetime
logger = logging.getLogger('yunwei')


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
        ip = request.POST['ip']
        cmd = "ansible-playbook "+ param + " --extra-vars \"host=" + ip + "\""
        log_cmd = str(cmd)
        s = commands.getstatusoutput(cmd)
        data = []
        stat = s[0]
        log_stat = str(stat)
        result = s[1]
        result = "<pre>"+result+"</pre>"
        data = [cmd, stat, result]
        data = json.dumps(data)
        if stat == 0:
            p = hosts.objects.get(hostip=ip)
            p.optimes = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            p.save()
        username = request.user.username
        logger.info(username + "|" + "run:" + log_cmd + ",status:" + log_stat )
        return HttpResponse(data)


def upload(request):
    if request.method == 'POST':
        path = request.POST.get('path')
        file = request.FILES['file']
        filename = str(file)
        handle_uploaded_file(file, str(file), str(path))
        username = request.user.username
        logger.info(username + "|" + "upload " + filename + " to " + path + " suceess!")
        return HttpResponse("上传文件成功", content_type="application/json")
    return HttpResponse("上传文件失败", content_type="application/json")


def handle_uploaded_file(file, filename, path):
    #today = datetime.date.today()
    #today_str = today.strftime("%Y%m%d")
    upload_path = str('upload/' + path + '/')
    #print upload_path
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
                # add user login log
                logger.info(username + "|" + "login suceess!")
                return HttpResponseRedirect('/index/')

            else:
                # An inactive account was used - no logging in!
                logger.info(username + "|" + "is disabled!")
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            logger.info(username + "|" + "username or password is not correct!")
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
    username = request.user.username
    logout(request)
    logger.info(username + "|" + "logout suceess!")
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
        data = { "data": hosts_lists, 'page':{'pageSize':pageSize,'totalCount':hosts_nums}}
        data = json.dumps(data)
        username = request.user.username
        logger.info(username + "|" +"choose " + groupname + " group!")

    return HttpResponse(data, content_type="application/json")

