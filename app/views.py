from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from .models import AddBlog, AddReview, AddImage, AddProject, ContactUs
from .forms import BlogForm, ImageForm, ProjectForm, ReviewForm


# Create your views here.

def Home(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        form = ContactUs.objects.create(name=name, email=email, subject=subject, message=message)
        form.save()
        messages.info(request, 'Submitted successifully, we will get back to you soon')
        return redirect('/')

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

    return render(request, 'app/index.html', context)

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