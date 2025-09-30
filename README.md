# Project Roadmap

## Phase 1: Single-Node KV Store
Build the foundation without distribution.

### Core Features
- In-memory hash map storage  
- Simple TCP server (key-value protocol)  
- Basic operations: `GET`, `PUT`, `DELETE`  
- Optional: Write-ahead log (WAL) for durability  
- Optional: Snapshot to disk  

**Why start here:** Get comfortable with the language, networking, and serialization before adding complexity.  

---

## Phase 2: Add Replication
Make it distributed across multiple nodes.

### Features
- Node discovery (hardcoded cluster config to start)  
- Replication factor `N` (copy data to N nodes)  
- Quorum reads/writes (`R + W > N` for consistency)  
- Coordinator node pattern (any node can handle requests)  

### Key Concepts
- Network communication between nodes  
- Handling node failures during writes (sloppy quorum)  
- Conflict resolution (last-write-wins with timestamps)  

---

## Phase 3: Consistent Hashing & Partitioning 
Scale beyond the memory of a single node.

### Features
- Consistent hashing ring with virtual nodes  
- Partition data across nodes  
- Route requests to correct nodes  
- Handle node additions/removals (data migration)  

### Challenges
- Rebalancing data when cluster changes  
- Maintaining replication while rebalancing  

---

## Phase 4: Failure Detection & Recovery 
Make it production-grade resilient.

### Features
- Gossip protocol for node failure detection  
- Hinted handoff (temporary storage when node is down)  
- Read repair (fix inconsistencies during reads)  
- Anti-entropy with Merkle trees (background reconciliation)  

---

## Phase 5: Polish & Observability 
Make it real.

### Features
- Metrics (latency, throughput, consistency stats)  
- Admin API (cluster status, rebalancing)  
- Client library  
- Basic benchmarking tools  
