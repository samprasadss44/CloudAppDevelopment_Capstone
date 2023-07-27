from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import get_dealerships, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.contrib.auth.decorators import login_required
from .restapis import get_dealerships, get_dealer_reviews_from_cf, analyze_review_sentiments, post_request
from django.shortcuts import get_object_or_404, render
from .models import CarDealer, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about_us(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact_us(request):
    return render(request, 'djangoapp/contact.html')
    
# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

def get_dealerships_view(request):
    context = {}
    # Call the get_dealerships function from restapi.py
    dealerships_data = get_dealerships(request)
    print("dealerships_data", dealerships_data)
    context['dealerships_data'] = dealerships_data
    # Pass the dealerships_data to the template
   # context = {'dealerships_data': dealerships_data}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    context = {}
    print("request",request)
    # Get the dealer object using the dealer_id
    #dealer = get_object_or_404(CarDealer, id=dealer_id)
    # Call the get_dealer_reviews_from_cf method to get the reviews for the dealer
    reviews = get_dealer_reviews_from_cf(dealer_id)
   # dealer = get_object_or_404(CarDealer, id=dealer_id)
    #print("dealer",dealer)
    # Get the dealer object using the dealer_id
    # Append the list of reviews to the context
    context = {
            'reviews': reviews,
        }
    # Return a HttpResponse with the reviews data
    if request.method == "GET":
         return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

@login_required
def add_review(request, dealer_id):
    context = {}
    if request.method == 'GET':
        # If it's a GET request, render the form to submit a review
        # Get the list of cars to display in the dropdown
        cars = CarModel.objects.all()  # Replace 'Car' with the actual model name for cars

        # Add 'cars' to the context
        context['cars'] = cars
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        # If it's a POST request, process the form data and submit the review

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to post a review.")
            return redirect('djangoapp:index')

        # Get the form data from the request
        name = request.POST['name']
        purchase = request.POST['purchase']
        review_text = request.POST['review']
        purchase_date = request.POST['purchase_date']
        car_make = request.POST['car_make']
        car_model = request.POST['car_model']
        car_year = request.POST['car_year']

        # Analyze the review sentiment using Watson NLU
        sentiment_response = analyze_review_sentiments(review_text)
        sentiment = sentiment_response.get("sentiment") if sentiment_response else None

        # Create the dictionary object for the review data
        review = {
            "time": datetime.utcnow().isoformat(),
            "name": name,
            "dealership": dealer_id,
            "review": review_text,
            "purchase": purchase,
            "purchase_date": purchase_date,
            "car_make": car_make,
            "car_model": car_model,
            "car_year": car_year,
            "sentiment": sentiment,
            # Add any additional attributes as needed for your cloud function
        }

        # Create the json_payload dictionary with the review key
        json_payload = {"review": review}

        # URL to post the review to (replace with your actual URL)
        post_url = "https://us-east.functions.appdomain.cloud/api/v1/web/c402b745-cf6b-4c53-97b6-f569d52c4d27/dealership-package/post-reviews"

        # Make the POST request to submit the review
        post_response = post_request(post_url, json_payload, dealerId=dealer_id)

        # Print the post response to the console
        print("POST Response:", post_response)

        # You can also append the post_response to an HttpResponse and render it on the browser
        # response = HttpResponse(post_response, content_type='application/json')
        # return response

        # Redirect to the dealer details page after submitting the review
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)