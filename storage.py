from typing import Optional

"""
Goal: Thread-safe in-memory hash map that stores key-value pairs with timestamps.

Use threading.RLock() for the lock
Use with self._lock: to acquire/release automatically
Store as self._data[key] = (value, timestamp)
"""
class Storage:
    def __init__(self):
        # TODO: Create a dictionary to store (value, timestamp) tuples
        # TODO: Create a threading lock for thead safety
        pass

    def get(self, key: str) -> Optional[str]:
        # TODO: Return value if key exists, None otherwise
        # Use the lock to make it thread safe
        pass
    
    def put(self, key: str, value: str, timestamp: Optional[float] = None) -> bool:
        # TODO: Store key-value pair with timestamp
        # If timestamp is None, use time.time()
        # Implement last-write wins: reject if incoming timestamp is older
        # Return True if stored, False if rejected
        pass

    def delete(self, key: str) -> bool:
        # TODO: Delete key if it exists
        # Return True if deleted, False if key didn't exist
        pass