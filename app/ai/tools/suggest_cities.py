from langchain_core.tools import tool

from app.ai.retriever import retrieve_similar_cities


@tool()
def suggest_cities_rag(query) -> list[dict]:
    """Suggest cities based on themes, duration, and budget in french."""
    print(query)
    similar_cities = retrieve_similar_cities("Abidjan", k=5)
    print(similar_cities)
    return similar_cities
