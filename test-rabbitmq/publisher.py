import pika
import json

# Connexion à RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Déclaration de la file (elle doit être la même que celle du consumer)
channel.queue_declare(queue="order_created")

# Message simulé
message = {
    "event": "order.created",
    "data": {
        "id": "123",
        "customer_id": "11",
        "products": [{"name": "T-shirt", "price": "20.00"}]
    }
}

# Envoi du message
channel.basic_publish(
    exchange="",
    routing_key="order_created",
    body=json.dumps(message)
)

print("✅ Message envoyé à RabbitMQ")
connection.close()
