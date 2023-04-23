from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import wills
from .models import ChangeLog, TestChange
from django.contrib.auth.decorators import login_required
from .forms import wills_form, newWillForm, RegisterForm, RegisterLawyerForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from PIL import Image
from django.contrib.auth.forms import UserCreationForm


from django.template.loader import get_template
from xhtml2pdf import pisa



def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('usersaccess:home')
        else:
            messages.success(request, ('there was an error login'))
            return redirect('usersaccess:login')
    else:
        return render(request, 'users_access/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, ('you were logged out'))
    # return render(request, 'users_access/login.html')
    return redirect('usersaccess:login')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Registration was successfull'))
            return(redirect('usersaccess:home'))
    else:
        form = RegisterForm()
    return render(request, 'users_access/register.html', {
        'form':form,
    })


def register_lawyer_view(request):
    if request.method == 'POST':
        form = RegisterLawyerForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Registration was successfull'))
            return(redirect('usersaccess:home'))
    else:
        form = RegisterLawyerForm()
    return render(request, 'users_access/register_lawyer.html', {
        'form':form,
    })



@login_required
def landing_view(request):
    if request.user.is_staff:
        mymodel = TestChange.objects.filter(lawyer=request.user)
        if mymodel.exists():
            # history = mymodel.history.all()
            print(mymodel[0].lawyer)
            # return render(request, 'my_template.html', {'mymodel': mymodel, 'history': history})
            return render(request, 'users_access/landing_page.html', {'clients': mymodel})
        else:
            return render(request, 'users_access/landing_page.html', {})
    else:
        try:
            mymodel = TestChange.objects.get(will_owner=request.user)
            history = mymodel.history.all()
            print(history)
            # return render(request, 'my_template.html', {'mymodel': mymodel, 'history': history})
            return render(request, 'users_access/landing_page.html', {'history': history, 'will_model': mymodel})
            
        except TestChange.DoesNotExist:
            return render(request, 'users_access/landing_page.html', {})

            
        





# @login_required
def create_new_will(request):
    if request.method != 'POST':
        # form = wills_form()
        form = newWillForm()
        context = {'form': form}
        return render(request, 'users_access/new_will.html',context)
    else:
        form = newWillForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            changelog = ChangeLog.objects.filter(will_owner=request.user)
            mymodel = TestChange.objects.get(will_owner=request.user)
            history = mymodel.history.all()
            return render(request, 'users_access/landing_page.html', {'data': changelog, 'history': history})
            # landing_view(request)def image_to_pdf(request):


def image_to_pdf(request):
    # Open the image file
    img = Image.open('path/to/image.jpg')
    
    # Create a new PDF file and canvas
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="image.pdf"'
    pdf_canvas = canvas.Canvas(response)
    
    # Get the size of the image and calculate the aspect ratio
    width, height = img.size
    aspect_ratio = height / width
    
    # Set the size of the PDF canvas to match the image size
    pdf_canvas.setPageSize((width, height))
    
    # Draw the image on the PDF canvas
    pdf_canvas.drawImage(img, 0, 0, width, height)
    
    # Save the PDF file to a model field
    my_model = MyModel.objects.create()
    my_model.my_file_field.save('image.pdf', response)
    
    # Close the canvas
    pdf_canvas.save()
    
    return response




@login_required()
def render_will_view(request):
    user= request.user
    # get the HTML string from the model
    mymodel = TestChange.objects.get(will_owner=request.user)
    my_data = mymodel.my_field
    
    # render the HTML string as a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    template = get_template('users_access/will_pdf.html')
    html = template.render({'my_data': my_data, 'user': user})
    pdf = pisa.CreatePDF(html, dest=response)
    
    # if PDF creation was successful, return the response
    if not pdf.err:
        return response
    
    # if PDF creation failed, return an error message
    return HttpResponse('Error creating PDF: %s' % pdf.err)







