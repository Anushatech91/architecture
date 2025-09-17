import redis
from queue import Queue

class NotificationQueue:
    def __init__(self):
        self.redis_client = redis.Redis()
        self.queue = Queue()
    
    def publish(self, message):
        self.queue.put(message)
        
    def subscribe(self):
        return self.queue.get()