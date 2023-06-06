from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from .models import AddBlog, AddReview, AddImage, AddProject, ContactUs, MpesaPayment, Pay
from .forms import BlogForm, ImageForm, ProjectForm, ReviewForm
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def getAccessToken(request):
    consumer_key = 'gvmRX9peDcWeYTRRHBrOZh42jITwtl4N'
    consumer_secret = 'Vsmx9HaLqGPdAhPQ'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    r = request.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def lipa_na_mpesa_online(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        amount = request.POST.get('amount')

        if number and amount:
            # Handle M-Pesa payment functionality
            if len(number) == 12 and number.startswith('2547'):
                access_token = MpesaAccessToken.validated_mpesa_access_token
                api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
                headers = {"Authorization": "Bearer %s" % access_token}
                payload = {
                    "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
                    "Password": LipanaMpesaPpassword.decode_password,
                    "Timestamp": LipanaMpesaPpassword.lipa_time,
                    "TransactionType": "CustomerPayBillOnline",
                    "Amount": amount,
                    "PartyA": number,
                    "PartyB": LipanaMpesaPpassword.Business_short_code,
                    "PhoneNumber": number,
                    "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
                    "AccountReference": "KimTech",
                    "TransactionDesc": "Buy me Coffee"
                }

                response = requests.post(api_url, json=payload, headers=headers)
                messages.success(request, 'Submitted successfully')
                return redirect('/')
            else:
                messages.error(request, f"Phone Number '{number}' is not valid or in the wrong format")
                return redirect('/')
        else:
            # Handle contact form submission
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            form = ContactUs.objects.create(name=name, email=email, subject=subject, message=message)
            form.save()
            messages.info(request, 'Submitted successfully. We will get back to you soon.')
            return redirect('/')

    image = AddImage.objects.all()
    project = AddProject.objects.all()
    blog = AddBlog.objects.all()
    contact = ContactUs.objects.all()
    review = AddReview.objects.all()

    context = {
        'image': image,
        'project': project,
        'blog': blog,
        'contact': contact,
        'review': review
    }
    return render(request, 'app/index.html', context)

@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://mydomain.com/confirmation",
               "ValidationURL": "https://mydomain.com/validation"}
    response = requests.post(api_url, json=options, headers=headers)

    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)

    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],

    )
    payment.save()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))

def adminPage(request):
    image = AddImage.objects.all()
    project = AddProject.objects.all()
    blog = AddBlog.objects.all()
    contact = ContactUs.objects.all()
    review = AddReview.objects.all()
        
    context = {
        'image':image,
        'project':project,
        'blog':blog,
        'contact':contact,
        'review':review
    }
    return render(request, 'app/admin.html', context)

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password,)
                
        if user is not None:
            auth.login(request, user)
            return redirect('adminPage')
        else:
            messages.error(request, 'Invalid details')
            return redirect('login')
    else:
        return render(request, 'app/login.html')
    return render(request, 'app/login.html')

def addBlog(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
    context = {'form':form}
    return render(request, 'app/add_blog.html', context)

def updateBlog(request, pk):
    blog = AddBlog.objects.get(id=pk)
    form = BlogForm(instance=blog)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
    context = {'form':form}
    return render(request, 'app/add_blog.html', context)

def addImage(request):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
    context = {'form':form}
    return render(request, 'app/add_image.html', context)

def updateImage(request, pk):
    image = AddImage.objects.get(id=pk)
    form = ImageForm(instance=image)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
    context = {'form':form}
    return render(request, 'app/add_image.html', context)

def addProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
    context = {'form':form}
    return render(request, 'app/add_project.html', context)

def updateProject(request, pk):
    project = AddProject.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
    context = {'form':form}
    return render(request, 'app/add_project.html', context)

def addReview(request):
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
    context = {'form':form}
    return render(request, 'app/add_review.html', context)

def updateReview(request, pk):
    review = AddReview.objects.get(id=pk)
    form = ReviewForm(instance=review)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
    context = {'form':form}
    return render(request, 'app/add_review.html', context)

def Contact(request):
    contact = ContactUs.objects.all()
        
    context = {
        'contact':contact,
    }
    return render(request, 'app/contact.html', context)


def Logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
        messages.info(request, 'You have been loged out')
    return render(request, 'app/logout.html')

def DeleteBlog(request, pk):
    blog = AddBlog.objects.get(id=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('adminPage')
    
    context = {
        'blog':blog,
    }
    return render(request, 'app/delete.html', context)

def DeleteImage(request, pk):
    image = AddImage.objects.get(id=pk)
    if request.method == 'POST':
        image.delete()
        return redirect('adminPage')
    
    context = {
        'image':image,
    }
    return render(request, 'app/delete.html', context)

def DeleteProject(request, pk):
    project = AddProject.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('adminPage')
    
    context = {
        'project':project,
    }
    return render(request, 'app/delete.html', context)

def DeleteReview(request, pk):
    review = AddReview.objects.get(id=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('adminPage')
    
    context = {
        'review':review,
    }
    return render(request, 'app/delete.html', context)