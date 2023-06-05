from django.contrib import admin
from .models import AddBlog,AddImage, AddProject,AddReview, ContactUs

# Register your models here.

admin.site.register(AddBlog)
admin.site.register(AddImage)
admin.site.register(AddProject)
admin.site.register(AddReview)
admin.site.register(ContactUs)