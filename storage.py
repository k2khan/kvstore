from typing import Optional
import threading
import time

class Storage:
    def __init__(self):
        self.store = {}
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[str]:
        with self._lock:
            if key not in self.store:
                return None
            return self.store[key][0]

    def put(self, key: str, value: Optional[str] = None, timestamp: Optional[float] = None) -> bool:
        with self._lock:
            if not timestamp:
                timestamp = time.time()

            if key not in self.store:
                self.store[key] = (value, timestamp)
            else:
                _, previous_timestamp = self.store[key]
                if timestamp > previous_timestamp: # ensure last write wins
                    self.store[key] = (value, timestamp)
                else:
                    return False # didn't successfully write... return false

            return True

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self.store:
                del self.store[key]
                return True
            return False