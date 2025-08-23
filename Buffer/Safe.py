import threading
import time
import random
from collections import deque

# Shared buffer and lock
buffer = deque()
MAX_SIZE = 100
condition = threading.Condition()

def safe_producer():
    while True:
        p1 = random.randint(1, 100)
        p2 = random.randint(101, 200)

        with condition:
            while len(buffer) >= MAX_SIZE - 1:
                print("[Producer] Buffer is full, stopping production.")
                condition.wait()
                

            print(f"[Producer] Produced pair: {p1}, {p2}")
            buffer.append(p1)
            print(f"[Producer] Placed P1 in buffer: {p1}")
            buffer.append(p2)
            print(f"[Producer] Placed P2 in buffer: {p2}")
            print(f"[Producer] Buffer size: {len(buffer)}")

            condition.notify_all()

        time.sleep(random.uniform(0.1, 0.4))

def safe_consumer():
    while True:
        with condition:
            # Remove the buffer size check to force error
            # while len(buffer) < 2:
            #     print("[Consumer] Buffer empty, waiting...")
            #     condition.wait()

            # This will raise IndexError if buffer is empty
            p1 = buffer.popleft()
            print(f"[Consumer] Fetched P1: {p1}")
            p2 = buffer.popleft()
            print(f"[Consumer] Fetched P2: {p2}")
            print(f"[Consumer] Packaged pair: {p1}, {p2}")

            condition.notify_all()

        time.sleep(random.uniform(0.2, 0.6))

# Start threads
threads = []

for _ in range(3):
    t = threading.Thread(target=safe_producer)
    t.daemon = True
    t.start()
    threads.append(t)

for _ in range(3):
    t = threading.Thread(target=safe_consumer)
    t.daemon = True
    t.start()
    threads.append(t)

# Keep the main thread alive
while True:
    time.sleep(1)