from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, Select
from django.contrib.auth.models import User
from .models import AddBlog, AddImage, AddProject, AddReview
from django import forms

class BlogForm(forms.ModelForm):
    class Meta:
        model = AddBlog
        fields = '__all__'
        widgets = {
        'tittle': forms.TextInput(attrs={'class': 'form-control'}),
        'date': forms.DateInput(attrs={'class': 'form-control'}),
        'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = AddImage
        fields = '__all__'
        widgets = {
        'ttttle': forms.Select(attrs={'class': 'form-control'}),
        'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = AddProject
        fields = '__all__'
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'tittle': forms.Select(attrs={'class': 'form-control'}),
        'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = AddReview
        fields = '__all__'
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'profession': forms.TextInput(attrs={'class': 'form-control'}),
        'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'messange': forms.Textarea(attrs={'class': 'form-control'}),
        }