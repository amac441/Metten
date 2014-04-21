from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

def login(request):
	c={}
	c.update(csrf(request))

	form = AuthenticationForm

	return render_to_response('login.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request,user)  #set state or auth object
		return HttpResponseRedirect('/5years')  #change this to some other site
	else:
		return HttpResponseRedirect('/invalid')

def loggedin(request):
	return render_to_response('/5years', {'full_name':request.user.username})

def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	auth.logout(request)
	return render_to_response('index.html')

def register_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/5years')

	args = {}
	args.update(csrf(request))
	args['form'] = UserCreationForm()
	return render_to_response('register.html', args)