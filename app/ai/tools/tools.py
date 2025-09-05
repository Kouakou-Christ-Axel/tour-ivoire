from app.ai.tools.get_pois import get_pois, search_restaurants, search_hotels, get_poi_details, get_hotel_details, get_restaurant_details
from app.ai.tools.plan_itinerary import plan_itinerary
from langchain_core.tools import tool
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from datetime import datetime, timedelta
from typing import Dict, List, Any

weather = OpenWeatherMapAPIWrapper()

@tool()
def get_travel_tips(destination: str, season: str = None) -> Dict[str, List[str]]:
    """
    Fournit des conseils de voyage pour une destination selon la saison.
    
    Args:
        destination (str): Nom de la destination (ville ou pays)
        season (str, optional): Saison de voyage (printemps, été, automne, hiver)
        
    Returns:
        Dict[str, List[str]]: Dictionnaire avec différentes catégories de conseils
    """

    if not season:
        current_month = datetime.now().month
        if 3 <= current_month <= 5:
            season = "printemps"
        elif 6 <= current_month <= 8:
            season = "été"
        elif 9 <= current_month <= 11:
            season = "automne"
        else:
            season = "hiver"
    
    # TODO: En base de données ou API pour des conseils réels
    seasonal_tips = {
        "printemps": [
            "Emportez un parapluie car les averses printanières sont fréquentes.",
            "C'est une excellente saison pour voir la floraison dans les parcs.",
            "Les températures peuvent varier considérablement, prévoyez des vêtements par couches."
        ],
        "été": [
            "N'oubliez pas la crème solaire et un chapeau.",
            "Hydratez-vous régulièrement en raison de la chaleur.",
            "Réservez vos hébergements à l'avance car c'est la haute saison touristique."
        ],
        "automne": [
            "Emportez des vêtements chauds pour les soirées fraîches.",
            "C'est une excellente période pour les promenades dans la nature et admirer les couleurs.",
            "Profitez des prix plus bas après la haute saison."
        ],
        "hiver": [
            "Prévoyez des vêtements chauds et imperméables.",
            "Vérifiez les horaires d'ouverture car certaines attractions peuvent être fermées.",
            "Renseignez-vous sur les festivités locales hivernales."
        ]
    }
    
    return {
        "destination": destination,
        "saison": season,
        "conseils_generaux": seasonal_tips[season],
        "conseils_sante": [
            "Vérifiez les recommandations sanitaires avant de partir.",
            "Emportez une trousse de premiers soins basique.",
            "Souscrivez à une assurance voyage."
        ],
        "conseils_securite": [
            "Gardez une copie de vos documents importants.",
            "Restez vigilant dans les zones touristiques.",
            "Enregistrez-vous auprès de votre ambassade si vous voyagez à l'étranger."
        ]
    }

@tool()
def estimate_travel_budget(
    destination: str, 
    duration: int, 
    travelers: int = 1,
    accommodation_level: str = "moyen"
) -> Dict[str, Any]:
    """
    Estime un budget de voyage pour une destination donnée.
    
    Args:
        destination (str): Nom de la destination
        duration (int): Durée du séjour en jours
        travelers (int, optional): Nombre de voyageurs. Par défaut 1.
        accommodation_level (str, optional): Niveau d'hébergement (économique, moyen, luxe). Par défaut "moyen".
        
    Returns:
        Dict[str, Any]: Budget estimatif détaillé
    """
    # Prix moyens par jour selon le niveau d'hébergement (en euros)
    accommodation_rates = {
        "économique": 50,
        "moyen": 100,
        "luxe": 250
    }
    
    # Prix moyens des repas par jour selon le niveau d'hébergement
    meal_rates = {
        "économique": 20,
        "moyen": 40,
        "luxe": 80
    }
    
    # Estimations d'activités par jour
    activity_rates = {
        "économique": 10,
        "moyen": 30,
        "luxe": 60
    }
    
    # Estimation transport local par jour
    transport_rates = {
        "économique": 5,
        "moyen": 15,
        "luxe": 30
    }
    
    # Calculer les coûts
    accommodation_cost = accommodation_rates.get(accommodation_level.lower(), 100) * duration * (travelers / 2 + 0.5)
    meal_cost = meal_rates.get(accommodation_level.lower(), 40) * duration * travelers
    activity_cost = activity_rates.get(accommodation_level.lower(), 30) * duration * travelers
    transport_cost = transport_rates.get(accommodation_level.lower(), 15) * duration * travelers
    
    # Estimation des coûts de transport international (très approximatif)
    international_transport = travelers * 300  # Valeur arbitraire
    
    # Budget total
    total_budget = accommodation_cost + meal_cost + activity_cost + transport_cost + international_transport
    
    return {
        "destination": destination,
        "durée_séjour": duration,
        "voyageurs": travelers,
        "niveau_hébergement": accommodation_level,
        "coûts_détaillés": {
            "hébergement": round(accommodation_cost, 2),
            "repas": round(meal_cost, 2),
            "activités": round(activity_cost, 2),
            "transport_local": round(transport_cost, 2),
            "transport_international": round(international_transport, 2)
        },
        "budget_total": round(total_budget, 2),
        "budget_par_personne": round(total_budget / travelers, 2),
        "budget_journalier": round(total_budget / duration, 2)
    }

agent_tools = [
    # suggest_cities_rag,
    weather.run,
    get_pois,
    get_poi_details,
    search_restaurants,
    get_restaurant_details,
    search_hotels,
    get_hotel_details,
    plan_itinerary,
    get_travel_tips,
    estimate_travel_budget
]