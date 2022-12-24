import json
from django.shortcuts import render
import smtplib
from email.message import EmailMessage
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from functools import reduce
import operator
from .models import User, Location, Shop, Image, Review, AboutImage
from django.db.models import Q
from difflib import SequenceMatcher
from django.core.paginator import Paginator
from geopy import distance
from django.contrib.auth.decorators import login_required
import os


def index(request):

    shops = Shop.objects.all()  # gets all shops and locations then splits up and serves in a pagination form if a post request or displays first page
    locations = Location.objects.all().order_by("name")
    pageRequested = 1
    personal = False
    pagination = True
    totalPages = 0

    try:
        coords = (request.POST["lat"], request.POST["long"])
        filteredShops = []
        distanceDict = {}
        for shop in shops:
            shopCoords = (shop.lat, shop.long)
            distanceBetween = distance.distance(coords, shopCoords).km
            if distanceBetween <= 10:
                filteredShops.append(shop)
                distanceDict[shop.id] = distanceBetween
                pagination = False

        personal = True
        shops = filteredShops

    except:
        pass

    try:
        pageRequested = int(request.POST["pageRequest"])

    except:
        pass

    try:
        shops = Location.objects.get(name=request.POST["locationRequest"]).shops.all()
        pagination = False

    except:
        pass

    if pagination:
        shops = Paginator(shops, 2)
        totalPages = shops.num_pages
        shops = shops.page(pageRequested)

    return render(request, 'brewguide/index.html', {
        "shops": shops,
        "locations": locations,
        "currentPage": pageRequested,
        "lastPage": totalPages,
        "personal": personal,
        "pagination": pagination
    })


def about(request):
    images = AboutImage.objects.all()
    return render(request, "brewguide/aboutUs.html", {
        "images": images
    })


def contact(request):
    if request.method == "POST":
        print(os.environ)

        address = os.environ["email"]
        password = os.environ["password"]

        userName = request.POST["name"]
        userEmail = request.POST["email"]
        body = request.POST["body"]

        if not validEmail(userName, userEmail, body):
            return HttpResponse("Critical Failure. Email not sent.")

        # create email
        email = EmailMessage()
        email['Subject'] = f"Contact from {userName}"
        email['From'] = address
        email['To'] = address
        email.set_content(f"Email from: {userEmail}\n{body}")

        # send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(address, password)
            smtp.send_message(email)
        
        return render(request, "brewguide/contact.html", {
            "message": "Success!"
        })
    
    else:
        return render(request, "brewguide/contact.html")
        


def register(request):   # registers the user or displays register page or redirects depending on context
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "brewguide/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "brewguide/register.html", {
                "message": "Username already taken."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        return render(request, "brewguide/register.html")


def login_view(request):  # logs in and redirects to index or just redirects depending on context
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"].strip()
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "brewguide/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        
        return render(request, "brewguide/login.html")


def search(request):
    fullSearch = request.GET["terms"].upper().strip()
    terms = fullSearch.split(" ")
    
    try:
        shop = Shop.objects.get(name=fullSearch)
        return HttpResponseRedirect(reverse("shop", kwargs={"name": shop.name}))
        
    except:
        locations = Location.objects.all()
        setattr(Shop, "ratio", 0)
        clauses = (Q(name__contains=term) for term in terms)
        query = reduce(operator.or_, clauses)
        shops = Shop.objects.filter(query)   # returns shops where one of the terms is in the name

        shops = sorted(shops, key =lambda shop: SequenceMatcher(None, fullSearch, shop.name).ratio(), reverse=True)
        return render(request, 'brewguide/index.html', {
        "shops": shops,
        "locations": locations
        })


def shop(request, name):
    shop = Shop.objects.get(name=name)
    reviews = Review.objects.filter(shop=shop).order_by("-timestamp")
    images = Image.objects.filter(shop=shop)
    return render(request, "brewguide/shop.html", {
        "shop": shop,
        "images": images,
        "reviews": reviews
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def validEmail(name, email, body):

    if len(name) == 0 or len(body) == 0 or len(email) == 0:
        return False

    if "@" not in email or "." not in email or " " in email.rstrip():
        return False

    if len(body) > 500:
        return False

    return True


def best(request):

    shops = Shop.objects.all().order_by("-rating")[:5]

    return render(request, 'brewguide/best.html', {
        "shops": shops
    })


@login_required
def review(request):
    if request.method == "POST":
        data = json.load(request)

        try:
            if data["review"] and len(data["review"]) < 100:
                review = Review(
                    content = data["review"],
                    shop = Shop.objects.get(id=data["shopId"]),
                    poster = request.user,
                )
                review.save()
                return JsonResponse({"Success": "Review added"}, status=201)
            else:
                return JsonResponse({"Error": "Bad request"}, status=400)

        except:
            return JsonResponse({"Error": "Bad request"}, status=400)