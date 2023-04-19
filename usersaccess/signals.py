from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import hashlib
from usersaccess.models import wills, ChangeLog

@receiver(post_save, sender=wills)
def pre_save_my_model(sender, instance, **kwargs):
    try:
        old_instance = wills.objects.get(pk=instance.pk)
        instance.__hash_before_save = hashlib.sha256(str(old_instance).encode('utf-8')).hexdigest()
    except wills.DoesNotExist:
        old_instance = None
        instance.__hash_before_save = hashlib.sha256(str(instance).encode('utf-8')).hexdigest()


@receiver(pre_save, sender=wills)
def post_save_my_model(sender, instance, **kwargs):
    # if hasattr(instance, '__hash_before_save')
    old_instance = wills.objects.get(pk=instance.pk)
    if hashlib.sha256(str(old_instance).encode('utf-8')).hexdigest() != hashlib.sha256(str(instance).encode('utf-8')).hexdigest():
        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(old_instance, field_name)
            new_value = getattr(instance, field_name)
            if old_value != new_value:
                ChangeLog.objects.create(
                    model_name=sender.__name__,
                    record_id=old_instance.pk,
                    field_name=field_name,
                    old_value=str(old_value),
                    new_value=str(new_value),
                    will_owner=instance.will_owner,
                )
    else:
        print("they are same")

@receiver(pre_delete, sender=wills)
def pre_delete_my_model(sender, instance, **kwargs):
    ChangeLog.objects.create(
        model_name=sender.__name__,
        record_id=instance.pk,
        field_name='__all__',
        old_value=str(instance),
        new_value='',
        will_owner= instance.will_owner,
    )
