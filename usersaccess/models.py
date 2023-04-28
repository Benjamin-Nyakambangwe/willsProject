from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import hashlib
from tinymce import models as tinymce_models
from simple_history.models import HistoricalRecords

def upload_to(instance, filename):
    return filename.format(filename=filename)

    
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


class TestChange(models.Model):
    will_owner=models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE,blank=True,null=True)
    excutor=models.ForeignKey(User, related_name='witness', on_delete=models.CASCADE,blank=True,null=True)
    lawyer=models.ForeignKey(User, related_name='lawyr', on_delete=models.CASCADE,blank=True,null=True)
    my_field = tinymce_models.HTMLField(blank=True, null=True)
    my_field_hash = models.CharField(max_length=64, blank=True, null=True)
    emails = models.TextField(blank=True, null=True)
    dc_image = models.ImageField(null=True, blank=True, upload_to=upload_to)
    dc_pdf = models.FileField(null=True, blank=True, upload_to=upload_to)
    will_pdf = models.FileField(null=True, blank=True, upload_to=upload_to)
    will_owner_sign = models.CharField(max_length=200, blank=True, null=True)
    executor_sign = models.CharField(max_length=200, blank=True, null=True)
    lawyer_sign = models.CharField(max_length=200, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.will_owner)
        # return str(self.will_owner.username.capitalize() + "'s Will")

    def save(self, *args, **kwargs):
        if self.my_field:
            new_hash = hashlib.sha256(self.my_field.encode('utf-8')).hexdigest()
            if new_hash != self.my_field_hash:
                print('Field Changed')
            else:
                print('Nothing Changed')
            self.my_field_hash = new_hash
        super(TestChange, self).save(*args, **kwargs)





class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_witness = models.BooleanField(blank=True, null=True)