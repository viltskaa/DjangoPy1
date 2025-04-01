import random

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import TestForm


@login_required(redirect_field_name="/login")
def index(request: HttpRequest):
    result = 0

    if request.POST:
        number1 = float(request.POST.get('number1'))
        number2 = float(request.POST.get('number2'))
        result = number1 + number2

    return render(request, "index.html", {
        "result": result,
    })


def profile(request: HttpRequest):
    if request.POST:
        email = request.POST.get('email')
        select = request.POST.get('select')
        gender = request.POST.get('gender')

        return render(request, "profile.html", {
            "id": random.randint(1, 100),
            "email": email,
            "select": select,
            "gender": gender,
        })
    else:
        return 404


def test_form(request: HttpRequest):
    if request.POST:
        form = TestForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['text_field']
            print(name)
            # add data to database
            return HttpResponseRedirect("/")
    else:
        form = TestForm()

    return render(request, "test.html", {
        "form": form,
    })
