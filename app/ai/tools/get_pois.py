import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from langchain_core.tools import tool
from app.config import Config

# Constantes pour l'API TripAdvisor via RapidAPI
HEADERS = {
    "x-rapidapi-key": Config.RAPIDAPI_KEY,
    "x-rapidapi-host": Config.RAPIDAPI_HOST
}


def get_city_coordinates(city: str) -> Optional[Dict[str, float]]:
    """
    Récupère les coordonnées géographiques (latitude, longitude) d'une ville.
    
    Args:
        city (str): Nom de la ville
        
    Returns:
        Optional[Dict[str, float]]: Dictionnaire avec latitude et longitude ou None en cas d'erreur
    """
    try:
        url = "https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/searchLocation"
        querystring = {"query": city}

        response = requests.get(url, headers=HEADERS, params=querystring)
        response.raise_for_status()  # Lance une erreur si la requête a échoué

        data = response.json()
        if data.get("data") and len(data["data"]) > 0:
            location = data["data"][0]
            return {
                "latitude": location.get("latitude", 0),
                "longitude": location.get("longitude", 0),
                "locationId": location.get("locationId", "")
            }
        return None
    except Exception as e:
        print(f"Erreur durant recherche des coordonnées {city}: {e}")
        return None


@tool()
def get_pois(city: str) -> List[Dict[str, Any]]:
    """
    Récupère les points d'intérêt (attractions touristiques) dans une ville donnée.

    Args:
        city (str): Nom de la ville

    Returns:
        List[Dict[str, Any]]: Liste des attractions touristiques
    """
    try:
        url = "https://api.content.tripadvisor.com/api/v1/location/search"
        params = {
            "key": Config.TRIPADVISOR_API_KEY,
            "searchQuery": city,
            "language": "fr",
            "category": "attractions"
        }
        headers = {
            "accept": "application/json"
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        attractions = []
        if data.get("data"):
            for attraction in data["data"][:10]:
                attractions.append({
                    "location_id": attraction.get("location_id", ""),
                    "nom": attraction.get("name", ""),
                    "adresse": attraction.get("address_obj", {}).get("address_string", "")
                })
        return attractions
    except Exception as e:
        print(f"Erreur lors de la recherche d'attractions à {city}: {e}")
        return [{"error": str(e)}]
    

@tool()
def get_poi_details(location_id: str) -> dict:
    """
    Récupère les détails d'une attraction à partir de son location_id.
    
    Args:
        location_id (str): L'identifiant unique de l'attraction
        
    Returns:
        dict: Les détails de l'attraction
    """
    url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/details"
    params = {
        "language": "fr",
        "currency": "EUR",
        "key": Config.TRIPADVISOR_API_KEY
    }
    headers = {
        "accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        # Extraction des informations pertinentes de la réponse API
        details = {
            "nom": data.get("name", ""),
            "description": data.get("description", ""),
            "adresse": data.get("address_obj", {}).get("address_string", ""),
            "latitude": data.get("latitude", ""),
            "longitude": data.get("longitude", ""),
            "rating": data.get("rating", ""),
            "num_reviews": data.get("num_reviews", ""),
            "web_url": data.get("web_url", ""),
            "email": data.get("email", ""),
            "phone": data.get("phone", ""),
            "website": data.get("website", ""),
            "catégorie": data.get("category", {}).get("name", ""),
            "type_attraction": data.get("subcategory", [{}])[0].get("name", "") if data.get("subcategory") else "",
            "photo_url": data.get("photo", {}).get("images", {}).get("original", {}).get("url", "") if data.get("photo") else ""
        }
        return details
    except Exception as e:
        print(f"Erreur lors de la récupération des détails pour {location_id}: {e}")
        return {"error": str(e)}


@tool()
def search_restaurants(city: str) -> List[Dict[str, Any]]:
    """
    Recherche des restaurants dans une ville donnée.
    
    Args:
        city (str): Nom de la ville
        
    Returns:
        List[Dict[str, Any]]: Liste des restaurants trouvés
    """
    try:
        url = "https://api.content.tripadvisor.com/api/v1/location/search"
        params = {
            "key": Config.TRIPADVISOR_API_KEY,
            "searchQuery": city,
            "language": "fr",
            "category": "restaurants"
        }
        headers = {
            "accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        restaurants = []
        
        if data.get("data"):
            for restaurant in data["data"][:10]:  # Limiter à 10 résultats
                restaurants.append({
                    "location_id": restaurant.get("location_id", ""),
                    "nom": restaurant.get("name", ""),
                    "adresse": restaurant.get("address_obj", {}).get("address_string", ""),
                    "latitude": restaurant.get("latitude", ""),
                    "longitude": restaurant.get("longitude", "")
                })
                
        return restaurants
    except Exception as e:
        print(f"Erreur lors de la recherche de restaurants à {city}: {e}")
        return [{"error": str(e)}]


@tool()
def search_hotels(city: str, min_stars: int = 0, max_price: int = 1000) -> List[Dict[str, Any]]:
    """
    Recherche des hôtels dans une ville donnée avec filtrage par étoiles et prix.
    
    Args:
        city (str): Nom de la ville
        min_stars (int, optional): Nombre minimum d'étoiles (0-5). Par défaut 0.
        max_price (int, optional): Prix maximum par nuit en euros. Par défaut 1000.
        
    Returns:
        List[Dict[str, Any]]: Liste des hôtels trouvés
    """
    try:
        url = "https://api.content.tripadvisor.com/api/v1/location/search"
        params = {
            "key": Config.TRIPADVISOR_API_KEY,
            "searchQuery": city,
            "language": "fr",
            "category": "hotels"
        }
        headers = {
            "accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        hotels = []
        
        if data.get("data"):
            for hotel in data["data"][:10]:  # Limiter à 10 résultats
                # Pour le filtrage par étoiles (si disponible dans les données)
                hotel_class = float(hotel.get("hotel_class", 0)) if hotel.get("hotel_class") else 0
                if hotel_class < min_stars:
                    continue
                    
                hotels.append({
                    "location_id": hotel.get("location_id", ""),
                    "nom": hotel.get("name", ""),
                    "adresse": hotel.get("address_obj", {}).get("address_string", ""),
                    "hotel_class": hotel.get("hotel_class", ""),
                    "rating": hotel.get("rating", ""),
                    "num_reviews": hotel.get("num_reviews", "")
                })
                
        return hotels
    except Exception as e:
        print(f"Erreur lors de la recherche d'hôtels à {city}: {e}")
        return [{"error": str(e)}]


@tool()
def get_hotel_details(location_id: str) -> Dict[str, Any]:
    """
    Récupère les détails d'un hôtel à partir de son location_id.
    
    Args:
        location_id (str): Identifiant unique de l'hôtel sur TripAdvisor
        
    Returns:
        Dict[str, Any]: Détails de l'hôtel incluant les services, photos, avis, etc.
    """
    try:
        # D'abord récupérer les infos générales via l'API Content
        url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/details"
        params = {
            "language": "fr",
            "currency": "EUR",
            "key": Config.TRIPADVISOR_API_KEY
        }
        headers = {
            "accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Création du dictionnaire de résultat avec les données réelles
        hotel_details = {
            "nom": data.get("name", ""),
            "description": data.get("description", ""),
            "adresse": data.get("address_obj", {}).get("address_string", ""),
            "rating": data.get("rating", ""),
            "num_reviews": data.get("num_reviews", ""),
            "catégorie": data.get("category", {}).get("name", ""),
            "sous_catégorie": data.get("subcategory", [{}])[0].get("name", "") if data.get("subcategory") else "",
            "téléphone": data.get("phone", ""),
            "website": data.get("website", ""),
            "email": data.get("email", ""),
            "latitude": data.get("latitude", ""),
            "longitude": data.get("longitude", ""),
            "photo_url": data.get("photo", {}).get("images", {}).get("original", {}).get("url", "") if data.get("photo") else "",
            "horaires": data.get("hours", {}).get("week_ranges", [])
        }
        
        return hotel_details
    except Exception as e:
        print(f"Erreur lors de la récupération des détails de l'hôtel {location_id}: {e}")
        return {"error": str(e)}


@tool()
def get_restaurant_details(location_id: str) -> Dict[str, Any]:
    """
    Récupère les détails d'un restaurant à partir de son location_id.
    
    Args:
        location_id (str): Identifiant unique du restaurant sur TripAdvisor
        
    Returns:
        Dict[str, Any]: Détails du restaurant incluant le menu, photos, avis, etc.
    """
    try:
        # Utilisation de l'API Content TripAdvisor pour obtenir les détails
        url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/details"
        params = {
            "language": "fr",
            "currency": "EUR",
            "key": Config.TRIPADVISOR_API_KEY
        }
        headers = {
            "accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Traitement des données réelles du restaurant
        restaurant_details = {
            "nom": data.get("name", ""),
            "description": data.get("description", ""),
            "adresse": data.get("address_obj", {}).get("address_string", ""),
            "rating": data.get("rating", ""),
            "num_reviews": data.get("num_reviews", ""),
            "catégorie": data.get("category", {}).get("name", ""),
            "cuisine": [c.get("name", "") for c in data.get("cuisine", [])] if data.get("cuisine") else [],
            "téléphone": data.get("phone", ""),
            "website": data.get("website", ""),
            "email": data.get("email", ""),
            "prix": data.get("price_level", ""),
            "photo_url": data.get("photo", {}).get("images", {}).get("original", {}).get("url", "") if data.get("photo") else "",
            "horaires": data.get("hours", {}).get("weekday_text", [])
        }
        
        return restaurant_details
    except Exception as e:
        print(f"Erreur lors de la récupération des détails du restaurant {location_id}: {e}")
        return {"error": str(e)}
