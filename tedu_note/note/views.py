from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Note

# Create your views here.
#check the login status:
def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
            if not c_username or not c_uid:
                return HttpResponseRedirect('/user/login')
            else:
                # save the session again:
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request, *args, **kwargs)
    return wrap


@check_login
def add_note(request):

    if request.method == 'GET':
        return render(request, 'note/add_note.html')

    elif request.method == 'POST':
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']

        Note.objects.create(title=title, content=content, user_id=uid)

        return HttpResponseRedirect('/note/all')

@check_login
def list_view(request):
    username = request.session['username']
    uid = request.session['uid']
    notes = Note.objects.filter(user_id=uid)    
    return render(request, 'note/list_note.html', locals())

