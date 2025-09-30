from typing import Optional

"""
Goal: Define request/response format for client-server communication. Use JSON for simplicity.

Use json.dumps() and json.loads()
Operations: "GET", "PUT", "DELETE", "PING"
"""
class Request:
    def __init__(self, operation: str, key: str, value: Optional[str] = None, timestamp: Optional[float] = None):
        # TODO: Store these as instance variables
        pass

    def to_json(self) -> str:
        # TODO: Convert to JSON string
        # Format: {"op": "GET", "key": "user:123", "value": "john", "timestamp": 123.45}
        pass

    @staticmethod
    def from_json(data: str) -> 'Request':
        # TODO: Parse JSON string and create Request object
        pass

class Response:
    def __init__(self, success: bool, value: Optional[str] = None, error: Optional[str] = None):
        # TODO: Store these as instance variables
        pass

    def to_json(self) -> str:
        # TODO: Convert to JSON string
        # Format: {"sucess": true, "value": "john", "error": null}
        pass
    
    pass
    def from_json(self, data: str) -> 'Respone':
        # TODO:  Pqrse JSON string and create response object
        pass