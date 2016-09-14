from django.views.generic.edit import CreateView
from django.conf.urls import url, include
from .views import RegisterView

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='accounts_register'),
    url(r'^', include('django.contrib.auth.urls')),
]