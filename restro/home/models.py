from django.db import models

# Create your models here.
class Restaurants(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class FoodItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class ItemsAvailable(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE, related_name="menu_items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name="restaurants")
    available = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('restaurant', 'food_item')  

    def __str__(self):
        return f"{self.restaurant.name} - {self.food_item.name} ({self.quantity} available)"

# New models for NGOs and their requirements
class NGO(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class FoodItemRequirement(models.Model):
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name="required_items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name="needed_by_ngos")
    is_required = models.BooleanField(default=True)
    quantity_needed = models.PositiveIntegerField(default=0)
    priority = models.IntegerField(default=0, help_text="Higher number means higher priority")
    
    class Meta:
        unique_together = ('ngo', 'food_item')
    
    def __str__(self):
        status = "required" if self.is_required else "optional"
        return f"{self.ngo.name} - {self.food_item.name} ({self.quantity_needed} needed, {status})"

class FoodDonation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE, related_name="donations")
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name="received_donations")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pickup_time = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Donation from {self.restaurant.name} to {self.ngo.name} ({self.status})"

class DonationItem(models.Model):
    donation = models.ForeignKey(FoodDonation, on_delete=models.CASCADE, related_name="items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.food_item.name} ({self.quantity}) - {self.donation}"
    
