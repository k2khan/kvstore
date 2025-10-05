from coordinator import ReplicationCoordinator
from node import Node
from cluster import ClusterConfig
from storage import Storage
from protocol import Request, Response
from operation import Operation
import socket 
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KVServer:
    def __init__(self, local_node: Node, cluster: ClusterConfig):
        self.host = local_node.host
        self.port = local_node.port
        self.local_node = local_node
        self.cluster = cluster
        
        self.store = Storage()
        self.coordinator = ReplicationCoordinator(cluster, self.store, local_node)
        
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._running = False
    
    def start(self):
        logger.info("Started Server \n")

        self._running = True
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self.host, self.port))
        self._socket.listen(5) # accept a max of 5 connections

        while self._running:
            try:
                client_socket, address = self._socket.accept()
                logger.info(f"Accepted connection from address: {address}")
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
            client_socket.settimeout(10.0)  # optional
            buffer = b""
            while True:
                # fill buffer until we have a full line
                while b"\n" not in buffer:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        # peer closed connection -> stop handling this client
                        return
                    buffer += chunk

                line, _, buffer = buffer.partition(b"\n")
                request_data = line.decode("utf-8").strip()

                if not request_data:
                    # ignore empty line(s); keep connection alive if client wants to pipeline
                    continue

                try:
                    request = Request.from_json(request_data)
                    response = self._process_request(request)
                    response_bytes = (response.to_json() + "\n").encode("utf-8")
                    client_socket.sendall(response_bytes)
                except Exception as e:
                    logger.error(f"Unable to process request: {request_data}. Error: {e}")
                    # safest is to close rather than try to write an error to a possibly-dead peer
                    return
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass

    
    def _process_request(self, request: Request) -> Response:
        op = request.operation

        if op == Operation.GET.value:
            if getattr(request, "forwarded", False):
                # Replica read: serve from local storage only
                value = self.store.get(request.key)
                if value is not None:
                    return Response(success=True, value=value)
                return Response(success=False, error="Key not found")
            else:
                # Client-originated GET: coordinate across replicas
                return self.coordinator.coordinate_get(request.key)

        elif op == Operation.PUT.value:
            if getattr(request, "forwarded", False):
                ok = self.store.put(request.key, request.value, request.timestamp)
                return Response(success=ok)
            else:
                return self.coordinator.coordinate_put(request.key, request.value, request.timestamp)

        elif op == Operation.DELETE.value:
            success = self.store.delete(request.key)
            return Response(success=success)

        elif op == Operation.PING.value:
            return Response(success=True, value="PONG")

        else:
            return Response(success=False, error=f"Unknown operation: {op}")

            
