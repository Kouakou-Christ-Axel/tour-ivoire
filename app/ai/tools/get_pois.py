from langchain_core.tools import tool

@tool(parse_docstring=True)
def get_pois(location: str, poi_type: str) -> str:
    """Get points of interest (POIs) of a specific type in a given location.

    Args:
        location (str): The location to search for POIs (e.g., "New York City").
        poi_type (str): The type of POI to search for (e.g., "restaurants", "museums").

    Returns:
        str: A list of POIs in the specified location and type.
    """
    # In a real implementation, this function would call an external API
    # such as Google Places API, Foursquare API, etc. to get real data.
    # Here, we return a mock response for demonstration purposes.

    mock_pois = {
        "New York City": {
            "restaurants": ["Joe's Pizza", "Le Bernardin", "Katz's Delicatessen"],
            "museums": ["The Met", "MoMA", "American Museum of Natural History"]
        },
        "San Francisco": {
            "restaurants": ["Tartine Bakery", "Zuni Cafe", "State Bird Provisions"],
            "museums": ["SFMOMA", "California Academy of Sciences", "de Young Museum"]
        }
    }

    pois = mock_pois.get(location, {}).get(poi_type, [])
    if not pois:
        return f"No {poi_type} found in {location}."

    return f"Here are some {poi_type} in {location}: " + ", ".join(pois)