from server import KVServer
from client import KVClient
from node import Node
from cluster import ClusterConfig
import time
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

NODES = [
    Node("node1", "localhost", 5001),
    Node("node2", "localhost", 5002),
    Node("node3", "localhost", 5003)
]

CLUSTER = ClusterConfig(
    nodes=NODES,
    replication_factor=3,
    write_quorum=2,
    read_quorum=2
)

def run_server(node_id: str):
    """Run a server for the specified node."""
    local_node = CLUSTER.find_node_by_id(node_id)
    
    logger.info(f"Starting {node_id} on {local_node.host}:{local_node.port}")
    
    server = KVServer(local_node, CLUSTER)
    try:
        server.start()
    except KeyboardInterrupt:
        logger.info(f"Shutting down {node_id}")
        server.stop()

def run_client_example():
    """Example client that connects to node1."""
    # Connect to any node (they all coordinate)
    client = KVClient(host="localhost", port=5001)
    client.connect()
    
    print("Testing distributed KV Store...")
    
    # Test PUT (should replicate to 3 nodes, wait for 2)
    print("\n1. PUT user:123 = 'Alice'")
    success = client.put("user:123", "Alice")
    print(f"   Result: {'Success' if success else 'Failed'}")
    
    print("\n2. GET user:123")
    value = client.get("user:123")
    print(f"   Result: {value}")
    
    print("\n3. PUT user:456 = 'Bob'")
    client.put("user:456", "Bob")
    
    print("\n4. GET user:456")
    value = client.get("user:456")
    print(f"   Result: {value}")
    
    client.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py server <node_id>   # Start a server node")
        print("  python main.py client             # Run client example")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "server":
        if len(sys.argv) < 3:
            print("Please specify node_id: node1, node2, or node3")
            sys.exit(1)
        node_id = sys.argv[2]
        run_server(node_id)
    
    elif command == "client":
        run_client_example()
    
    else:
        print(f"Unknown command: {command}")