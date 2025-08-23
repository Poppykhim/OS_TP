import threading
import time
import random
from collections import deque

# Shared buffer (bounded to 100 particles)

buffer_capacity = 100

buffer = deque(maxlen=buffer_capacity)
# Semaphores
empty_slots = threading.Semaphore(buffer_capacity)  # Initially 100 empty slots
full_slots = threading.Semaphore(0)                 # Initially 0 full slots

# Mutex lock for buffer access
buffer_lock = threading.Lock()
condition = threading.Condition()

# Unsafe Producer
def unsafe_producer():
    while True:
        p1 = random.randint(1, 100)
        p2 = random.randint(101, 200)
        with condition:
            while len(buffer) >= buffer_capacity  - 1:
                print("[Producer] Buffer is full, stopping production.")
                condition.wait()
        empty_slots.acquire()  # Wait if buffer is full
        empty_slots.acquire()  # Need two empty slots for two items
        print(f"[Producer] Produced pair: {p1}, {p2}")

        # No wait/check – directly accessing buffer
        buffer.append(p1)  # May overflow silently
        print(f"[Producer] Placed P1 in buffer: {p1}")
        buffer.append(p2)
        print(f"[Producer] Placed P2 in buffer: {p2}")

        full_slots.release()  # Signal one full slot
        full_slots.release()  # Signal second full slot

        time.sleep(random.uniform(0.1, 0.4))

# Unsafe Consumer
def unsafe_consumer():
    while True:

        full_slots.acquire()  # Wait if buffer is empty
        full_slots.acquire()  # Need two full slots to consume a pair

        try:
            # Direct access without checking length
            p1 = buffer.popleft()  # May cause IndexError if empty
            print(f"[Consumer] Fetched P1: {p1}")
            p2 = buffer.popleft()
            print(f"[Consumer] Fetched P2: {p2}")
            print(f"[Consumer] Packaged pair: {p1}, {p2}")
        except IndexError:
            print("[Consumer] Tried to consume from empty buffer! 💥")

        empty_slots.release()  # Signal one empty slot freed
        empty_slots.release()  # Signal second empty slot freed

        time.sleep(random.uniform(0.2, 0.6))

# Start threads
producer_thread = threading.Thread(target=unsafe_producer)
consumer_thread = threading.Thread(target=unsafe_consumer)

producer_thread.start()
consumer_thread.start()
