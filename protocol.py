from typing import Optional
import json

class Request:
    """
    Client request format.
    
    Example JSON:
    {"op": "PUT", "key": "user:123", "value": "john", "timestamp": 1234567890.0}
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
        return Request(operation=obj["op"], key=obj["key"], value=obj.get("value"), timestamp=obj.get("timestamp"))

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

    def from_json(self, data: str) -> 'Response':
        obj = json.loads(data)
        return Response(success=obj["success"], value=obj.get("value"), error=obj.get("error"))