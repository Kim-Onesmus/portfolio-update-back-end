from django.urls import path
from . import views

urlpatterns = [
    path('', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    path('home', views.Home, name='home'),
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),

    # register, confirmation, validation and callback urls
    path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    path('c2b/confirmation', views.confirmation, name="confirmation"),
    path('c2b/validation', views.validation, name="validation"),
    path('c2b/callback', views.call_back, name="call_back"),

    path('login', views.Login, name='login'),
    path('adminPage', views.adminPage, name='adminPage'),
    path('addBlog', views.addBlog, name='addBlog'),
    path('updateBlog/<str:pk>/', views.updateBlog, name='updateBlog'),
    path('DeleteBlog/<str:pk>/', views.DeleteBlog, name='DeleteBlog'),
    
    path('addImage', views.addImage, name='addImage'),
    path('updateImage/<str:pk>/', views.updateImage, name='updateImage'),
    path('DeleteImage/<str:pk>/', views.DeleteImage, name='DeleteImage'),
    
    path('addProject', views.addProject, name='addProject'),
    path('updateProject/<str:pk>/', views.updateProject, name='updateProject'),
    path('DeleteProject/<str:pk>/', views.DeleteProject, name='DeleteProject'),
    
    path('addReview', views.addReview, name='addReview'),
    path('updateReview/<str:pk>/', views.updateReview, name='updateReview'),
    path('DeleteReview/<str:pk>/', views.DeleteReview, name='DeleteReview'),
    
    path('contact', views.Contact, name='contact'),
    path('logout', views.Logout, name='logout'),
]