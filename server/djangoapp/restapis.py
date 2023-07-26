import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse  # Import HttpResponse here

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        response.raise_for_status()  # Raise an error for unsuccessful responses
        json_data = json.loads(response.text)
        return json_data
    except requests.exceptions.RequestException as e:
        # If a network exception occurs, print the error and return None or an empty dictionary
        print("Network exception occurred:", e)
        return None
    except json.JSONDecodeError as e:
        # If JSON decoding fails, print the error and return None or an empty dictionary
        print("JSON decoding error:", e)
        return None

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result and "result" in json_result:
        dealers = json_result["result"]
        for dealer in dealers:
            dealer_doc = dealer.get("doc")
            # Create a CarDealer object with values in the dealer object
            dealer_obj = CarDealer(
                doc_id=dealer.get("_id"),
                address=dealer_doc.get("address"),
                city=dealer_doc.get("city"),
                full_name=dealer_doc.get("full_name"),
                id=dealer_doc.get("id"),
                lat=dealer_doc.get("lat"),
                long=dealer_doc.get("long"),
                short_name=dealer_doc.get("short_name"),
                st=dealer_doc.get("st"),
                state=dealer_doc.get("state"),
                zip_code=dealer_doc.get("zip")
            )
            results.append(dealer_obj)
    return results

def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/c402b745-cf6b-4c53-97b6-f569d52c4d27/dealership-package/get_all_dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ','.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return dealerships

def get_dealer_reviews_from_cf(dealer_id):
    url = "https://us-east.functions.appdomain.cloud/api/v1/web/c402b745-cf6b-4c53-97b6-f569d52c4d27/dealership-package/get-all-reviews"

    # Call get_request with the URL parameter to get reviews by dealer's id
    json_result = get_request(url, dealerId=dealer_id)
    reviews = []

    if json_result:
        # Loop through the JSON array of review documents
        for review_doc in json_result:
            review_obj = DealerReview(
                name=review_doc.get("name"),
                purchase=review_doc.get("purchase"),
                review=review_doc.get("review"),
                purchase_date=review_doc.get("purchase_date"),
                car_make=review_doc.get("car_make"),
                car_model=review_doc.get("car_model"),
                car_year=review_doc.get("car_year"),
                sentiment=review_doc.get("sentiment"),
                id=review_doc.get("_id"),
            )
            reviews.append(review_obj)

    return reviews

