import socket
from typing import Optional

from protocol import Request, Response
from storage import Operation

class KVClient:
    """
    Client for connecting to KV store server.
    
    Usage:
        client = KVClient("localhost", 5000)
        client.connect()
        client.put("key1", "value1")
        value = client.get("key1")
        client.close()
    """
    def __init__(self, host: str = "localhost", port: int = 5000):
        self.host = host
        self.port = port
        self._socket = None

    def connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))
    
    def _send_request(self, request: Request) -> Response:
        request_data = request.to_json() + '\n'
        self._socket.sendall(data.encode("utf-8"))

        response_data = b""
        while b'\n' not in response_data:
            chunk = self._socket.recv(4096)
            if not chunk:
                raise ConnectionError("Server closed connection.")
            response_data += chunk
        
        return Response.from_json(response_data.decode("utf-8").strip())
    
    def get(self, key: str) -> Optional[str]:
        request = Request(Operation.GET.value, key)
        response = self._send_request(request)

        if response.success:
            return response.value
        return None
    
    def put(self, key: str, value: str, timestamp: Optional[float] = None) -> bool:
        request = Request(Operation.PUT.value, key, value, timestamp)
        response = self._send_request(request)

        return response.success
    
    def delete(self, key: str) -> bool:
        request = Request(Operation.DELETE.value, key)
        response = self._send_request(request)

        return response.success

    def close(self):
        if self._socket:
            self._socket.close()