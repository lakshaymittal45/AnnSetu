document.addEventListener("DOMContentLoaded", function () {
  document.querySelector(".view-more").addEventListener("click", function () {
      alert("Loading more recipient history...");
      // Future: Load more data dynamically
  });

  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
          function (position) {
              const latitude = position.coords.latitude;
              const longitude = position.coords.longitude;
              initMap(latitude, longitude);
          },
          function (error) {
              console.error("Error getting location: ", error);
              alert("Location access denied. Showing default map.");
              initMap(28.6139, 77.2090); // Default: New Delhi, India
          }
      );
  } else {
      alert("Geolocation is not supported by this browser.");
  }
});

function initMap(latitude, longitude) {
  const map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: latitude, lng: longitude },
      zoom: 14,
  });

  new google.maps.Marker({
      position: { lat: latitude, lng: longitude },
      map,
      title: "Your Location",
      icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
  });

  fetchNearbyRestaurants(map, latitude, longitude);
}

function fetchNearbyRestaurants(map, latitude, longitude) {
  const service = new google.maps.places.PlacesService(map);
  service.nearbySearch(
      {
          location: { lat: latitude, lng: longitude },
          radius: 5000, // 5 km search radius
          type: "restaurant",
      },
      function (results, status) {
          if (status === google.maps.places.PlacesServiceStatus.OK) {
              results.forEach((place) => {
                  new google.maps.Marker({
                      position: place.geometry.location,
                      map,
                      title: place.name,
                  });
              });
          } else {
              console.error("Places API request failed: ", status);
          }
      }
  );
}