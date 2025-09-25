from typing import Dict, Any

from langchain_core.tools import tool

from app.ai.tools.get_pois import get_pois, search_restaurants, search_hotels


@tool()
def plan_itinerary(
    city: str, 
    days: int = 3, # Nombre de jours du séjour
    interests: str = "culture, histoire, gastronomie",  # Intérêts du voyageur
    budget: str = "moyen"
) -> Dict[str, Any]:
    """
    Planifie un itinéraire touristique complet pour une ville donnée.
    
    Args:
        city (str) : Nom ville à visiter
        days (int, optional) : Nombre de jours du séjour. Par défaut 3.
        interests (str, optional) : Intérêts du voyageur (séparés par virgule). Par défaut "culture, histoire, gastronomie".
        budget (str, optional) : Budget du voyageur ("bas", "moyen", "élevé"). Par défaut "moyen".
    """
    try:
        print("Planification de l'itinéraire...")
        print(f"Ville: {city}, Jours: {days}, Intérêts: {interests}, Budget: {budget}")
        # Récupérer les attractions ville
        attractions = get_pois(city)
        if isinstance(attractions, list) and len(attractions) > 0 and "error" in attractions[0]:
            return {"error": attractions[0]["error"]}
        
        # Récupérer les restaurants ville
        restaurants = search_restaurants(city)
        if isinstance(restaurants, list) and len(restaurants) > 0 and "error" in restaurants[0]:
            return {"error": restaurants[0]["error"]}
            
        hotels = search_hotels(city)
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

            print(restaurants)
            
            daily_plan = {
                "jour": day,
                "matin": {
                    "petit_dejeuner": {
                        "nom": restaurants[breakfast_idx]["nom"] if len(restaurants) > breakfast_idx else "Non disponible",
                        "adresse": restaurants[breakfast_idx]["adresse"] if len(restaurants) > breakfast_idx else "Non disponible"
                    },
                    "activite": {
                        "nom": day_attractions[0]["nom"] if len(day_attractions) > 0 else "Non disponible",
                        "adresse": day_attractions[0]["adresse"] if len(day_attractions) > 0 and "adresse" in day_attractions[0] else "Non disponible"
                    }
                },
                "midi": {
                    "dejeuner": {
                        "nom": restaurants[lunch_idx]["nom"] if len(restaurants) > lunch_idx else "Non disponible",
                        "adresse": restaurants[lunch_idx]["adresse"] if len(restaurants) > lunch_idx else "Non disponible"
                    },
                    "activite": {
                        "nom": day_attractions[1]["nom"] if len(day_attractions) > 1 else "Non disponible",
                        "adresse": day_attractions[1]["adresse"] if len(day_attractions) > 1 and "adresse" in day_attractions[1] else "Non disponible"
                    }
                },
                "soir": {
                    "diner": {
                        "nom": restaurants[dinner_idx]["nom"] if len(restaurants) > dinner_idx else "Non disponible",
                        "adresse": restaurants[dinner_idx]["adresse"] if len(restaurants) > dinner_idx else "Non disponible"
                    },
                    "activite": {
                        "nom": day_attractions[2]["nom"] if len(day_attractions) > 2 else "Non disponible",
                        "adresse": day_attractions[2]["adresse"] if len(day_attractions) > 2 and "adresse" in day_attractions[2] else "Non disponible"
                    }
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
        print(f"Erreur lors planification de l'itinéraire pour {city}: {e}")
        return {"error": str(e)}
