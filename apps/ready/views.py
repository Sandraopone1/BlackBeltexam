from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.db.models import Count
def index(request):
    return render(request, "ready/index.html")

def register(request):
    whatever_register_returned = User.objects.register(request.POST)
    if whatever_register_returned[0]:
        request.session["user_id"] = whatever_register_returned[1].id
        messages.add_message(request, messages.SUCCESS, 'You successfully registered, good job!')
        return redirect("/dashboard")
    else:
        for error in whatever_register_returned[1]:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/")

def login(request):
    user = User.objects.login(request.POST)
    if user["is_valid"]:
        request.session["user_id"] = user["user"].id
        messages.add_message(request, messages.SUCCESS, 'You successfully logged in, good job!')
        return redirect("/dashboard")
    else:
        for error in user["errors"]:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/")

def logout(request):
    request.session.clear()
    messages.add_message(request, messages.SUCCESS, "You have just logged out, goodbye!")
    return redirect("/")

def dashboard(request): 
	
    user = User.objects.get(id=request.session["user_id"])
    context = {
        'user': user,
        'quotable_quotes': Quote.objects.exclude(favorites = user),
        'favorites': user.favorites.all()
    }
    return render(request, 'ready/dashboard.html', context)
    
	# 	# "movies": Movie.objects.all(),
	# 	# "actors": Actor.objects.all()
	# return render(request, "ready/dashboard.html", {"user": user})

def create(request):
    if request.method != 'POST':
        return redirect('/')
    
    check = Quote.objects.validateQuote(request.POST)
    if request.method != 'POST':
        return redirect('/dashboard')
    if check[0] == False:
        for error in check[1]:
            messages.add_message(request, messages.INFO, error, extra_tags="add_item")
            return redirect('/dashboard')
    if check[0] == True:

        quote = Quote.objects.create(
            content = request.POST.get('content'),
            poster = User.objects.get(id=request.session["user_id"]),
            author = request.POST.get('author')
            )

        return redirect('/dashboard')
    return redirect('/dashboard')


def add_favorite(request, id):

    user = User.objects.get(id=request.session["user_id"])
    favorite = Quote.objects.get(id=id)

    user.favorites.add(favorite)

    return redirect('/dashboard')

def remove_favorite(request, id):

    user = User.objects.get(id=request.session["user_id"])
    favorite = Quote.objects.get(id=id)

    user.favorites.remove(favorite)

    return redirect('/dashboard')






def show_user(request, id):

    user =  User.objects.get(id = id)
    
    # user_info = User.objects.get(id=request.session["user_id"])
    context = {
        'user': user,
        'favorites': user.favorites.all(),  
        # 'the_quotes' : Quote.objects.filter
         # poster = User.objects.get(id=request.session["user_id"]),
        'quotable_quotes' : Quote.objects.all()     
    }
    return render(request, 'ready/user.html', context)

