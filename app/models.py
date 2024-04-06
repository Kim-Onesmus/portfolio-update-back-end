from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
IMAGE = {
    ('top','Top Image'),
    ('about','About Image'),
}

PROJECT = {
    ('design','Design'),
    ('development', 'Development'),
}
class AddBlog(models.Model):
    tittle = models.CharField(max_length=200)
    date = models.DateField()
    image = models.ImageField(upload_to='media/')
    description = models.TextField(max_length=500)
    
    def __str__(self):
        return self.tittle
    
class AddImage(models.Model):
    tittle = models.CharField(max_length=200, choices=IMAGE)
    image = models.ImageField(upload_to='media/')
    
    def __str__(self):
        return self.tittle
    
    
class AddProject(models.Model):
    name = models.CharField(max_length=200)
    tittle = models.CharField(max_length=200, choices=PROJECT)
    image = models.ImageField(upload_to='media/')
    
    def __str__(self):
        return self.name
    
    
class AddReview(models.Model):
    name = models.CharField(max_length=200)
    profession = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='media/')
    messange = models.TextField(max_length=1000)
    rating = models.PositiveBigIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    def __str__(self):
        return self.name
    
    
class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=200)
    
class Pay(models.Model):
    number = models.PositiveBigIntegerField(max_length=13)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

   
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# M-pesa Payment models

class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'


class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'


class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.first_name    
    
    
