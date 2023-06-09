from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import wills
from .models import ChangeLog, TestChange
from django.contrib.auth.decorators import login_required
from .forms import wills_form, newWillForm, RegisterForm, RegisterLawyerForm, dCertForm, RegisterExecutorForm, ownerSignWillForm, executorSignWillForm, lawyerSignWillForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from PIL import Image
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMessage
import mimetypes
from django.core.files.base import ContentFile


import os
import io
from django.core.files import File
from django.shortcuts import get_object_or_404
from django.views.generic import View
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from django.conf import settings

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


def register_executor_view(request):
    if request.method == 'POST':
        form = RegisterExecutorForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Registration was successfull'))
            return(redirect('usersaccess:home'))
    else:
        form = RegisterExecutorForm()
    return render(request, 'users_access/register_executor.html', {
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


# @login_required
def edit_will_view(request, id):
    will = TestChange.objects.get(pk=id)
    form = newWillForm(request.POST or None, instance=will)
    if form.is_valid():
        # if will.will_owner_sign is not None:
        #     return redirect('usersaccess:home')
        form.save() 
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
    return render(request, 'users_access/edit_will.html', {'will':will, 'form': form})



# @login_required
def edit_own_will_view(request):
    will = TestChange.objects.get(will_owner=request.user)
    form = newWillForm(request.POST or None, instance=will)
    if form.is_valid():
        # if will.will_owner_sign is not None:
        #     return redirect('usersaccess:home')
        form.save() 
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
    return render(request, 'users_access/edit_will.html', {'will':will, 'form': form})




def handleDC(request, id):
    will = TestChange.objects.get(pk=id)
    form = dCertForm(request.POST or None, request.FILES or None, instance=will)
    if form.is_valid():
        print('form is valid')
        form.save()
        print(will.dc_image)

        #CONVERT THE SAVED DC IMAGE TO PDF
        image_path = os.path.join(settings.MEDIA_ROOT, str(will.dc_image))
        # Open the image file as a binary stream
        with open(image_path, 'rb') as image_file:
            # Create an ImageReader object from the binary stream
            image_reader = ImageReader(image_file)
            # Create a buffer to store the PDF data
            buffer = io.BytesIO()
            # Create a canvas and draw the image onto it
            pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
            pdf_canvas.drawImage(image_reader, 0, 0, width=letter[0], height=letter[1])
            pdf_canvas.save()
            # Get the PDF data from the buffer and save it to the model object
            pdf_file = File(buffer)
            # my_model = TestChange.objects.get(pk=4)
            will.dc_pdf.save('my.pdf', pdf_file)



            my_data = will.my_field
            user = will.will_owner
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'

            template = get_template('users_access/will_pdf.html')
            html = template.render({'my_data': my_data, 'user': user})

            pdf_data = io.BytesIO()
            pdf = pisa.CreatePDF(html, dest=pdf_data)

            if not pdf.err:
                # Reset the pointer to the beginning of the BytesIO object
                pdf_data.seek(0)

                # Save the PDF to the model field
                will.will_pdf.save('mypdf.pdf', ContentFile(pdf_data.getvalue()))

                # Close the BytesIO object to free up memory
                pdf_data.close()


            email_list = will.emails.split(',')
            if len(email_list) == 3:
                email1, email2, email3 = [e.strip() for e in email_list]

            email = EmailMessage(
            'Will Attachment',
            'Attached below is the will for your relative that just died',
            'tbjenu@gmail.com',
            [email1, email2, email3],
            reply_to=['tbjenu@gmail.com'],
        )
            file = will.will_pdf
            print(f"file type: {type(file)}, file value: {file}")
            if file:
                content_type, encoding = mimetypes.guess_type(file.name)
                email.attach(file.name, file.read(), content_type)
            email.send()
            print('email sent')

        mymodel = TestChange.objects.filter(lawyer=request.user)
        if mymodel.exists():
            print(mymodel[0].lawyer)
            return render(request, 'users_access/landing_page.html', {'clients': mymodel})
        else:
            
            return render(request, 'users_access/landing_page.html', {})
    print(form.errors)
    print('form is not valid')
    return render(request, 'users_access/handle_dc.html', {'will':will, 'form': form})




class ImageToPDFView(View):
    def get(self, request):

        image_path = os.path.join(settings.MEDIA_ROOT, 'guest_posting_image.jpg')
        # Open the image file as a binary stream
        with open(image_path, 'rb') as image_file:
            # Create an ImageReader object from the binary stream
            image_reader = ImageReader(image_file)
            # Create a buffer to store the PDF data
            buffer = io.BytesIO()
            # Create a canvas and draw the image onto it
            pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
            pdf_canvas.drawImage(image_reader, 0, 0, width=letter[0], height=letter[1])
            pdf_canvas.save()
            # Get the PDF data from the buffer and save it to the model object
            pdf_file = File(buffer)
            my_model = TestChange.objects.get(pk=2)
            my_model.dc_pdf.save('my.pdf', pdf_file)
            # Return the PDF file as an attachment for download
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=my.pdf'
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


@login_required
def scheduleCall(request, id):
    will = TestChange.objects.get(pk=id)
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        time = request.POST.get('time')
        emailAcc = will.will_owner.email
        emailAcc2 = will.excutor.email
        email = EmailMessage(
            'Will Online Schedule',
            'Please attend the WILL review and sign on\t' + time + ' and use the room name\t' + room_name,
            'will',
            [emailAcc, emailAcc2],
            reply_to=['tbjenu@gmail.com'],
        )
        email.send()
        print(will.will_owner.email)
        print('email sent')
        return redirect('usersaccess:home')
    return render(request, 'users_access/schedule_call.html', {will: 'will'})


@login_required
def new_lobby(request):
    
    return render(request, 'base/lobby.html', {})

# def room(request):
#     return render(request, 'base/room.html')




def executor_sign_view(request):
    will = TestChange.objects.get(excutor=request.user)
    form = executorSignWillForm(request.POST or None, instance=will)
    if form.is_valid():
        form.save() 
        return redirect('usersaccess:home')
    return render(request, 'users_access/executor_sign.html', {'will':will, 'form': form})


def owner_sign_view(request):
    will = TestChange.objects.get(will_owner=request.user)
    form = ownerSignWillForm(request.POST or None, instance=will)
    if form.is_valid():
        form.save() 
        return redirect('usersaccess:home')
    return render(request, 'users_access/owner_sign.html', {'will':will, 'form': form})


def lawyer_sign_view(request, id):
    will = TestChange.objects.get(pk=id)
    form = lawyerSignWillForm(request.POST or None, instance=will)
    if form.is_valid():
        form.save() 
        return redirect('usersaccess:home')
    return render(request, 'users_access/lawyer_sign.html', {'will':will, 'form': form})


import requests
from django.shortcuts import render
from django.http import HttpResponse

def image_to_text(request, id):
    will = TestChange.objects.get(pk=id)
    if request.method == 'POST':
        # Get the image file from the POST request
        image_file = request.FILES.get('image_file')
        if not image_file:
            return HttpResponse('No image file provided.')
        
        # Set the OCR Space API endpoint and parameters
        api_url = 'https://api.ocr.space/parse/image'
        api_key = 'K81252015588957'
        payload = {
            'apikey': api_key,
            'isOverlayRequired': False,
            'language': 'eng', # Specify the language of the text in the image
        }
        
        # Send the image file to OCR Space for processing
        response = requests.post(api_url, files={'image': image_file}, data=payload)
        if response.status_code != 200:
            return HttpResponse('Error processing image.')
        
        # Extract the text from the OCR Space response
        response_data = response.json()
        if response_data['OCRExitCode'] != 1:
            return HttpResponse('Error extracting text from image.')
        else:
            text = response_data['ParsedResults'][0]['ParsedText']
            will.dc_text = text
            will.save()

            my_set = {"PLACE OF DEATH", "place of death", "CERTIFICATE OF DEATH", "certificate of death", "DATE OF DEATH","date of death"}

            if any(substring in will.dc_text for substring in my_set):
                print('VALID DEATH CERTIFICATE')
                my_data = will.my_field
                user = will.will_owner
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'

                template = get_template('users_access/will_pdf.html')
                html = template.render({'my_data': my_data, 'user': user})

                pdf_data = io.BytesIO()
                pdf = pisa.CreatePDF(html, dest=pdf_data)

                if not pdf.err:
                    # Reset the pointer to the beginning of the BytesIO object
                    pdf_data.seek(0)

                    # Save the PDF to the model field
                    will.will_pdf.save('mypdf.pdf', ContentFile(pdf_data.getvalue()))

                    # Close the BytesIO object to free up memory
                    pdf_data.close()
                
                email_list = will.emails.split(',')
                if len(email_list) == 3:
                    email1, email2, email3 = [e.strip() for e in email_list]

                email = EmailMessage(
                'Will Attachment',
                'Attached below is the will for your relative that just died',
                'tbjenu@gmail.com',
                [email1, email2, email3],
                reply_to=['tbjenu@gmail.com'],
            )
                file = will.will_pdf
                print(f"file type: {type(file)}, file value: {file}")
                if file:
                    content_type, encoding = mimetypes.guess_type(file.name)
                    email.attach(file.name, file.read(), content_type)
                email.send()
                print('email sent')
                messages.success(request, ('VALID DEATH CERTIFICATE, ATTACHMENT SENT TO RELATIVES'))

            else:
                print('INVALID DEATH CERTIFICATE')
                print(will.dc_text)
                messages.success(request, ('INVALID DEATH CERTIFICATE'))
                return redirect('usersaccess:home')

            # return HttpResponse(text)
            return redirect('usersaccess:home')
    
    return render(request, 'users_access/image_to_text.html')