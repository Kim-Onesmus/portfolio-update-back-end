from django.db import models

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
    description = models.TextField(max_length=200)
    
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
    profession = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')
    messange = models.TextField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=200)