from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
import hashlib

# Create your views here.
def reg_view(request):

    #register as a new user
    #GET    return page
    if request.method == 'GET':
        return render(request, 'user/register.html')
    #POST    deal with the data
    elif request.method == 'POST':
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
    #   1.two passwords should be same
        if password_1 != password_2:
            return HttpResponse('Two passwords do not match!')
        # hash algorithm - Given the plaintext,
        #                compute a length of irreversible value;
        #   md5, sha-256 ...
        # 特点：
        #   1. Some length of value(can not change the length, md5 - 32)
        #   2. Irreversible: can not compute the plaintext from code
        #   3. 雪蹦效应： 输入改变，输出必然变
        # When to use: 1. passcode 2. 文件完整性校验
        # How to use：
        # import hashlib
        # m = hashlib.md5()
        # m.update(b'123456')
        # m.hexdigest() 
        # output: e10adc3949ba59abbe56e057f20f883e
        m = hashlib.md5()
        m.update(password_1.encode())
        password_m = m.hexdigest()

    #   2.check if the username already exist
        old_users = User.objects.filter(username=username)
        if old_users:
            return HttpResponse('The username already exist!')

    #   3.insert data[just insert right password]
        try:
            user = User.objects.create(username=username, password=password_m)
        except Exception as e:
            # there may have error by write in same data
            print('--create user error %s'%(e))
            return HttpResponse('The username exist!')
        
        # save the session:
        request.session['username'] = username
        request.session['uid'] = user.id
        #To do change session max_length to 1 day

        return HttpResponseRedirect('/index')


def login_view(request):

    # GET login page
    if request.method == 'GET':

        # 1.check the login status, if logged in, show 'logged in already'
        if request.session.get('username') and request.session.get('uid'):
            #return HttpResponse('Logged in already')
            return HttpResponseRedirect('/index')
        # 2.check the COOKIES
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        if c_username and c_uid:
            # rewrite the session
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            #return HttpResponse('Logged in already')
            return HttpResponseRedirect('/index')

        return render(request, 'user/login.html')

    # POST deal with the data
    elif request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        # search the username

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print('--login user error %s'%(e))
            return HttpResponse('The username or password is incorrect!')
        
        #check the password
        # use the HASH again to find password
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()

        if password_m != user.password:
            return HttpResponse('The username or password is incorrect!')

        # record the session
        request.session['username'] = username
        request.session['uid'] = user.id

        resp = HttpResponseRedirect('/index')
        # check user if clicked the "remember username" checkbox
        if 'remember' in request.POST:
            resp.set_cookie('username', username, 3600*24*3)
            resp.set_cookie('uid', user.id, 3600*24*3)
        # if yes -> Cookies store [username, uid] time to be 3 days

        return resp


def logout_view(request):
    # delete the sessionid and cookies
    resp = HttpResponseRedirect('/index')
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    # delete COOKIES    
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    #302 return to home page
    return resp