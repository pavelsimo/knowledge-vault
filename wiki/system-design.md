# System Design

System design is the process of defining the architecture, interfaces, and data for a system that satisfies specific requirements. It requires thinking from infrastructure all the way down to how data is stored and served. Good system design decisions made early are hard to reverse — poor ones compound as systems grow.

## Source

- `raw/06-system-design/System Design.md`
- Course by Karan Pratap Singh: https://karanpratapsingh.com/courses/system-design

---

## Chapter I: Networking Fundamentals

### IP Addressing

**IPv4:** 32-bit dot-decimal notation (e.g., `102.22.192.181`). ~4 billion addresses — insufficient for modern internet scale.

**IPv6:** 128-bit hexadecimal notation (e.g., `2001:0db8:85a3:0000:0000:8a2e:0370:7334`). ~340 undecillion addresses.

| Type | Description |
|---|---|
| **Public** | One address for the whole network (assigned by ISP to router) |
| **Private** | Unique per device within the local network |
| **Static** | Manually assigned, does not change — used for servers, geo-location services |
| **Dynamic** | Assigned by DHCP; changes over time — common for consumer devices |

### OSI Model

Seven-layer model for network communication, from top (user-facing) to bottom (physical):

| Layer | Name | Responsibility |
|---|---|---|
| 7 | **Application** | User-facing protocols: HTTP, SMTP, FTP |
| 6 | **Presentation** | Translation, encryption/decryption, compression |
| 5 | **Session** | Opens/closes communication sessions; synchronizes data with checkpoints |
| 4 | **Transport** | End-to-end delivery; breaks data into segments; reassembles at destination |
| 3 | **Network** | Routing packets across networks; finds best physical path |
| 2 | **Data Link** | Transfer between devices on the same network; packets → frames |
| 1 | **Physical** | Physical cables, switches; data → bit stream (1s and 0s) |

### TCP vs UDP

| Feature | TCP | UDP |
|---|---|---|
| Connection | Connection-oriented (handshake required) | Connectionless |
| Reliability | Guaranteed delivery and ordering | Best effort; no delivery guarantee |
| Error checking | Built-in | Minimal |
| Speed | Slower (overhead for acks and retransmissions) | Faster |
| Use cases | File transfer, web pages, email | Streaming, gaming, DNS, video calls |

Use TCP when data integrity matters. Use UDP when lowest latency is critical and late data is worse than lost data.

### DNS (Domain Name System)

DNS translates human-readable domain names into IP addresses through a hierarchical resolution chain:

1. Client queries **DNS Resolver** (step 1 → step 8 recursive response)
2. DNS Resolver queries **Root Server** iteratively (steps 2, 3) → returns TLD server address
3. DNS Resolver queries **TLD Server** (steps 4, 5) → returns authoritative server address
4. DNS Resolver queries **Authoritative Server** (steps 6, 7) → returns final IP address
5. DNS Resolver returns the IP to the client (step 8)

The distinction between recursive (client ↔ resolver: one round trip) and iterative (resolver ↔ each server: resolver does the legwork) is key to understanding DNS latency and caching.

**DNS record types:** A (IPv4 address), AAAA (IPv6 address), CNAME (canonical name/alias), MX (mail server), TXT (arbitrary text/verification).

### Load Balancing

A load balancer distributes incoming traffic across multiple servers, preventing any single server from becoming a bottleneck.

**Layer 4 (Transport):** Routes based on IP and TCP/UDP ports — fast but limited context.

**Layer 7 (Application):** Routes based on HTTP headers, URLs, cookies — enables content-aware routing (e.g., route `/api` to API servers, `/static` to CDN).

**Algorithms:**
- **Round Robin** — requests distributed sequentially
- **Least Connections** — route to server with fewest active connections
- **IP Hash** — same client always routes to same server (session affinity)
- **Weighted Round Robin** — higher-capacity servers receive proportionally more traffic

**Redundant load balancers:** Deploy two load balancers in active-passive or active-active mode. If the active one fails, the passive one takes over (failover). Eliminates load balancer as a single point of failure.

### Clustering

A cluster is a group of interconnected nodes that work together as a single system, providing high availability and increased throughput.

A typical cluster topology has a primary node (Node 1) connected to multiple secondary nodes (Nodes 2–7), all within a shared network boundary. Traffic is distributed across nodes and work can be redistributed when any node fails.

**Active-Active:** all nodes handle traffic simultaneously; if one fails, the others absorb its load.

**Active-Passive:** one node handles all traffic; the passive node(s) stand by as hot standby, taking over instantly on failover.

### Caching

Caching stores frequently accessed data in fast storage (memory) to reduce latency and database load.

**Write strategies:**

| Strategy | How it works | Tradeoff |
|---|---|---|
| **Write-through** | Data written to cache and storage simultaneously | Consistent but adds write latency |
| **Write-around** | Client writes directly to storage, bypasses cache | Cache stays clean for frequently-read data; cold cache for new writes |
| **Write-back** | Client writes to cache only; cache flushes to storage asynchronously | Fast writes; risk of data loss if cache fails before flush |

The write-around cache diagram shows: Client → Read → Cache (fast path); Client → Write → Storage directly (cache not involved for writes). This pattern suits read-heavy workloads where write performance isn't critical.

**Eviction policies:** LRU (Least Recently Used), LFU (Least Frequently Used), FIFO, Random.

**Distributed cache:** cache layer spread across multiple nodes (e.g., Redis Cluster). No single point of failure; scales horizontally.

**Global cache:** single shared cache accessed by all application servers — simpler but can become a bottleneck.

### CDN (Content Delivery Network)

A CDN places content on geographically distributed edge servers so users get responses from the nearest location rather than the origin.

The CDN topology: a single **Origin Server** (e.g., London) connects via dashed backbone links to **Edge Servers** deployed in regional data centers (USA, Japan, Brazil, Australia). End users in each region are served by their nearest edge server rather than the London origin. This dramatically reduces latency for global audiences.

**Pull CDN:** edge fetches content from origin on first request; caches until TTL expires.
**Push CDN:** content is explicitly pushed to edge nodes when it changes — better for large files that don't change frequently.

### Proxy

**Forward proxy:** sits in front of client machines. Multiple clients → Forward Proxy → Internet → Servers. Hides client identity; enables content filtering, corporate firewalls, caching.

**Reverse proxy:** sits in front of server machines. Clients → Internet → Reverse Proxy → Server pool. Hides server topology; enables load balancing, SSL termination, rate limiting, caching, web application firewall.

### Availability and Scalability

**Availability (nines):**

| SLA | Downtime per year |
|---|---|
| 99% (two nines) | ~87.6 hours |
| 99.9% (three nines) | ~8.76 hours |
| 99.99% (four nines) | ~52.6 minutes |
| 99.999% (five nines) | ~5.26 minutes |

**Scalability:**
- **Vertical scaling (scale up):** add more CPU/RAM to existing server — simpler, but has physical limits and creates a single point of failure
- **Horizontal scaling (scale out):** add more servers — complex to coordinate but effectively unlimited, more fault tolerant

---

## Chapter II: Databases

### SQL vs NoSQL

| Property | SQL | NoSQL |
|---|---|---|
| Data model | Rigid schema (tables, rows, columns) | Flexible (document, key-value, graph, column) |
| Consistency | ACID by default | BASE by default (eventually consistent) |
| Scalability | Vertical (primarily) | Horizontal |
| Joins | Native and efficient | Application-level or limited |
| Best for | Financial systems, complex queries, reporting | High-throughput, unstructured/semi-structured data |

**NoSQL types:** Document (MongoDB), Key-Value (Redis), Wide Column (Cassandra), Graph (Neo4j).

### ACID vs BASE

**ACID** (SQL transactions):
- **Atomicity:** all operations succeed or all roll back — no partial transactions
- **Consistency:** database moves from one valid state to another
- **Isolation:** concurrent transactions don't interfere
- **Durability:** committed data survives failures (written to disk)

**BASE** (NoSQL/distributed):
- **Basically Available:** responds even during partial failures
- **Soft state:** state may change without input (due to eventual consistency)
- **Eventually consistent:** system converges to a consistent state over time

### CAP Theorem

In a distributed system, you can only guarantee two of three properties simultaneously:
- **Consistency (C):** every read returns the most recent write
- **Availability (A):** every request gets a response (not necessarily the most recent write)
- **Partition Tolerance (P):** system continues operating despite network splits

In practice, network partitions are unavoidable, so the real choice is **CP vs AP** during a partition:
- **CP** (e.g., HBase, MongoDB) — prioritize consistency; may reject requests during partition
- **AP** (e.g., Cassandra, CouchDB) — prioritize availability; may return stale data

### PACELC Theorem

CAP only addresses behavior during partitions. PACELC extends it to cover normal operation:

```
If (Partition):
    choose between Availability (A) vs Consistency (C)
Else (normal operation):
    choose between Latency (L) vs Consistency (C)
```

The decision tree: Partition occurs? **Yes** → trade off Availability vs Consistency. **No** → trade off Latency vs Consistency.

Most systems are either PA/EL (high availability, low latency, eventual consistency) or PC/EC (strong consistency at both partition and normal time).

### Database Replication

Replication copies data across multiple database nodes for redundancy and read scaling.

**Master-replica:** writes go to master; replicas serve reads and act as hot standbys.
**Multi-master:** multiple nodes accept writes; requires conflict resolution.

**Synchronous replication:** master waits for replica acknowledgment before confirming write — strong consistency, higher latency.
**Asynchronous replication:** master confirms write immediately; replica catches up — lower latency, risk of data loss on failover.

### Sharding

Sharding horizontally partitions data across multiple database nodes. Each shard holds a subset of rows.

The sharding diagram: an original table with rows A, B, C, D gets split into Shard 1 (rows A, B) and Shard 2 (rows C, D). Queries must be routed to the appropriate shard.

**Partitioning criteria:**
- **Range-based:** e.g., rows 1–1M on shard 1, 1M–2M on shard 2 — simple but can cause hot spots
- **Hash-based:** hash of a key determines shard — even distribution but complicates range queries
- **Directory-based:** lookup table maps keys to shards — flexible but single point of failure

### Consistent Hashing

Standard hash-based sharding requires re-mapping all keys when a node is added or removed. Consistent hashing minimizes reshuffling:
- Both nodes and keys are mapped to positions on a hash ring
- Each key is owned by the nearest node clockwise on the ring
- Adding or removing a node only affects the keys in that node's immediate range

Commonly used in distributed caches (Redis Cluster, Memcached), CDNs, and distributed databases.

### Distributed Transactions: Two-Phase Commit (2PC)

Distributed transactions span multiple nodes and require a coordinator to ensure atomicity:

**Phase 1 — Prepare:** Coordinator sends Prepare to all participant nodes (Node 0, Node 1). Each node locks resources and replies Ack (prepared).

**Phase 2 — Commit:** Once all nodes are prepared, Coordinator broadcasts Commit. Each node applies the transaction and acknowledges.

If any node fails to prepare → Coordinator sends Abort to all nodes, rolling back the transaction.

**Limitation:** 2PC is blocking — if the coordinator crashes after prepare but before commit, participants hold locks indefinitely until the coordinator recovers.

### Indexes

Indexes trade write performance for faster read performance. An index on a column creates a data structure (typically B-tree) that allows lookups in O(log n) instead of O(n) full table scans.

**Tradeoff:** every write (INSERT, UPDATE, DELETE) must also update all indexes on that table. Heavy indexing slows writes and increases storage.

**Use indexes on:** columns used in WHERE, JOIN, and ORDER BY. Avoid indexing columns with low cardinality (e.g., boolean fields).

---

## Chapter III: Distributed Architecture

### N-Tier Architecture

N-tier separates concerns across multiple horizontal layers. A typical 3-tier production setup:

```
Clients (browser, mobile)
  → Internet
    → Load Balancer
      → Web Servers (tier 1: presentation/static)
        → Load Balancer
          → API Servers (tier 2: business logic)
            → Load Balancer
              → DB Servers (tier 3: data)
```

Each tier can scale independently. Load balancers at each layer prevent single points of failure between tiers.

### Message Queues and Pub-Sub

**Message Queue:** point-to-point async delivery. Producer publishes a message; consumer reads and acknowledges it; message is removed. Each message consumed by exactly one consumer. Examples: RabbitMQ, Amazon SQS.

**Publish-Subscribe:** producer publishes to a topic; all subscribers to that topic receive the message. Decouples producers from consumers; enables fan-out. Examples: Apache Kafka, Google Pub/Sub, AWS SNS.

### Monoliths vs Microservices

| Property | Monolith | Microservices |
|---|---|---|
| Deployment | Single deployable unit | Each service deploys independently |
| Scaling | Scale the whole application | Scale individual services |
| Development | Simpler initially; complex at large scale | More operational overhead; better team autonomy |
| Failures | One bug can affect the whole system | Failures are isolated to a service |
| Communication | In-process function calls | Network calls (REST, gRPC, message queues) |

Start with a monolith. Decompose into services only when team size, deployment frequency, or scaling requirements justify the operational overhead.

### API Gateway

An API gateway is a reverse proxy that sits in front of microservices, handling cross-cutting concerns:
- Authentication and authorization
- Rate limiting and throttling
- Request routing to the appropriate service
- SSL termination
- Response caching
- Request/response transformation
- Logging and monitoring

Without an API gateway, every microservice must implement authentication, rate limiting, and logging independently — creating duplication and inconsistency.

### REST vs GraphQL vs gRPC

| Feature | REST | GraphQL | gRPC |
|---|---|---|---|
| Protocol | HTTP/1.1 | HTTP/1.1 or HTTP/2 | HTTP/2 |
| Format | JSON/XML | JSON | Protocol Buffers (binary) |
| Overfetching | Common | None (client specifies fields) | None |
| Schema | OpenAPI (optional) | Strongly typed schema required | `.proto` file (required) |
| Best for | Public APIs, simple CRUD | Complex queries, mobile clients | Internal microservices, streaming |

### Long Polling, WebSockets, Server-Sent Events

**Long polling:** client sends a request and the server holds it open until data is available, then responds. Client immediately sends another request. Simulates push over HTTP — high overhead, not truly real-time.

**WebSockets:** full-duplex persistent connection over a single TCP connection. Client and server can both push data at any time. Ideal for chat, gaming, collaborative editing.

**Server-Sent Events (SSE):** the SSE diagram shows a single HTTP request from the client, followed by a stream of multiple server responses over that same connection. Unidirectional (server → client only). Simpler than WebSockets for push-only use cases (live feeds, notifications, dashboards).

---

## Chapter IV: Advanced Patterns

### Circuit Breaker

The circuit breaker pattern prevents cascading failures when a downstream service is unavailable:

- **Closed:** requests flow normally; failures are counted
- **Open:** after failure threshold exceeded, all requests fail fast (no downstream calls) — circuit "trips"
- **Half-Open:** after a timeout, one trial request is allowed; if it succeeds, circuit closes; if it fails, stays open

This prevents a slow or failed service from exhausting resources across the entire system.

### Rate Limiting

Rate limiting controls how many requests a client can make in a given time window, protecting the system from abuse and overload.

**Algorithms:**
- **Token bucket:** each client gets a bucket of tokens that refills at a fixed rate; each request consumes a token — allows short bursts
- **Leaky bucket:** requests queue and are processed at a constant rate — no bursts, smooth flow
- **Fixed window counter:** count requests per fixed window (e.g., 100 req/minute) — simple but vulnerable to burst at window boundaries
- **Sliding window:** smoother version of fixed window using rolling counts

### Geohashing and Quadtrees

Used for location-based services (finding nearby drivers, restaurants, etc.).

**Geohashing:** encode latitude/longitude into a short alphanumeric string (Base-32). Nearby locations share a common prefix. Example: San Francisco `37.7564, -122.4016` → geohash `9q8yy9mf`. Allows proximity queries by string prefix comparison.

**Quadtrees:** a tree where each internal node has exactly four children, recursively subdividing 2D space into four quadrants. Each leaf stores points (e.g., driver locations). Efficient range queries: search only the quadrants that overlap your query radius.

For ride-sharing: store driver geohashes in memory (Redis), use quadtree for range queries, index by geohash prefix for fast lookups.

### SLA, SLO, SLI

| Term | Definition | Example |
|---|---|---|
| **SLI** (Service Level Indicator) | A measurable metric | 99.95% of requests return in < 200ms |
| **SLO** (Service Level Objective) | Target for an SLI | We commit to 99.9% availability monthly |
| **SLA** (Service Level Agreement) | Contract with customer specifying SLOs + penalties | "If uptime < 99.9%, credits are issued" |

Build from the inside out: measure SLIs → set SLOs → formalize SLAs with customers.

### Virtual Machines vs Containers

| Property | Virtual Machine | Container |
|---|---|---|
| Isolation | Full OS isolation (hypervisor) | Process-level isolation (shared kernel) |
| Startup time | Minutes | Seconds |
| Size | GBs (includes full OS) | MBs (only app + dependencies) |
| Overhead | High CPU/RAM overhead | Near-native performance |
| Best for | Strong isolation, legacy apps | Microservices, CI/CD, cloud-native |

### OAuth 2.0 and Authentication

**OAuth 2.0:** authorization framework — allows a third-party application to access resources on behalf of a user without exposing the user's credentials.

**OpenID Connect (OIDC):** identity layer on top of OAuth 2.0 — provides authentication (who is the user?), not just authorization.

**Single Sign-On (SSO):** authenticate once with an identity provider; access multiple services without re-authenticating. Used in enterprise (Okta, Active Directory, Google Workspace).

**TLS/mTLS:**
- TLS: server presents certificate; client verifies server identity
- mTLS (mutual TLS): both client and server present certificates — used in service meshes for zero-trust inter-service authentication

---

## Chapter V: System Design Interview Case Studies

### URL Shortener (e.g., bit.ly)

**Key requirements:** generate a unique short code for any URL; redirect short code → original URL at low latency; handle billions of URLs.

**Core decisions:**
- Short code generation: hash the URL (MD5/SHA256, take first 7 chars) or auto-increment ID encoded in Base62
- Storage: key-value store (Redis + persistent DB) — the mapping is a simple lookup
- Redirect: 301 (permanent, client caches) vs 302 (temporary, every request hits server)
- Scale reads with CDN/cache; writes are infrequent

### WhatsApp / Chat System

**Key requirements:** 1:1 messaging, group chats, online/offline status, push notifications.

**Core decisions:**
- Use WebSockets for persistent bidirectional connections between clients and servers
- Message queues (Kafka) to buffer messages between chat servers
- Fan-out for group chats: message broker distributes to each recipient's message queue
- Push notifications via APNs (iOS) / FCM (Android) for offline users
- Store messages in Cassandra (high write throughput, time-ordered reads per conversation)

### Twitter / Social Feed

**Key requirements:** post tweets, follow users, read home timeline (all tweets from people you follow).

**Fan-out approaches:**
- **Push (fan-out on write):** on post, write tweet to every follower's timeline cache — fast reads, expensive writes for users with millions of followers
- **Pull (fan-out on read):** on timeline load, query and merge tweets from all followed users — expensive reads, cheap writes
- **Hybrid:** push for normal users; pull for celebrity accounts (too many followers to push to)

### Netflix / Video Streaming

**Key requirements:** global video delivery, adaptive bitrate streaming, personalized recommendations.

**Core decisions:**
- CDN is the central piece: content pre-positioned at edge servers globally
- Adaptive bitrate streaming (MPEG-DASH/HLS): player switches quality based on bandwidth
- Personalization: collaborative filtering + deep learning recommendation models
- Separate CDN from API servers — content delivery and metadata/auth are different scaling problems

### Uber / Ride Sharing

**Key requirements:** real-time driver location updates, ride matching, surge pricing, payment.

**Core decisions:**
- **Location tracking:** WebSockets (push model) from drivers → servers continuously; not HTTP polling (creates unnecessary load)
- **Ride matching:** geohashing for fast proximity lookup; quadtree in Redis for range queries
- **Race conditions:** mutex around ride matching logic; all actions transactional
- **Payments:** third-party processor (Stripe/PayPal) + webhook for payment events
- **Scale:** Kafka for notifications (APNs/FCM), consistent hashing for data partitioning, read replicas for databases

---

## Related Topics

- [[distributed-training]] — distributed systems applied to ML training (data/tensor/pipeline parallelism)
- [[mlops]] — deploying ML models in production with the same reliability principles
- [[rag]] — retrieval-augmented systems require caching, vector search, and API design
- [[gpu-cuda]] — GPU cluster topology and PCIe bandwidth constraints in distributed ML
- [[ai-agents]] — multi-agent orchestration as a distributed system problem
