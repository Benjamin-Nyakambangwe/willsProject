from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import hashlib
from tinymce import models as tinymce_models

# Create your models here.

# Create your models here.
class wills(models.Model):
    """register of wills"""
    will_owner=models.ForeignKey(User, related_name='will_owner', on_delete=models.CASCADE,blank=True,null=True)
    excutor=models.ForeignKey(User, related_name='excutor', on_delete=models.CASCADE,blank=True,null=True)
    lawyer=models.ForeignKey(User, related_name='lawyer', on_delete=models.CASCADE,blank=True,null=True)
    will=tinymce_models.HTMLField()
    hash_value = models.CharField(max_length=64, blank=True)

    class Meta:
        verbose_name_plural="Will"

    def __str__(self):
        return str(self.will)

    def save(self, *args, **kwargs):
        serialized_data = str(self.will) + str(self.hash_value)
        hash_object = hashlib.sha256(serialized_data.encode('utf-8'))
        self.hash_value = hash_object.hexdigest()
        super(wills, self).save(*args, **kwargs)

class ChangeLog(models.Model):
    model_name = models.CharField(max_length=255)
    record_id = models.IntegerField()
    field_name = models.CharField(max_length=255)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    will_owner=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class test(models.Model):
    name =  models.CharField(max_length=255)
    surname =  models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)