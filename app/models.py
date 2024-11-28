from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import random, string

PAY_STATUS = (
    ('Unpaid', 'Unpaid'),
    ('Paid', 'Paid')
)

# Create your models here.
def generate_order_id():
    while True:
        unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        if not buyMeCoffee.objects.filter(id=unique_id).exists():
            return unique_id
 
class buyMeCoffee(models.Model):
    id = models.CharField(primary_key=True, max_length=15, default=generate_order_id, editable=False)
    phone_number = models.CharField(max_length=20)
    amount = models.CharField(max_length=20)
    receipt_number = models.CharField(max_length=20, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    merchant_request_id = models.CharField(max_length=200, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, choices=PAY_STATUS, default='Unpaid')


IMAGE = {
    ('top','Top Image'),
    ('about','About Image'),
}

PROJECT = {
    ('graphic_design','Graphic Design'),
    ('development', 'Web Development'),
    ('web_design', 'Web Design'),
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
      
    
    
