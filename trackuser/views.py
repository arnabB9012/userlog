# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from models import User, Login
from datetime import datetime
from django.template import Context
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

def login(request):
	if request.session.get('logged_in', False) == True:
		return HttpResponseRedirect('profile')
	c = Context({})
	c.update(csrf(request))
	if request.GET.get('err', 'false') == 'true':
		c['errormsg'] = 'Login unsuccessful'
	return render_to_response("loginpage.html", c)
def dologin(request):
	try:
		uname = request.POST["username"]
		passw = request.POST["password"]
		u = User.objects.get(username=uname, password=passw)
		l = Login(user = u, loginlast = datetime.now())
		l.save()
		request.session['logged_in'] = True
	        request.session['uid'] = u.id
		return HttpResponseRedirect('profile')
	except (KeyError, User.DoesNotExist, User.MultipleObjectsReturned):
		return HttpResponseRedirect('/?err=true')

def profile(request):
	c = Context({})
	try:
		u = User.objects.get(id=request.session['uid'])
		loginList = Login.objects.filter(user=u)
		return HttpResponse(u.username)
		c['loginList'] = loginList
		c['username'] = u.username
	except KeyError:
		return HttpResponse("Not logged in yet")
	except (User.DoesNotExist, User.MultipleObjectsReturned):
		return HttpResponse("An unknown error occured")
