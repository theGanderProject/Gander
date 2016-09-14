from django.conf.urls import url
from django.contrib.auth.decorators import login_required


from . import views

urlpatterns = [
    url(r'^submit/$', login_required(views.SubmitView.as_view()), name='audio_submit'),
    url(r'^view/(?P<pk>[0-9]+)/$', views.ViewView.as_view(), name='audio_view'),
]