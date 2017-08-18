from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class data_groups(models.Model):
    name = models.CharField(max_length=100)
    is_removable = models.BooleanField(default=True)
    class Meta:
        db_table = "data_groups"

class gis_data(models.Model):
    created_on = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User)
    data_group = models.ForeignKey(data_groups)

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
    data_group = models.ForeignKey(data_groups, null=True)
    
    class Meta:
        db_table = "options"

class uploads(models.Model):
    file_name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    file_ref = models.FileField(upload_to='uploads/%Y/%m/%d')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_meta = models.CharField(max_length=150)
    class Meta:
        db_table = "uploads"

class shapefiles(models.Model):
    shape_name = models.CharField(max_length=256)
    shp_file = models.ForeignKey(uploads, related_name='shp_file', on_delete=models.CASCADE)
    dbf_file = models.ForeignKey(uploads, related_name='dbf_file', on_delete=models.CASCADE)
    shx_file = models.ForeignKey(uploads, related_name='shx_file',on_delete=models.CASCADE)

    class Meta:
        db_table = "shapefiles"