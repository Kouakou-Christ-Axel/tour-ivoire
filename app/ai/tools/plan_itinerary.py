import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from langchain_core.tools import tool
from app.config import Config
from app.ai.tools.get_pois import get_pois, search_restaurants, search_hotels

@tool()
def plan_itinerary(
    city: str, 
    days: int = 3, 
    interests: str = "culture, histoire, gastronomie", 
    budget: str = "moyen"
) -> Dict[str, Any]:
    """
    Planifie un itinéraire touristique complet pour une ville donnée.
    
    Args:
        city (str): Nom de la ville à visiter
        days (int, optional): Nombre de jours du séjour. Par défaut 3.
        interests (str, optional): Intérêts du voyageur (séparés par virgule). Par défaut "culture, histoire, gastronomie".
        budget (str, optional): Budget du voyageur ("bas", "moyen", "élevé"). Par défaut "moyen".
        
    Returns:
        Dict[str, Any]: Itinéraire détaillé avec attractions, restaurants et hôtels
    """
    try:
        # Récupérer les attractions de la ville
        attractions = get_pois(city)
        if isinstance(attractions, list) and len(attractions) > 0 and "error" in attractions[0]:
            return {"error": attractions[0]["error"]}
        
        # Récupérer les restaurants de la ville
        restaurants = search_restaurants(city)
        if isinstance(restaurants, list) and len(restaurants) > 0 and "error" in restaurants[0]:
            return {"error": restaurants[0]["error"]}
        
        # Récupérer les hôtels selon le budget
        max_price = 1000  # Par défaut (budget moyen)
        min_stars = 3     # Par défaut (budget moyen)
        
        if budget.lower() == "bas":
            max_price = 100
            min_stars = 1
        elif budget.lower() == "élevé" or budget.lower() == "eleve":
            max_price = 5000
            min_stars = 4
            
        hotels = search_hotels(city, min_stars=min_stars, max_price=max_price)
        if isinstance(hotels, list) and len(hotels) > 0 and "error" in hotels[0]:
            return {"error": hotels[0]["error"]}
        
        # Planifier l'itinéraire jour par jour
        daily_plans = []
        
        # Limiter le nombre d'attractions par jour en fonction du nombre de jours
        attractions_per_day = min(3, max(1, len(attractions) // days))
        
        # Assurer qu'on a assez d'attractions
        if len(attractions) == 0:
            return {"error": f"Aucune attraction trouvée pour {city}"}
            
        # Assurer qu'on a assez de restaurants
        if len(restaurants) == 0:
            return {"error": f"Aucun restaurant trouvé pour {city}"}
        
        # Créer un itinéraire pour chaque jour
        for day in range(1, days + 1):
            start_idx = (day - 1) * attractions_per_day % len(attractions)
            day_attractions = []
            
            for i in range(attractions_per_day):
                idx = (start_idx + i) % len(attractions)
                day_attractions.append(attractions[idx])
                
            # Choisir des restaurants pour ce jour
            breakfast_idx = (day - 1) % len(restaurants)
            lunch_idx = (day + 1) % len(restaurants)
            dinner_idx = (day + 2) % len(restaurants)
            
            daily_plan = {
                "jour": day,
                "matin": {
                    "petit_dejeuner": restaurants[breakfast_idx]["nom"] if len(restaurants) > breakfast_idx else "Non disponible",
                    "activite": day_attractions[0]["nom"] if len(day_attractions) > 0 else "Non disponible"
                },
                "midi": {
                    "dejeuner": restaurants[lunch_idx]["nom"] if len(restaurants) > lunch_idx else "Non disponible",
                    "activite": day_attractions[1]["nom"] if len(day_attractions) > 1 else "Non disponible"
                },
                "soir": {
                    "diner": restaurants[dinner_idx]["nom"] if len(restaurants) > dinner_idx else "Non disponible",
                    "activite": day_attractions[2]["nom"] if len(day_attractions) > 2 else "Non disponible"
                }
            }
            
            daily_plans.append(daily_plan)
            
        # Recommander un hôtel
        recommended_hotel = hotels[0] if hotels else {"nom": "Aucun hôtel trouvé"}
        
        # Construire l'itinéraire complet
        itinerary = {
            "ville": city,
            "duree_sejour": days,
            "interets": interests,
            "budget": budget,
            "hotel_recommande": recommended_hotel,
            "planning_journalier": daily_plans
        }
        
        return itinerary
    except Exception as e:
        print(f"Erreur lors de la planification de l'itinéraire pour {city}: {e}")
        return {"error": str(e)}
