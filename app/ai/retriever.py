from langchain_chroma import Chroma

cities_chroma = Chroma

def retrieve_similar_cities(query: str, k: int = 5) -> list[dict]:
    """Retrieve similar cities from the Chroma vector store based on a query.

    Args:
        query (str): The input query to search for similar cities.
        k (int): The number of similar cities to retrieve. Default is 5.

    Returns:
        List[dict]: A list of dictionaries containing metadata of similar cities.
    """
    results = cities_chroma.similarity_search_with_score(query, k=k, collection_name="tourivoire_cities")
    return [result[0].metadata for result in results]