import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse  # Import HttpResponse here

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    api_key = 'sD3XHJa0nKttvAlGugGkFpdj02oG220lpVbEodqhl2GF'
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            # Basic authentication GET
                 response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', 'sD3XHJa0nKttvAlGugGkFpdj02oG220lpVbEodqhl2GF'))
        else:
            # no authentication GET
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
                                    
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
    url = "https://us-east.functions.appdomain.cloud/api/v1/web/c402b745-cf6b-4c53-97b6-f569d52c4d27/dealership-package/get-reviews?dealership="+ str(dealer_id)

    params = {"dealership": dealer_id}

    # Call get_request with the URL and query parameters to get reviews by dealer's id
    json_result = get_request(url, params=params)
    # Call get_request with the URL parameter to get reviews by dealer's id
    #json_result = get_request(url, dealerId=dealer_id)
    reviews = []

    if json_result:
        # Loop through the JSON array of review documents
        for review_doc in json_result:
            review_text = review_doc.get("review")
            
            # Analyze the sentiment for the review using Watson NLU
            sentiment_response = analyze_review_sentiments(review_text)
            print("Sentiment123", sentiment_response)

            #sentiment = sentiment_response.get("sentiment") if sentiment_response else None
            #print("Sentiment:", sentiment)

            review_obj = DealerReview(
                name=review_doc.get("name"),
                purchase=review_doc.get("purchase"),
                review=review_text,
                purchase_date=review_doc.get("purchase_date"),
                car_make=review_doc.get("car_make"),
                car_model=review_doc.get("car_model"),
                car_year=review_doc.get("car_year"),
                sentiment=sentiment_response,  # Assign the sentiment to the DealerReview object
                id=review_doc.get("_id"),
            )
            reviews.append(review_obj)

    return reviews

def analyze_review_sentiments(review_text):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/4cd5c906-0192-4cd4-8ab9-f39894146c75/v1/analyze?version=2019-07-12"
    api_key = "sD3XHJa0nKttvAlGugGkFpdj02oG220lpVbEodqhl2GF"  # Replace with your actual API key for the Watson NLU service
    # Set up the parameters for the Watson NLU request
    params = {
        "text": review_text,
        "features": {
            "sentiment": {}
        }
    }

    try:
        # Make the POST request to Watson NLU
        response = requests.post(url, json=params, headers={'Content-Type': 'application/json'},
                                 auth=HTTPBasicAuth('apikey', api_key))
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            json_result = response.json()

            # Extract and return the sentiment
            sentiment = json_result.get("sentiment", {}).get("document", {}).get("label")
            return sentiment
        else:
            # If the request was not successful, print the response body and return None
            print(f"Error occurred: Status Code {response.status_code}, Response Body: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        print(f"Error occurred during request: {e}")
        return None

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    api_key = 'A2CSAdannOiHGvz-pit1HLlqXwHBTEiS_44cfqiJeaGP'
    try:
        # Call post method of requests library with URL, JSON payload, and parameters
        if api_key:
            # Basic authentication POST
            response = requests.post(url, json=json_payload, params=kwargs,
                                     headers={'Content-Type': 'application/json'},
                                     auth=HTTPBasicAuth('apikey', api_key))
        else:
            # no authentication POST
            response = requests.post(url, json=json_payload, params=kwargs,
                                     headers={'Content-Type': 'application/json'})

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