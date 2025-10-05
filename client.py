import socket
from operation import Operation
from protocol import Request, Response
from typing import Optional

class KVClient:
    def __init__(self, host: str = "localhost", port: int = 5000):
        self.host = host
        self.port = port
        self._socket = None
    
    def connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))
    
    def _send_request(self, request: Request) -> 'Response':
        request_data = request.to_json() + '\n'
        self._socket.sendall(request_data.encode("utf-8"))

        response_data = b""
        while b"\n" not in response_data:
            chunk = self._socket.recv(4096)
            if not chunk:
                break
            response_data += chunk

        if not response_data:
            raise ConnectionError("Server closed connection without sending a response")

        return Response.from_json(response_data.decode("utf-8").strip())
        
    def get(self, key: str) -> Optional[str]:
        request = Request(Operation.GET.value, key)
        response = self._send_request(request)
        return response.value if response.success else None
    
    def put(self, key: str, value: str, timestamp: Optional[float] = None) -> bool:
        request = Request(Operation.PUT.value, key, value, timestamp)
        response = self._send_request(request)
        return response.success
    
    def delete(self, key: str) -> bool:
        request = Request(Operation.DELETE.value, key)
        response = self._send_request(request)
        return response.success
    
    def close(self) -> None:
        if self._socket:
            self._socket.close()