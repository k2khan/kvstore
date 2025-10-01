from protocol import Request
from server import KVServer
from client import KVClient
import time
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_server():
    server = KVServer()
    try:
        server.start()
    except KeyboardInterrupt as e:
        logger.info(f"Got keyboard interrupt: {e}")
        server.stop()

def run_client_example():
    client = KVClient()
    client.connect()

    client.put("Hamad", "Test1", time.time())
    client.put("Khurram", "Test2")

    print(client.get("Hamad"))
    print(client.get("Khurram"))

    client.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "client":
        run_client_example()
    else:
        run_server()