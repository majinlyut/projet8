import json
import random
import time
from datetime import datetime, timezone
from kafka import KafkaProducer
import os

# Définition des valeurs possibles
demande_possibles = ["Accès plateforme", "Erreur de facturation", "Demande d'information"]
types = ["technique", "administratif"]
priorites = ["haute", "moyenne", "faible"]

# Récupération du broker depuis la variable d'environnement
kafka_broker = os.getenv("KAFKA_BROKER", "redpanda-0:9092")

# Initialisation du producer Kafka avec sérialisation JSON
producer = KafkaProducer(
    bootstrap_servers=kafka_broker,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Boucle d'envoi des tickets
ticket_id = 1
while True:
    ticket = {
        "ticket_id": ticket_id,
        "client_id": random.randint(1000, 9999),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "demande": random.choice(demande_possibles),
        "type": random.choice(types),
        "priorité": random.choice(priorites)
    }
    print(f"Envoi du ticket : {ticket}", flush=True)

    producer.send("client_tickets", value=ticket)
    ticket_id += 1
    time.sleep(10)
