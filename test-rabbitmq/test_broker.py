import threading
import time
from event_bus import publish_event, consume_event

# Variable partagée entre les threads
message_recu = []

# Fonction de test : sera appelée quand un message est reçu
def on_message(data):
    print("Message capté par le test :", data)
    message_recu.append(data)

# Fonction pour lancer le consumer dans un thread séparé
def lancer_consumer():
    consume_event("client.updated", on_message)

# 1. Lancer le consumer en arrière-plan
thread = threading.Thread(target=lancer_consumer, daemon=True)
thread.start()

# 2. Attendre un peu que le consumer soit bien prêt
time.sleep(1)

# 3. Envoyer un message test
message_test = {
    "id": 99,
    "nom": "Test Auto"
}
publish_event("client.updated", message_test)

# 4. Attendre la réception du message
time.sleep(2)  # laisser le temps au message d'arriver

# 5. Vérifier le résultat
if message_recu and message_recu[0] == message_test:
    print("TEST RÉUSSI : message reçu correctement")
else:
    print("TEST ÉCHOUÉ : aucun message ou mauvais contenu reçu")
