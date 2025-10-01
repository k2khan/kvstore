from operation import Operation
from typing import Optional
import json

""" Wire Protocol """
class Request:
    """
    Client request format.

    Example JSON:
    {"op": "GET", "key": "user123", "value": "5", "timestamp": 1234567890.0}
    """
    def __init__(self, operation: str, key: str, value: Optional[str] = None, timestamp: Optional[float] = None):
        self.operation = operation
        self.key = key
        self.value = value
        self.timestamp = timestamp

    def to_json(self) -> str:
        return json.dumps({
            "op": self.operation,
            "key": self.key,
            "value": self.value,
            "timestamp": self.timestamp
        })

    @staticmethod
    def from_json(data: str) -> 'Request':
        obj = json.loads(data)
        return Request(obj["op"], obj["key"], obj.get("value"), obj.get("timestamp"))

class Response:
    """
    Server response format.

    Example JSON:
    {"success": true, "value": "john", "error": null}
    """
    def __init__(self, success: bool, value: Optional[str] = None, error: Optional[str] = None):
        self.success = success 
        self.value = value
        self.error = error
    
    def to_json(self) -> str:
        return json.dumps({
            "success": self.success,
            "value": self.value,
            "error": self.error
        })
    
    @staticmethod
    def from_json(data: str) ->  'Response':
        obj = json.loads(data)
        return Response(obj["success"], obj.get("value"), obj.get("error"))