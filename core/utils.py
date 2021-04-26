from django.db.models import F
from django.urls import reverse, NoReverseMatch

from core.models import RequestCounter


def set_request_count(request):
    """
    It increases the count on request or create the obj
    for the first time. Being called from multiple places
    so decided to factor this as func
    """
    try:
        # getting admin index url
        admin_index = reverse('admin:index')
    except NoReverseMatch:
        return
    if request.path.startswith(admin_index):
        # if url starts with /admin we return there
        # cause we want to set count of apis request only not the admin panel
        return

    obj = RequestCounter.objects.first()
    # fetch the counter(only one is there) object
    # and update by +1
    if obj:
        RequestCounter.objects.update(count=F('count')+1)
    # if there is not RequestCounter obj, create one
    else:
        RequestCounter.objects.create(count=1)
