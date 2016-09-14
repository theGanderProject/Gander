from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Image, ImageForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic.edit import FormView, UpdateView
from django.db.models import F
from django.http import JsonResponse


class EditView(UpdateView):
    model = Image
    fields = 'title description'.split()
    template_name = 'visual_art/edit.html'
    success_url = '/'

    def form_valid(self, form):
        # make sure user owns object
        image = form.save(commit=False)
        if (image.owner != self.request.user):
            return HttpResponse("You can't edit art that isn't yours")
        else:
            image.save()
            return super(EditView, self).form_valid(form) 

@login_required
def post_favorite(request, pk):
    if request.method == 'POST':
        image = Image.objects.get(pk=pk)
        if Image.objects.filter(pk=pk, favorite=request.user): # already favorited
            image.favorite.remove(request.user)
            return HttpResponse("removed favorite")
        elif image.owner == request.user:
            return HttpResponse("You can't favorite your own art.")
        else:
            image.favorite.add(request.user)
            return HttpResponse("added favorite")

class HomePageView(generic.ListView):
    template_name = 'visual_art/home_page.html'
    context_object_name = 'images'

    def get_queryset(self):
        return Image.objects.all()

class ArtView(generic.ListView):
    template_name = 'visual_art/art.html'
    context_object_name = 'images'

    def get_queryset(self):
        return Image.objects.all()


class GalleryView(generic.ListView):
    template_name = 'visual_art/gallery.html'
    context_object_name = 'images'

    def get_queryset(self):
        return Image.objects.filter(owner__username=self.kwargs['username'])

class SubmitView(FormView):
    template_name = 'submit.html'
    form_class = ImageForm
    success_url = '/'

    def form_valid(self, form):
        image = form.save(commit=False)
        image.owner = self.request.user
        image.save()
        return super(SubmitView, self).form_valid(form)

class ViewView(generic.DetailView):
    model = Image
    template_name = 'visual_art/view.html'

