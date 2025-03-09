from rest_framework import serializers
from .models import Restaurants, FoodItem, ItemsAvailable, NGO, FoodItemRequirement, FoodDonation, DonationItem

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = '__all__'

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'

class ItemsAvailableSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    food_item_name = serializers.CharField(source="food_item.name", read_only=True)

    class Meta:
        model = ItemsAvailable
        fields = ['id', 'restaurant', 'restaurant_name', 'food_item', 'food_item_name', 'available', 'quantity']

# New serializers for NGO models
class NGOSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGO
        fields = '__all__'

class FoodItemRequirementSerializer(serializers.ModelSerializer):
    ngo_name = serializers.CharField(source="ngo.name", read_only=True)
    food_item_name = serializers.CharField(source="food_item.name", read_only=True)

    class Meta:
        model = FoodItemRequirement
        fields = ['id', 'ngo', 'ngo_name', 'food_item', 'food_item_name', 'is_required', 'quantity_needed', 'priority']

class DonationItemSerializer(serializers.ModelSerializer):
    food_item_name = serializers.CharField(source="food_item.name", read_only=True)
    
    class Meta:
        model = DonationItem
        fields = ['id', 'donation', 'food_item', 'food_item_name', 'quantity']

class DonationItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationItem
        fields = ['food_item', 'quantity']

class FoodDonationSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    ngo_name = serializers.CharField(source="ngo.name", read_only=True)
    items = DonationItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = FoodDonation
        fields = ['id', 'restaurant', 'restaurant_name', 'ngo', 'ngo_name', 'status', 
                 'created_at', 'updated_at', 'pickup_time', 'notes', 'items']

class FoodDonationCreateSerializer(serializers.ModelSerializer):
    items = DonationItemCreateSerializer(many=True)
    
    class Meta:
        model = FoodDonation
        fields = ['restaurant', 'ngo', 'pickup_time', 'notes', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        donation = FoodDonation.objects.create(**validated_data)
        
        for item_data in items_data:
            DonationItem.objects.create(donation=donation, **item_data)
            
        return donation