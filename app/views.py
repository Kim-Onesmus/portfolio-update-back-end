from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth, User
from django.contrib import messages
from .models import AddBlog, AddReview, AddImage, AddProject, ContactUs, buyMeCoffee
from .forms import BlogForm, ImageForm, ProjectForm, ReviewForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import os, requests, base64, json
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import time
from datetime import datetime
from django.core.cache import cache
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import send_mail

load_dotenv()


def AccessToken(request):
    client_id = os.getenv('KCB_CONSUMER_KEY')
    client_secret = os.getenv('KCB_CONSUMER_SECRET')
    auth_value = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    url = f"{os.getenv('KCB_BASE_URL')}/token?grant_type=client_credentials"
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth_value}'
    }
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        token = response.json().get('access_token')
        return token 
    return JsonResponse({'error': 'Unable to retrieve access token'}, status=500)


def Index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        form = ContactUs.objects.create(name=name, email=email, subject=subject, message=message)
        form.save()
        
                
        subject = "New Portfolio Contact"
        message = f'{name}\n\n{email}\n\n{form.subject}\n\n{message}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['Kimonesmuske@gmail.com',]

        send_mail(subject, message, from_email, recipient_list)
        
        messages.info(request, 'Submitted successfully. I will get back to you soon.')
        return redirect('/')
    

    image = [
        {
            'id': img.id,
            'title': img.tittle,
            'image_url': default_storage.url(img.image.name)  # Use full S3 URL
        }
        for img in AddImage.objects.all()
    ]
    project = [
        {
            'id': proj.id,
            'name': proj.name,
            'title': proj.tittle,
            'image_url': default_storage.url(proj.image.name)  # Use full S3 URL
        }
        for proj in AddProject.objects.all()
    ]
    blog = [
        {
            'id': b.id,
            'title': b.tittle,
            'date': b.date,
            'image_url': default_storage.url(b.image.name),  # Use full S3 URL
            'description': b.description
        }
        for b in AddBlog.objects.all()
    ]
    reviews = [
        {
            'id': r.id,
            'name': r.name,
            'profession': r.profession,
            'image_url': default_storage.url(r.image.name),  # Use full S3 URL
            'message': r.messange,
            'rating': r.rating,
            'star_range': list(range(r.rating)),
            'complement_range': list(range(5 - r.rating)),
        }
        for r in AddReview.objects.filter(is_approved=True)
    ]

    # Prepare data for caching
    cached_data = {
        'image': image,
        'project': project,
        'blog': blog,
        'review': reviews,
    }

    return render(request, 'app/index.html', {'cached_data': cached_data})

def ReviewForms(request):
    if request.method == 'POST':
        name = request.POST['name']
        profession = request.POST['profession']
        image = request.FILES['image']
        rating = request.POST['rating']
        message = request.POST['message']
        
        review_details = AddReview.objects.create(
            name=name,
            profession=profession,
            image=image,
            rating=rating,
            messange=message
        )
        review_details.save()
        
        subject = "New Portfolio Review"
        message = f'{name}\n\n{profession}\n\n{rating}\n\n{message}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['Kimonesmuske@gmail.com',]

        send_mail(subject, message, from_email, recipient_list)
        
        messages.success(request, 'Review Submitted Successfully')
        return redirect('/')

def BuyMeCoffee(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            number = data.get('number')
            amount = data.get('amount')

            if not number or not amount:
                return JsonResponse({'status': 400, 'message': 'Number and amount are required.'}, status=400)

            if len(number) != 12 or not number.startswith('2547'):
                return JsonResponse({'status': 400, 'message': f"Phone Number '{number}' is not valid or in the wrong format."}, status=400)

            user = buyMeCoffee(
                phone_number=number,
                amount=amount,
            )
            access_token = AccessToken(request)
            url = f"{os.getenv('KCB_BASE_URL')}/mm/api/request/1.0.0/stkpush"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            payload = {
                "phoneNumber": number,
                "amount": amount,
                "invoiceNumber": "7932911-Kim_Technologies",
                "sharedShortCode": True,
                "orgShortCode": "",
                "orgPassKey": "",
                "callbackUrl": f"{request.build_absolute_uri(reverse('callback'))}?user_id={user.id}",
                "transactionDescription": "Buy me Coffee"
            }
            print('User ID', user.id)
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json().get('response', {})
            print('Response', response.json())

            if response.status_code == 200 and response_data.get('ResponseCode') == '0':
                user.save()
                return JsonResponse({
                    'status': 200,
                    'message': '📲 STK Push Sent! ✅ Check your 📱 phone to complete the payment. 💳',
                    'id': user.id
                })
            else:
                return JsonResponse({
                    'status': 500,
                    'message': response_data.get('ResponseDescription', 'An error occured while initiating payment, Please try agein later!!.')
                })

        except json.JSONDecodeError:
            return JsonResponse({'status': 400, 'message': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 500, 'message': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def CheckPayment(request):
    user__id = request.GET.get('user_id')
    if not user__id:
        return JsonResponse({'status': 400, 'message': 'Payment ID is required...'})

    try:
        pay = buyMeCoffee.objects.get(id=user__id)
    except buyMeCoffee.DoesNotExist:
        return JsonResponse({'status': 404, 'message': 'Payment record not found.'})
    
    result_code = int(pay.result_code) if pay.result_code is not None else None
    
    if result_code is None:
        return JsonResponse({
            'status': 202, 
            'message': pay.result_desc,
        })
    elif result_code == 0:
        return JsonResponse({'status': 200, 'message': pay.result_desc})
    else:
        return JsonResponse({'status': 201, 'message': pay.result_desc})



@csrf_exempt
def Callback(request):
    print('Callback received, Processing data')
    if request.method == "POST":
        try:
            user_id = request.GET.get("user_id")
            print('User Id', user_id)
            if not user_id:
                return JsonResponse({"error": "User id not provided in callback URL"}, status=400)
            
            callback_data = json.loads(request.body)
            print('Callback Data', callback_data)

            stk_callback = callback_data.get("Body", {}).get("stkCallback", {})
            result_code = stk_callback.get("ResultCode", None)
            result_desc = stk_callback.get("ResultDesc", "")
            merchant_request_id = stk_callback.get("MerchantRequestID", "")
            checkout_request_id = stk_callback.get("CheckoutRequestID", "")
            callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])

            amount = None
            receipt_number = None
            transaction_date = None
            phone_number = None

            for item in callback_metadata:
                name = item.get("Name")
                value = item.get("Value", None)
                if name == "Amount":
                    amount = value
                elif name == "MpesaReceiptNumber":
                    receipt_number = value
                elif name == "TransactionDate":
                    transaction_date = value
                elif name == "PhoneNumber":
                    phone_number = value


            if result_code == 0:
                pay = buyMeCoffee.objects.get(id=user_id)
                pay.receipt_number = receipt_number
                pay.merchant_request_id = merchant_request_id
                pay.checkout_request_id = checkout_request_id
                pay.result_desc = result_desc
                pay.result_code = result_code
                pay.status = 'Paid'
                pay.save()
                return JsonResponse({
                    'status': 200,
                    'message': 'Payment made successfully. Thank you for helping make my dreams a reality',
                })
            else:
                pay = buyMeCoffee.objects.get(id=user_id)
                pay.merchant_request_id = merchant_request_id
                pay.checkout_request_id = checkout_request_id
                pay.result_desc = result_desc
                pay.result_code = result_code
                pay.save()
                return JsonResponse({
                    'status': 500,
                    'message': f'{result_desc}',
                })
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)




@login_required(login_url='log_in')
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
            return redirect('log_in')
    else:
        return render(request, 'app/login.html')
    return render(request, 'app/login.html')

@login_required(login_url='log_in')
def addBlog(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
    context = {'form':form}
    return render(request, 'app/add_blog.html', context)

@login_required(login_url='log_in')
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

@login_required(login_url='log_in')
def addImage(request):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
    context = {'form':form}
    return render(request, 'app/add_image.html', context)

@login_required(login_url='log_in')
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

@login_required(login_url='log_in')
def addProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
    context = {'form':form}
    return render(request, 'app/add_project.html', context)

@login_required(login_url='log_in')
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

@login_required(login_url='log_in')
def addReview(request):
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
    context = {'form':form}
    return render(request, 'app/add_review.html', context)

@login_required(login_url='log_in')
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

@login_required(login_url='log_in')
def Contact(request):
    contact = ContactUs.objects.all()
        
    context = {
        'contact':contact,
    }
    return render(request, 'app/contact.html', context)


@login_required(login_url='log_in')
def Logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
        messages.info(request, 'You have been loged out')
    return render(request, 'app/logout.html')

@login_required(login_url='log_in')
def DeleteBlog(request, pk):
    blog = AddBlog.objects.get(id=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('adminPage')
    
    context = {
        'blog':blog,
    }
    return render(request, 'app/delete.html', context)

@login_required(login_url='log_in')
def DeleteImage(request, pk):
    image = AddImage.objects.get(id=pk)
    if request.method == 'POST':
        image.delete()
        return redirect('adminPage')
    
    context = {
        'image':image,
    }
    return render(request, 'app/delete.html', context)

@login_required(login_url='log_in')
def DeleteProject(request, pk):
    project = AddProject.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('adminPage')
    
    context = {
        'project':project,
    }
    return render(request, 'app/delete.html', context)

@login_required(login_url='log_in')
def DeleteReview(request, pk):
    review = AddReview.objects.get(id=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('adminPage')
    
    context = {
        'review':review,
    }
    return render(request, 'app/delete.html', context)