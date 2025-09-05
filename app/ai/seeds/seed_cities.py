import os
import json
from langchain_openai import OpenAIEmbeddings

from app.ai.retriever import cities_chroma


def seed_cities():
    """Seed the Chroma vector store with city data from a JSON file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "cities.json")

    with open(json_path, "r", encoding="utf-8") as f:
        cities = json.load(f)

    persist_directory = "chroma_db"
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

    docs = []
    metadatas = []
    ids = []

    for city in cities:
        docs.append(city["embedding_text"])
        ids.append(city["id"])

        metadatas.append({
            "id": city["id"],
            "name": city["name"],
            "country": city["country"],
            "themes": json.dumps(city.get("themes", [])),
            "avg_cost": city.get("avg_cost"),
            "ideal_durations": json.dumps(city.get("ideal_durations", [])),
            "seasonality": json.dumps(city.get("seasonality", {})),
            "safety_index": city.get("safety_index"),
            "crowd_level_by_month": json.dumps(city.get("crowd_level_by_month", {})),
            "access": json.dumps(city.get("access", {})),
            "short_pitch": city.get("short_pitch"),
            "sources": json.dumps(city.get("sources", [])),
        })

    cities_chroma.from_texts(
        texts=docs,
        embedding=embedding_model,
        metadatas=metadatas,
        ids=ids,
        collection_name="tourivoire_cities",
        persist_directory=persist_directory
    )

    print(f"✅ Seed terminé : {len(cities)} villes ajoutées dans Chroma (dossier: {persist_directory})")