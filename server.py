from protocol import Request, Response
from storage import Operation, Storage
import logging
import socket
import threading


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KVServer:
    def __init__(self, host: str = "localhost", port: int = 5000):
        self.host = host
        self.port = port
        self.storage = Storage()
        self._running = False
        self._server_socket = None

    def start(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(5)
        self._running = True

        logger.info(f"KV Server started on {self.host}:{self.port}")
        
        while self._running:
            try:
                client_socket, address = self._server_socket.accept()
                logger.info(f"Connection from {address}")
                
                # Handle each client in separate thread
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                if self._running:
                    logger.error(f"Error accepting connection: {e}")


    def _handle_client(self, client_socket):
        """Handle a single client connection."""
        try:
            while True:
                # Read request (newline-delimited JSON)
                data = b""
                while b"\n" not in data:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        return  # Client disconnected
                    data += chunk
                
                request_data = data.decode('utf-8').strip()
                logger.debug(f"Received: {request_data}")
                
                # Process request
                try:
                    request = Request.from_json(request_data)
                    response = self._process_request(request)
                except Exception as e:
                    response = Response(success=False, error=str(e))
                
                # Send response
                response_data = response.to_json() + "\n"
                client_socket.sendall(response_data.encode('utf-8'))
                
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def _process_request(self, request: Request) -> Response:
        """Process a client request and return response."""
        op = request.operation
        
        if op == Operation.GET.value:
            value = self.storage.get(request.key)
            if value is not None:
                return Response(success=True, value=value)
            else:
                return Response(success=False, error="Key not found")
        
        elif op == Operation.PUT.value:
            success = self.storage.put(request.key, request.value, request.timestamp)
            return Response(success=success)
        
        elif op == Operation.DELETE.value:
            success = self.storage.delete(request.key)
            return Response(success=success)
        
        elif op == Operation.PING.value:
            return Response(success=True, value="PONG")
        
        else:
            return Response(success=False, error=f"Unknown operation: {op}")
    
    def stop(self):
        """Stop the server."""
        self._running = False
        if self._server_socket:
            self._server_socket.close()
        logger.info("Server stopped")

