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
