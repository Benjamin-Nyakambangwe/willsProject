from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import wills
from .models import ChangeLog, TestChange
from django.contrib.auth.decorators import login_required
from .forms import wills_form, newWillForm



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users_access:home')
        else:
            return HttpResponse("<h1>Access Denied</h1>")
            # Return an 'invalid login' error message.
    return render(request, 'users_access/login.html')

@login_required
def landing_view(request):
    changelog = ChangeLog.objects.filter(will_owner=request.user)
    mymodel = TestChange.objects.get(will_owner=request.user)
    history = mymodel.history.all()
    print(history[1].lawyer)
    # return render(request, 'my_template.html', {'mymodel': mymodel, 'history': history})
    return render(request, 'users_access/landing_page.html', {'data': changelog, 'history': history})


# @login_required
def create_new_will(request):
    if request.method != 'POST':
        # form = wills_form()
        form = newWillForm()
        context = {'form': form}
        return render(request, 'users_access/new_will.html',context)
    else:
        form = newWillForm(data=request.POST)
        if form.is_valid():
            form.save() 
            changelog = ChangeLog.objects.filter(will_owner=request.user)
            mymodel = TestChange.objects.get(will_owner=request.user)
            history = mymodel.history.all()
            return render(request, 'users_access/landing_page.html', {'data': changelog, 'history': history})
            # landing_view(request)
