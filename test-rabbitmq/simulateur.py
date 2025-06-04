# simulateur.py
from event_bus import publish_event
import time

for i in range(5):
    publish_event("client.created", {"id": i, "nom": f"Client {i}"})
    time.sleep(1)
