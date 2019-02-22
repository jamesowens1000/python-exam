from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, "quotes/index.html")

def register(request):
    errors = User.objects.validator(request.POST, "registration", "")

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        #Redirect the user back to the  reg/login page to fix the errors
        return redirect("/")
    else:
        User.objects.create(first_name=request.POST['reg-fname'], last_name=request.POST['reg-lname'], email=request.POST['reg-email'], password=request.POST['reg-pword'])
        thisUser = User.objects.last()
        request.session['user_id'] = thisUser.id
        request.session['user_fname'] = thisUser.first_name
        request.session['user_lname'] = thisUser.last_name
        request.session['user_email'] = thisUser.email
        return redirect("/quotes")

def login(request):
    errors = User.objects.validator(request.POST, "login", "")

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        #Redirect the user back to the  reg/login page to fix the errors
        return redirect("/")
    else:
        thisUser = User.objects.filter(email=request.POST['log-email'], password=request.POST['log-pword'])
        request.session['user_id'] = thisUser[0].id
        request.session['user_fname'] = thisUser[0].first_name
        request.session['user_lname'] = thisUser[0].last_name
        request.session['user_email'] = thisUser[0].email
        return redirect("/quotes")

def edit_page(request):
    data = {
        "thisUser": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "quotes/edit.html", data)

def update(request):
    errors = User.objects.validator(request.POST, "update", request.session['user_email'])

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect("/edit_page")
    else:
        thisUser = User.objects.get(id=request.session['user_id'])
        thisUser.first_name = request.POST['fname']
        thisUser.last_name = request.POST['lname']
        thisUser.email = request.POST['email']
        thisUser.save()
        request.session['user_fname'] = thisUser.first_name
        request.session['user_lname'] = thisUser.last_name
        request.session['user_email'] = thisUser.email
        return redirect("/quotes")

def quotes(request):
    if 'user_id' not in request.session:
        return redirect("/")
    else:
        data = {
            "all_quotes": Quote.objects.all().order_by("-created_at")
        }
        return render(request, "quotes/dashboard.html", data)

def post_quote(request):
    errors = Quote.objects.validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/quotes")
    else:
        thisUser = User.objects.get(id=request.session['user_id'])
        Quote.objects.create(user=thisUser, author=request.POST['post-author'], quote=request.POST['post-quote'])
        return redirect("/quotes")

def user_quotes(request, user_id):
    thisUser = User.objects.get(id=user_id)
    data = {
        "user_fname": thisUser.first_name,
        "user_lname": thisUser.last_name,
        "user_quotes": thisUser.quotes.all().order_by("-created_at")
    }
    return render(request, "quotes/user_quotes.html", data)

def like_quote(request, quote_id):
    thisUser = User.objects.get(id=request.session['user_id'])
    thisQuote = Quote.objects.get(id=quote_id)
    thisQuote.like.add(thisUser)
    thisQuote.save()
    return redirect("/quotes")

def delete_quote(request, quote_id):
    thisQuote = Quote.objects.get(id=quote_id)
    thisQuote.delete()
    return redirect("/quotes")

def logout(request):
    request.session.clear()
    return redirect("/")