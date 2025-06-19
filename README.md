# Ticket Stream Processor

Un producteur-consommateur Redpanda en Python pour simuler un système de tickets clients en temps réel.

## 🚀 Fonctionnalités

- Production de messages Kafka simulant des tickets clients
- Traitement en temps réel avec PySpark
- Architecture conteneurisée avec Docker Compose
- Monitoring possible via Redpanda Console 

## 🛠️ Stack technique

- Python 3.10+
- Kafka / Redpanda
- PySpark
- Docker & Docker Compose

## 📁 Structure du projet

```
.
├── producer/                 # Producteur Kafka (Python)
│   └── producer_ticket.py
├── consumer/                 # Consommateur PySpark
│   └── consumer_ticket.py
├── docker-compose.yml
└── README.md
```
## 📊 Diagramme du pipeline

```mermaid
flowchart LR
    A[Producer Python] -->|envoie messages JSON| B[Redpanda Broker]
    B -->|consommé via Spark Streaming| C[Consumer PySpark]
    C -->|traitement + agrégation| D[Résultats en mémoire/logs]
    B -->|monitoring| E[Redpanda Console]
```

## 🧪 Lancer le projet en local

1. Cloner le dépôt  
   ```bash
   git clone https://https://github.com/majinlyut/projet8.git
   cd ticket-stream-processor
   ```

2. Lancer les services avec Docker Compose  
   ```bash
   docker-compose up --build
   ```

3. Accéder à la Redpanda Console 
   [http://localhost:8080](http://localhost:8080)

4. Consulter les tickets crées
   ```bash
   docker-compose logs -f consumer
   ```
   
5. Consulter les tickets traités par Spark
   ```bash
   docker-compose logs -f producer
   ```

## 🎥 Démo en vidéo

[![Watch the video](https://img.youtube.com/vi/pB50tTuo0IM/maxresdefault.jpg)](https://www.youtube.com/watch?v=pB50tTuo0IM)



