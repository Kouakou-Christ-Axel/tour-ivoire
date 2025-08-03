# TourIvoire – Assistant touristique intelligent pour la Côte d’Ivoire

TourIvoire est un agent conversationnel (chatbot) déployé sur Telegram (et WhatsApp dans le futur) qui génère
automatiquement des itinéraires touristiques personnalisés en Côte d’Ivoire, selon les préférences de l'utilisateur :
budget, centres d’intérêt, durée du séjour, événements en cours, etc.

## Fonctionnalités

- Chatbot sur Telegram/WhatsApp : dialogue simple pour collecter les préférences de l’utilisateur

- Génération d’itinéraires multi-jours avec lieux à visiter, événements, activités

- Utilisation de LangChain + GPT-4 pour générer un plan de voyage cohérent

- Intégration d’événements en temps réel (scraping de sites comme Tikerama)

- Estimation de budget par activité ou journée

- Export de l’itinéraire (texte, image, lien Google Maps)

## Technologies utilisées

- Language : Python 3.10+

- Orchestration IA : LangChain, OpenAI GPT-4

- Bot Interface : Telegram Bot API (possibilité d’ajouter WhatsApp avec Twilio)

- Scraping : requests, BeautifulSoup, Selenium (selon sources)

- Base de données : PostgreSQL (via Docker)

- Containerisation : Docker & Docker Compose

## Lancer le projet en local

1. Cloner le dépôt :
```bash
   git clone https://github.com/Kouakou-Christ-Axel/tour-ivoire
    cd tour-ivoire
```
2. Créer un environnement virtuel et l’activer :

```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. Installer les dépendances :

```bash
   pip install -r requirements.txt
```

4. Configurer les variables d’environnement :
```bash
    cp .env.example .env
    nano .env  # Modifier les variables nécessaires (API keys, DB, etc.)
```
5. Lancer la base de données PostgreSQL avec Docker :

```bash
   docker-compose up -d
``` 

6. Lancer le bot Telegram :

```bash
   python main.py
```
   