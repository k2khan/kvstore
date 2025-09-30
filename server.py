from protocol import Request, Response

"""
Goal: TCP server that listens for connections and processes requests.

Use socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Use socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) to avoid "address already in use"
Read data in chunks: client_socket.recv(4096)
Keep reading until you see b"\n"
Decode with .decode('utf-8')
Send with client_socket.sendall(data.encode('utf-8'))
Use threading.Thread(target=self._handle_client, args=(client_socket,))
"""
class KVServer:
    def __init__(self, host: str = "localhost", port: int = 5000):
        # TODO: Store host, port
        # TODO: Create storage instance
        # TODO: Create server socket
        pass

    def start(self):
        # TODO: Create TCP socket, bing to host:port, listen
        # TODO: Accept connections in a loop
        # TODO: For each connection, spawn a thread to handle it
        # Call self._handle_client(client_socket) in the thread
        pass

    def _handle_client(self, client_socket):
        # TODO: Read data from socket until newline
        # TODO: Parse the json request (_process_request)
        # TODO: Send response back as JSON + newline
        # TODO: Close socket when done
        pass

    def _process_request(self, request: Request) -> Response:
        # TODO: Check request.operation
        # If "GET": call self.storage.get()
        # If "PUT": call self.storage.put()
        # If "DELETE": call self.storage.delete()
        # If "PING": return success response
        # Return appropriate response object
        pass

