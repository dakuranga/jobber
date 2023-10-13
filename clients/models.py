from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    website = models.URLField(max_length=200)
    about_client_attachment = models.FileField(upload_to='About_clients/')
    hq = models.CharField(max_length=200,blank=True, null=True)
    office = models.CharField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    