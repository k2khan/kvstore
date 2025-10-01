from storage import Storage
from protocol import Request, Response
from operation import Operation
import socket 
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KVServer:
    def __init__(self, host: str = "localhost", port: int = 5000):
        self.host = host
        self.port = port
        self.store = Storage()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._running = False
    
    def start(self):
        logger.info("Started Server \n")

        self._running = True
        self._socket.bind((self.host, self.port))
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.listen(5) # accept a max of 5 connections

        while self._running:
            try:
                client_socket, address = self._socket.accept()
                logger.info(f"Accepted connection from addres: {address}")
                client_thread = threading.Thread(target=self._handle_client, args=(client_socket,))
                client_thread.daemon = True
                client_thread.start()
            
            except Exception as e:
                if self._running:
                    logger.info(f"Unable to handle request for address: {address}. Exception: {e}")

    def stop(self):
        if self._socket:
            self._socket.close()

    def _handle_client(self, client_socket):
        try:
            while True:
                data = b""
                while b"\n" not in data:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                
                # decode input bytes into python string
                request_data = data.decode("utf-8").strip()

                try:
                    request = Request.from_json(request_data)
                    response = self._process_request(request)
                except Exception as e:
                    logger.error(f"Unable to process request: {request_data}. Error: {e}")

                response_data = response.to_json() + '\n'
                client_socket.send(response_data.encode("utf-8"))
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            client_socket.close()
    
    def _process_request(self, request: Request) -> Response:
        op = request.operation

        if op == Operation.GET.value:
            result = self.store.get(request.key)
            if result:
                return Response(True, result)
            return Response(False)
        elif op == Operation.PUT.value:
            return Response(self.store.put(request.key, request.value, request.timestamp))
        elif op == Operation.DELETE.value:
            return Response(self.store.delete(request.key))
        elif op == Operation.PING.value:
            return Response(True, "Pong")
        else:
            return Response(False, f"Malformed operation: {op}")
        
