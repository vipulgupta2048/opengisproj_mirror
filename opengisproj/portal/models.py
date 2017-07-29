from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class gis_data(models.Model):
    created_on = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User)

    class Meta:
        db_table = "gis_data"

class gis_data_meta(models.Model):
    key = models.CharField(max_length=100)
    value = models.TextField()
    data = models.ForeignKey(gis_data,on_delete=models.CASCADE)
    
    class Meta:
        db_table = "gis_data_meta"

class options(models.Model):
    option_name = models.CharField(max_length=100)
    value = models.TextField()
    is_removable = models.BooleanField(default=False)
    
    class Meta:
        db_table = "options"
