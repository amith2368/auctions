from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms 
from django.contrib import messages
from django.db.models import Max

from .models import User, Listing, CommentSection, Bid, Auction

# Forms for the website 

class ListingForm(forms.ModelForm):
    # model for the form
    class Meta:
        model = Listing
        fields = ['name', 'description', 'image', 'start_bid', 'category', 'status' ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentSection
        fields = ('body',)

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid 
        fields = ['user_bid',]

# All functions


def watchcount(request):
    w_user = request.user
    count = Listing.objects.filter(wl = w_user).count()
    return count


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.exclude(status = "inactive").all(),
        "count": watchcount(request),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    form = ListingForm(request.POST or None, request.FILES or None)
    if form.is_valid() and request.method == "POST":
        obj = form.save(commit = False)
        obj.creater = request.user
        obj.top_bid = request.POST['start_bid']
        obj.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(reverse("index")) 
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {
        "form": form,
        "count": watchcount(request),
    })

@login_required()
def view_listing(request, listing_id):
    listing = Listing.objects.get( pk = listing_id)
    comments = listing.comments.filter(active=True)
    new_comment = None
    new_bid = None
    bid_error = False
    auction_result = False
    # If Comment posted
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        bid_form = BidForm(request.POST)
        if comment_form.is_valid():

            #creating temporary Comment yet to add to database
            new_comment = comment_form.save(commit=False)
            new_comment.name = request.user
            new_comment.listing = listing
            new_comment.save()
            return HttpResponseRedirect(reverse("view", args=(listing.id, )))
        elif bid_form.is_valid():
            new_bid = bid_form.save(commit=False)
            if new_bid.user_bid > listing.top_bid:
                Listing.objects.filter(id = listing_id).update(top_bid = new_bid.user_bid) 
                new_bid.listing = listing
                new_bid.bidder = request.user
                new_bid.save()
                bid_id = new_bid.id
                auction(bid_id, listing_id)
                return HttpResponseRedirect(reverse("view", args=(listing.id, )))
            else:
                bid_error = True
                bid_form = BidForm()
                

    else:
        comment_form = CommentForm()
        bid_form = BidForm()

    if request.user in listing.wl.all():
        is_w_user = False
    else:
        is_w_user = True
    
    if request.user == listing.creater:
        stop_auction = True
    else:
        stop_auction = False

    if listing.status == "sold":
         auction_result = True  
         result = Auction.objects.get(pk = listing_id) 
         r_winner = result.winner
         return render(request, "auctions/view_listing.html", {
        "listing": listing,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        "is_w_user": is_w_user,
        "auction_result":auction_result,
        "winner": r_winner,
        "count": watchcount(request),

        })

    return render(request, "auctions/view_listing.html", {
        "listing": listing,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        "bid_form": bid_form,
        "bids": listing.bids.count(),
        "is_w_user": is_w_user,
        "bid_error": bid_error,
        "stop_auction":stop_auction,
        "count": watchcount(request),

    })

def view_userlistings(request, q_user):
    q_user = request.user
    return render(request, "auctions/userlistings.html", {
        "listings": Listing.objects.filter(creater = q_user).all(),
        "count": watchcount(request),
    })


    
def watchlist(request,listing_id):
    listing = Listing.objects.get( pk = listing_id)
    w_user = request.user
    if w_user not in listing.wl.all():
        listing.wl.add(w_user)
        listing.save()
    else:
        listing.wl.remove(w_user)
        listing.save()
    return HttpResponseRedirect(reverse("view", args=(listing.id, )))

def watchlist_view(request):
    w_user = request.user
    return render(request, "auctions/watchlist.html", {
        "listings": Listing.objects.filter(wl = w_user).all(),
        "count": watchcount(request)
    })


def auction(w_bid, listing_id):
    if Auction.objects.filter(listing = listing_id).exists():
        Auction.objects.filter(listing = listing_id).update(winner = w_bid)
    else:
        listing = Listing.objects.get( pk = listing_id)
        winning_bid = Bid.objects.get(pk = w_bid)
        Auction.objects.create(listing = listing, winner = winning_bid)
    return HttpResponseRedirect(reverse("view", args=(listing_id, ))) 

def stop_auction(request, listing_id):
    Listing.objects.filter(id = listing_id).update(status = "sold")
    return HttpResponseRedirect(reverse("view", args=(listing_id, )))






    
    



    

