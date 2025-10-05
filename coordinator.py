from typing import List, Optional, Tuple
from cluster import ClusterConfig
from storage import Storage
from protocol import Request, Response
from node import Node
from operation import Operation
import time
import threading
import logging

logger = logging.getLogger(__name__)

class ReplicationCoordinator:
    """
    Coordinates replication across multiple nodes.
    Implements quorum reads and writes.
    """
    
    def __init__(self, cluster: ClusterConfig, local_storage: Storage, local_node: Node):
        self.cluster = cluster
        self.local_storage = local_storage
        self.local_node = local_node
    
    def coordinate_put(self, key: str, value: str, timestamp: Optional[float] = None) -> Response:
        """
        Coordinate a PUT across N replicas, wait for W acknowledgments.
        """
        if timestamp is None:
            timestamp = time.time()
        
        preference_list = self.cluster.get_preference_list(key)
        logger.info(f"PUT {key}={value} to nodes: {preference_list}")
        
        req = Request(Operation.PUT.value, key, value, timestamp, forwarded=True)
        responses = self._send_to_nodes(preference_list, req)
        successful = sum(1 for r in responses if r and r.success)
        
        logger.info(f"PUT {key}: {successful}/{len(preference_list)} nodes succeeded (need {self.cluster.write_quorum})")
        
        if successful >= self.cluster.write_quorum:
            return Response(success=True)
        else:
            return Response(success=False, error=f"Only {successful}/{self.cluster.write_quorum} nodes acknowledged")
    
    def coordinate_get(self, key: str) -> Response:
        preference_list = self.cluster.get_preference_list(key)
        nodes_to_read = preference_list[:self.cluster.read_quorum]
        logger.info(f"GET {key} from nodes: {nodes_to_read}")

        responses = self._send_to_nodes(
            nodes_to_read,
            Request(Operation.GET.value, key, forwarded=True)
        )

        successful = [(r, i) for i, r in enumerate(responses) if r and r.success]
        logger.info(f"GET {key}: {len(successful)}/{self.cluster.read_quorum} nodes responded")

        if len(successful) < self.cluster.read_quorum:
            return Response(success=False, error="Could not reach read quorum")

        return successful[0][0]

        
    def _send_to_nodes(self, nodes: List[Node], request: Request) -> List[Optional[Response]]:
        """
        Send a request to multiple nodes in parallel using threads.
        Returns a list of responses (None if node failed).
        """
        responses = [None] * len(nodes)
        threads = []
        
        def send_to_node(index: int, node: Node):
            # Special case: if this is the local node, just call storage directly
            if node == self.local_node:
                responses[index] = self._handle_local_request(request)
            else:
                responses[index] = node.send_request(request)
        
        # Create threads
        for i, node in enumerate(nodes):
            thread = threading.Thread(target=send_to_node, args=(i, node))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete (with timeout)
        for thread in threads:
            thread.join(timeout=3.0)
        
        return responses
    
    def _handle_local_request(self, request: Request) -> Response:
        """
        Handle a request locally without network round-trip.
        """
        op = request.operation
        
        if op == Operation.GET.value:
            value = self.local_storage.get(request.key)
            if value is not None:
                return Response(success=True, value=value)
            return Response(success=False, error="Key not found")
        
        elif op == Operation.PUT.value:
            success = self.local_storage.put(request.key, request.value, request.timestamp)
            return Response(success=success)
        
        elif op == Operation.DELETE.value:
            success = self.local_storage.delete(request.key)
            return Response(success=success)
        
        else:
            return Response(success=False, error=f"Unknown operation: {op}")