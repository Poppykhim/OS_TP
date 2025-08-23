import threading
import time
import random
from collections import deque

# Shared buffer (bounded to 100 particles)
buffer = deque(maxlen=100)

# Semaphores for synchronization
empty_slots = threading.Semaphore(100)  # Initially 100 empty slots (buffer capacity)
filled_slots = threading.Semaphore(0)   # Initially 0 filled slots (items available)
buffer_lock = threading.Lock()          # Mutex for buffer access

# Safe Producer with semaphores
def safe_producer():
    while True:
        p1 = random.randint(1, 100)
        p2 = random.randint(101, 200)
        print(f"[Producer] Produced pair: {p1}, {p2}")

        # Wait for empty slots (blocks if buffer is full) - PREVENTS OVERFLOW
        empty_slots.acquire()  # wait() - Must have space before adding
        empty_slots.acquire()  # Need 2 empty slots for the pair
        
        # Critical section - access buffer safely
        with buffer_lock:
            buffer.append(p1)
            print(f"[Producer] Placed P1 in buffer: {p1}")
            buffer.append(p2)
            print(f"[Producer] Placed P2 in buffer: {p2}")
            print(f"[Producer] Buffer size: {len(buffer)}")

        # Signal that items are available for consumers
        filled_slots.release()  # signal() - increment filled slots
        filled_slots.release()  # Signal for both items added

        time.sleep(random.uniform(0.1, 0.4))

# Safe Consumer with semaphores  
def safe_consumer():
    while True:
        # Wait for filled slots (blocks if buffer is empty) - PREVENTS UNDERFLOW
        filled_slots.acquire()  # wait() - Must have items before consuming
        filled_slots.acquire()  # Need 2 items for the pair
        
        # Critical section - access buffer safely
        with buffer_lock:
            p1 = buffer.popleft()  # Guaranteed to have items due to semaphore
            print(f"[Consumer] Fetched P1: {p1}")
            p2 = buffer.popleft()  # Guaranteed to have items due to semaphore
            print(f"[Consumer] Fetched P2: {p2}")
            print(f"[Consumer] Packaged pair: {p1}, {p2}")
            print(f"[Consumer] Buffer size: {len(buffer)}")
                
        # Signal that slots are now available for producers
        empty_slots.release()  # signal() - increment empty slots
        empty_slots.release()  # Signal for both freed slots

        time.sleep(random.uniform(0.2, 0.6))

# Alternative implementation using Condition variables (bonus)
class BoundedBufferWithCondition:
    def __init__(self, max_size=100):
        self.buffer = deque()
        self.max_size = max_size
        self.condition = threading.Condition()
    
    def put(self, item):
        with self.condition:
            # Wait while buffer is full
            while len(self.buffer) >= self.max_size:
                print("[Producer] Buffer full, waiting...")
                self.condition.wait()
            
            self.buffer.append(item)
            print(f"[Producer] Added {item}, buffer size: {len(self.buffer)}")
            self.condition.notify_all()  # Wake up waiting consumers
    
    def get(self):
        with self.condition:
            # Wait while buffer is empty
            while len(self.buffer) == 0:
                print("[Consumer] Buffer empty, waiting...")
                self.condition.wait()
            
            item = self.buffer.popleft()
            print(f"[Consumer] Removed {item}, buffer size: {len(self.buffer)}")
            self.condition.notify_all()  # Wake up waiting producers
            return item

# Start threads with semaphore solution
print("=== Starting Safe Bounded Buffer with Semaphores ===")
producer_thread = threading.Thread(target=safe_producer, daemon=True)
consumer_thread = threading.Thread(target=safe_consumer, daemon=True)

producer_thread.start()
consumer_thread.start()

# Let it run for a while to demonstrate
try:
    time.sleep(10)
    print("\n=== Stopping demonstration ===")
except KeyboardInterrupt:
    print("\n=== Stopped by user ===")