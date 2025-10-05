from typing import List
from node import Node

class ClusterConfig:
    """
    Configuration for the distributed cluster.
    Determines which nodes should store each key.
    """
    
    def __init__(self, nodes: List[Node], replication_factor: int = 3, 
                 write_quorum: int = 2, read_quorum: int = 2):
        """
        Args:
            nodes: List of all nodes in the cluster
            replication_factor (N): Number of nodes to replicate data to
            write_quorum (W): Number of nodes that must acknowledge a write
            read_quorum (R): Number of nodes to read from
        
        Consistency guarantee: If R + W > N, you get strong consistency
        """
        self.nodes = nodes
        self.replication_factor = replication_factor
        self.write_quorum = write_quorum
        self.read_quorum = read_quorum
        
        if replication_factor > len(nodes):
            raise ValueError(f"Replication factor {replication_factor} > number of nodes {len(nodes)}")
        if write_quorum > replication_factor:
            raise ValueError(f"Write quorum {write_quorum} > replication factor {replication_factor}")
        if read_quorum > replication_factor:
            raise ValueError(f"Read quorum {read_quorum} > replication factor {replication_factor}")
    
    def get_preference_list(self, key: str) -> List[Node]:
        """
        Get the list of N nodes that should store this key.
        
        For Phase 2: Simple strategy - just use first N nodes.
        In Phase 3, we'll implement consistent hashing for better distribution.
        """
        # Simple strategy: always use first N nodes
        # This is not production-ready (hotspots, no load balancing)
        # But it's simple for learning
        return self.nodes[:self.replication_factor]
    
    def find_node_by_id(self, node_id: str) -> Node:
        """Find a node by its ID."""
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        raise ValueError(f"Node {node_id} not found in cluster")