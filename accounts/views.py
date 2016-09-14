from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django import forms

class UserCreationWithEmailForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationWithEmailForm, self).save(commit=False)
        email_already_in_use = User.objects.filter(email__iexact=self.cleaned_data["email"])
        if email_already_in_use:
            raise forms.ValidationError(validators.DUPLICATE_EMAIL)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationWithEmailForm

    def form_valid(self, form):
        new_user = form.save()
        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                                )
        login(self.request, new_user)
        next = self.request.GET.get('next', '/')
        return HttpResponseRedirect(next)