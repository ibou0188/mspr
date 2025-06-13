# consumer.py

import pika
import json

def traitement_message(body):
    # Fonction appelée quand un message est reçu
    data = json.loads(body)
    print(" Message reçu :", data)

# Connexion à RabbitMQ (local)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# On déclare l'exchange (comme dans publisher.py)
channel.exchange_declare(exchange='events', exchange_type='topic')

# Création d'une file temporaire unique pour écouter les messages
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# On s'abonne à tous les messages du type "client.*"
channel.queue_bind(exchange='events', queue=queue_name, routing_key='client.*')

# Dès qu’un message est reçu, on l’envoie à la fonction `traitement_message`
def callback(ch, method, properties, body):
    traitement_message(body)

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print("En attente de messages... (Arrêter = Ctrl + C)")
channel.start_consuming()
