import socket
from protocol import Request, Response
from typing import Optional

class Node:
    """
    Represents a single node in the distributed cluster.
    Handles sending requests to other nodes.
    """
    
    def __init__(self, node_id: str, host: str, port: int):
        self.node_id = node_id
        self.host = host
        self.port = port
    
    def __repr__(self):
        return f"Node({self.node_id}, {self.host}:{self.port})"
    
    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.node_id == other.node_id
    
    def __hash__(self):
        return hash(self.node_id)
    
    def send_request(self, request: Request, timeout: float = 2.0) -> Optional[Response]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((self.host, self.port))
            
            request_data = request.to_json() + '\n'
            sock.sendall(request_data.encode('utf-8'))
            
            response_data = b""
            while b"\n" not in response_data:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
            
            sock.close()
            
            if not response_data or response_data.strip() == b"":
                return None
            
            return Response.from_json(response_data.decode('utf-8').strip())
            
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            return None
        except Exception as e:
            print(f"Error sending request to {self}: {e}")
            return None