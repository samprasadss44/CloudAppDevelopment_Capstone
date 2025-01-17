from django.db import models
from django.utils.timezone import now

from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Add any other fields you would like to include in the Car Make model
    
    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices as needed
    ]
    
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='car_models')
    dealer_id = models.IntegerField()  # Assuming it's an IntegerField, adjust the field accordingly
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CAR_TYPES)
    year = models.DateField()
    # Add any other fields you would like to include in the Car Model model
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()}) - {self.car_make.name}"

class CarDealer(models.Model):
    doc_id = models.CharField(max_length=50, primary_key=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    id = models.IntegerField()  # Change the field name to 'id'
    lat = models.FloatField()
    long = models.FloatField()
    short_name = models.CharField(max_length=20)
    st = models.CharField(max_length=2)  # Assuming 'st' is for the state abbreviation
    state = models.CharField(max_length=100)  # Add the 'state' field
    zip_code = models.CharField(max_length=10)  # Change the field name to 'zip_code'

    def __str__(self):
        return self.full_name

from django.db import models
from .models import CarDealer  # Import the CarDealer model

class DealerReview(models.Model):
    car_make = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    car_year = models.IntegerField()
    dealership = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    review = models.TextField()
    # Additional field for sentiment analysis (can be added later)
    sentiment = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Review for {self.dealership} - {self.name} - Car: {self.car_make} {self.car_model} ({self.car_year})"