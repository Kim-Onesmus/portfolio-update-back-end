from django.contrib import admin
from .models import AddBlog,AddImage, AddProject,AddReview, ContactUs, buyMeCoffee

@admin.register(buyMeCoffee)
class buyMeCofeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'phone_number', 'status')
    ordering = ('-transaction_date',)

admin.site.register(AddBlog)
admin.site.register(AddImage)
admin.site.register(AddProject)
admin.site.register(AddReview)
admin.site.register(ContactUs)