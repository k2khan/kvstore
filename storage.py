from datetime import time
from enum import Enum
from typing import Dict, List, Optional
import threading

class Operation(Enum):
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    PING = "PING"

class Storage:
    def __init__(self):
        self.store: Dict[str, tuple] = {}
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[str]:
        with self._lock:
            if key in self.store:
                return self.store[key][0]
            return None
    
    def put(self, key: str, value: str, timestamp: Optional[float] = None) -> bool:
        if not timestamp:
            timestamp = time.time()

        with self._lock:
            if key in self.store:
                last_timestamp = self.store[key][1]
                
                if timestamp < last_timestamp:
                    return False

                self.store[key] = (value, timestamp)
                return True

            self.store[key] = (value, timestamp)
            return True

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self.store:
                del self.store[key]
                return True
            return False

    def size(self) -> int:
        with self._lock:
            return len(self.store)
    
    def keys(self) -> List[str]:
        with self._lock:
            return list(self.store.keys())