"""
Goal: Client library to connect to the server and send requests.


"""
class KVClient:
    def __init__(self, host: str = "localhost", port: int = 5000):
        # TODO: Store host, port
        # TODO: Initialize socket to None
        pass
    
    def connect(self):
        # TODO: Create socket and connect to server
        pass
    
    def _send_request(self, request: Request) -> Response:
        # TODO: Serialize request to JSON + newline
        # TODO: Send to server
        # TODO: Read response until newline
        # TODO: Parse and return Response object
        pass
    
    def get(self, key: str) -> Optional[str]:
        # TODO: Create GET request
        # TODO: Send and return the value from response
        pass
    
    def put(self, key: str, value: str, timestamp: Optional[float] = None) -> bool:
        # TODO: Create PUT request
        # TODO: Send and return success status
        pass
    
    def delete(self, key: str) -> bool:
        # TODO: Create DELETE request
        # TODO: Send and return success status
        pass
    
    def close(self):
        # TODO: Close the socket
        pass