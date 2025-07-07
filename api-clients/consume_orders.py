# consume_orders.py (à placer dans l’API Clients)

import pika
import json

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Message reçu : {method.routing_key} → {message}")
    # Ici tu peux traiter les infos : afficher un message, log, ou futur traitement

def main():
    print("En attente des événements RabbitMQ (orders.created, orders.updated)...")

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='events', exchange_type='topic')
    queue_name = 'clients_listen_orders'
    channel.queue_declare(queue=queue_name, durable=True)

    channel.queue_bind(exchange='events', queue=queue_name, routing_key='orders.created')
    channel.queue_bind(exchange='events', queue=queue_name, routing_key='orders.updated')

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()
