import logging

from django.db import models, IntegrityError
from django.db.models.signals import pre_save
from django.dispatch import receiver

logger = logging.getLogger('core')


class RequestCounter(models.Model):
    """
    Create only one object of this model to store count of request
    """
    count = models.PositiveBigIntegerField(default=0)


@receiver(pre_save, sender=RequestCounter)
def borrower_pre_save(instance, **kwargs):
    """
    Stopping multiple obj creation of this counter
    """
    obj_count = RequestCounter.objects.count()

    if obj_count > 0:
        logger.error(
            "Can not create object another Request count obj is already there"
        )
        raise IntegrityError("Another Request count obj is already there")
