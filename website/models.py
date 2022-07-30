from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AuditFields(models.Model):

    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='%(class)s_created_by',blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    modified_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='%(class)s_modified_by',blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True,blank=True,null=True)
    is_valid = models.BooleanField(default=True)
        
    class Meta:
        abstract = True

class ToDos(AuditFields):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, null=False)
    todo = models.TextField(blank=False, null=False)
    is_completed = models.BooleanField(default=False)
        
    class Meta:
        db_table = "todos"
        app_label = 'website'

    def __str__(self):
        return self.user.username