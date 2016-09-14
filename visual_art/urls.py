from django.conf.urls import url
from django.contrib.auth.decorators import login_required


from . import views

urlpatterns = [
    url(r'^submit/$', login_required(views.SubmitView.as_view()), name='art_submit'),
    url(r'^view/(?P<pk>[0-9]+)/$', views.ViewView.as_view(), name='art_view'),
    url(r'^view/(?P<pk>[0-9]+)/favorite$', views.post_favorite, name='art_post_favorite'),
    url(r'^edit/(?P<pk>[0-9]+)/$', login_required(views.EditView.as_view()), name='art_edit'),
    url(r'^tags$', views.get_tags, name='art_get_tags'),
    url(r'^$', views.ArtView.as_view(), name='art'),

]