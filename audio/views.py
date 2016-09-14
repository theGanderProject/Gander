from django.shortcuts import render, redirect
from .models import Audio, AudioForm
from django.views import generic
from django.views.generic.edit import FormView

# Create your views here.
class ViewView(generic.DetailView):
    model = Audio
    template_name = 'audio/view.html'

class SubmitView(FormView):
    template_name = 'submit.html'
    form_class = AudioForm
    success_url = '/'

    def form_valid(self, form):
        audio = form.save(commit=False)
        audio.owner = self.request.user.username
        audio.save()
        return super(SubmitView, self).form_valid(form)