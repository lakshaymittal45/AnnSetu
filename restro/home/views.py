from django.shortcuts import render
import googlemaps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurants, ItemsAvailable, NGO
from .utils import generate_gemini_response
import json

def frontend_view(request):
    return render(request, 'main.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST['name']
        email = request.POST['email']
        query = request.POST['query']
        # Save to database or send email (to be implemented)
        
    return render(request, 'contact.html')

def donation_view(request):
    return render(request, 'donation.html')

def how_view(request):
    return render(request, 'how.html')

def leaderboard_view(request):
    return render(request, 'leaderboard.html')

def mission_view(request):
    return render(request, 'mission.html')

def ngo_view(request):
    return render(request, 'ngo.html')

def recipient_view(request):
    return render(request, 'recipient.html')

def restaurant_view(request):
    return render(request, 'restaurant.html')

def setting_view(request):
    return render(request, 'setting.html')

def vision_view(request):
    return render(request, 'vision.html')

def page_view(request, page_name):
    template_name = f"{page_name}.html"
    return render(request, template_name)

# Configure Google Maps API
GOOGLE_MAPS_API_KEY = "AIzaSyAM6QzamW0kmu2dI-rVPctAFPtGkeloEQA"  # Replace with your API key
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

@csrf_exempt
def notify_food_availability(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            restaurant_id = data.get('restaurant_id')
            food_item_id = data.get('food_item_id')
            quantity = data.get('quantity')

            # Validate input
            if not all([restaurant_id, food_item_id, quantity]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Get restaurant and food item
            restaurant = Restaurants.objects.get(id=restaurant_id)
            item_available = ItemsAvailable.objects.get(restaurant=restaurant, food_item_id=food_item_id)

            # Update quantity
            item_available.quantity = quantity
            item_available.available = True if quantity > 0 else False
            item_available.save()

            # Generate a notification message using Gemini AI
            prompt = (
                f"A restaurant named {restaurant.name} located at {restaurant.location} "
                f"has {quantity} units of {item_available.food_item.name} available. "
                f"Generate a concise notification message for nearby NGOs to collect this food."
            )
            notification_message = generate_gemini_response(prompt)

            # Use Google Maps API to geocode the restaurant's location
            geocode_result = gmaps.geocode(restaurant.location)
            if not geocode_result:
                return JsonResponse({'error': 'Could not geocode restaurant location'}, status=500)
            
            restaurant_location = geocode_result[0]['geometry']['location']
            restaurant_lat, restaurant_lng = restaurant_location['lat'], restaurant_location['lng']

            # Find nearby NGOs (simplified; in reality, you'd search for NGOs in the database)
            nearby_ngos = []
            for ngo in NGO.objects.all():
                ngo_geocode = gmaps.geocode(ngo.location)
                if ngo_geocode:
                    ngo_location = ngo_geocode[0]['geometry']['location']
                    ngo_lat, ngo_lng = ngo_location['lat'], ngo_location['lng']
                    # Calculate distance (simplified; use a proper distance calculation in production)
                    distance = ((restaurant_lat - ngo_lat) ** 2 + (restaurant_lng - ngo_lng) ** 2) ** 0.5
                    if distance < 0.1:  # Arbitrary threshold (~10km, adjust as needed)
                        nearby_ngos.append({
                            'name': ngo.name,
                            'location': ngo.location,
                            'distance': distance
                        })

            # In a real app, you’d send notifications (e.g., via email, SMS, or push notifications)
            # For now, return the nearby NGOs in the response
            return JsonResponse({
                'message': 'Food availability updated',
                'notification': notification_message,
                'nearby_ngos': nearby_ngos,
                'restaurant_id': restaurant_id,
                'food_item_id': food_item_id,
                'quantity': quantity
            }, status=200)

        except Restaurants.DoesNotExist:
            return JsonResponse({'error': 'Restaurant not found'}, status=404)
        except ItemsAvailable.DoesNotExist:
            return JsonResponse({'error': 'Food item not available at this restaurant'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

from rest_framework import viewsets
from .models import Restaurants, FoodItem, ItemsAvailable, NGO, FoodItemRequirement, FoodDonation
from .serializers import (
    RestaurantSerializer,
    FoodItemSerializer,
    ItemsAvailableSerializer,
    NGOSerializer,
    FoodItemRequirementSerializer,
    FoodDonationSerializer
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer

class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

class FoodItemAvailableViewSet(viewsets.ModelViewSet):
    queryset = ItemsAvailable.objects.all()
    serializer_class = ItemsAvailableSerializer

class NGOViewSet(viewsets.ModelViewSet):
    queryset = NGO.objects.all()
    serializer_class = NGOSerializer

class FoodItemRequirementViewSet(viewsets.ModelViewSet):
    queryset = FoodItemRequirement.objects.all()
    serializer_class = FoodItemRequirementSerializer

class FoodDonationViewSet(viewsets.ModelViewSet):
    queryset = FoodDonation.objects.all()
    serializer_class = FoodDonationSerializer
