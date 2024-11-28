from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='lipa_na_mpesa'),
    
    path('buy_me_coffee/', views.BuyMeCoffee, name='buy_me_cofee'),
    path('check_payment_status', views.CheckPaymentStatus, name='check_payment_status'),

    path('c2b/callback', views.Callback, name="callback"),

    path('log_in', views.Login, name='log_in'),
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