from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render

from .forms import SignUpForm


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            form = UserCreationForm(request.POST)
            return render(request, "test.html", {
                "form": form,
                "title": "Sign Up",
                "errors": form.errors,
            })
    else:
        return render(request, "test.html", {
            "form": UserCreationForm(),
            "title": "Sign Up",
        })
