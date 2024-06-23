from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import *
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

def get_announcement_bar_instance():
    instance = AnnouncementBar.objects.first()
    if instance and instance.expiration_date and instance.expiration_date < timezone.now():
        # If the instance exists and is expired, return None or handle as needed
        instance = None
    return instance

# Create your views here.
def index(request):
    announcement_bar = get_announcement_bar_instance()
    landing = get_object_or_404(Landing, pk=1)
    categories = Category.objects.prefetch_related('subjects').all()
    why = Why.objects.all()
    team = Team.objects.all()
    now = timezone.now()
    try:
        announcement = Announcement.objects.filter(expiration_date__gt=now).latest('date_time')
    except ObjectDoesNotExist:
        announcement = None
    context = {
        'landing': landing,
        'announcement': announcement,
        'now': now,
        'categories': categories,
        'why': why,
        'teams': team,
        'announcement_bar': announcement_bar,
    }

    return render(request,'enduser/index.html', context)

def announcements(request):
    announcement_bar = get_announcement_bar_instance()
    now = timezone.now()
    try:
        announcements = Announcement.objects.filter(expiration_date__gt=now).all()
    except ObjectDoesNotExist:
        announcements = None
    context = {
        'announcements': announcements,
        'now': now,
        'announcement_bar': announcement_bar,
    }

    return render(request,'enduser/announcements.html', context)

def about(request):
    announcement_bar = get_announcement_bar_instance()
    team = Team.objects.all()

    return render(request,'enduser/about.html', {'teams': team,'announcement_bar': announcement_bar})