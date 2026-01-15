"""
🧠 AETHERBOT DEEP MEMORY SYSTEM
================================
Persistent vector-based memory for intelligent context retention.

The memory system provides:
- Short-term memory: Current session context
- Long-term memory: Persistent cross-session knowledge
- Episodic memory: Past analysis records
- Semantic memory: Code pattern understanding
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import pickle

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    from qdrant_client.http.models import Distance, VectorParams, PointStruct
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False


class MemoryType(Enum):
    """Types of memory in the AETHERBOT system."""
    SHORT_TERM = "short_term"      # Current session
    LONG_TERM = "long_term"        # Persistent knowledge
    EPISODIC = "episodic"          # Past analyses
    SEMANTIC = "semantic"          # Code patterns
    WORKING = "working"            # Active processing


@dataclass
class MemoryEntry:
    """A single memory entry in the AETHERBOT system."""
    id: str
    content: str
    memory_type: MemoryType
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    importance: float = 0.5  # 0-1 scale
    access_count: int = 0
    last_accessed: Optional[str] = None
    related_memories: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None


@dataclass
class AnalysisRecord:
    """Record of a past analysis for episodic memory."""
    repo_name: str
    repo_path: str
    timestamp: str
    entropy_score: float
    severity: str
    key_findings: List[str]
    recommendations: List[str]
    guilt_index: float
    security_score: float
    performance_score: float


class AetherMemory:
    """
    🧠 AETHERBOT DEEP MEMORY

    A sophisticated memory system that provides:
    - Persistent storage across sessions
    - Vector-based semantic search
    - Memory consolidation (short → long term)
    - Pattern recognition from past analyses
    - Context-aware retrieval
    """

    MEMORY_DIR = Path.home() / ".aetherbot" / "memory"
    VECTOR_DIM = 384

    # Collection names for different memory types
    COLLECTIONS = {
        MemoryType.SHORT_TERM: "aether_short_term",
        MemoryType.LONG_TERM: "aether_long_term",
        MemoryType.EPISODIC: "aether_episodic",
        MemoryType.SEMANTIC: "aether_semantic",
        MemoryType.WORKING: "aether_working"
    }

    def __init__(self,
                 use_vector_db: bool = True,
                 qdrant_host: str = "localhost",
                 qdrant_port: int = 6333,
                 in_memory: bool = True):
        """
        Initialize AETHERBOT memory system.

        Args:
            use_vector_db: Whether to use Qdrant for vector storage
            qdrant_host: Qdrant server host
            qdrant_port: Qdrant server port
            in_memory: Use in-memory Qdrant (no external server needed)
        """
        self.use_vector_db = use_vector_db and QDRANT_AVAILABLE
        self.qdrant_host = qdrant_host
        self.qdrant_port = qdrant_port
        self.in_memory = in_memory

        # Initialize storage
        self.MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        self.client: Optional[QdrantClient] = None
        self._local_memory: Dict[MemoryType, List[MemoryEntry]] = {
            mt: [] for mt in MemoryType
        }

        # Load persistent memory
        self._load_persistent_memory()

        # Initialize vector DB if available
        if self.use_vector_db:
            self._init_vector_db()

    def _init_vector_db(self) -> bool:
        """Initialize Qdrant vector database."""
        try:
            if self.in_memory:
                self.client = QdrantClient(":memory:")
            else:
                self.client = QdrantClient(
                    host=self.qdrant_host,
                    port=self.qdrant_port
                )

            # Create collections for each memory type
            for memory_type, collection_name in self.COLLECTIONS.items():
                self._ensure_collection(collection_name)

            return True
        except Exception as e:
            print(f"[AETHERBOT] Vector DB init failed: {e}")
            self.use_vector_db = False
            return False

    def _ensure_collection(self, name: str):
        """Ensure a collection exists in Qdrant."""
        try:
            collections = self.client.get_collections().collections
            if name not in [c.name for c in collections]:
                self.client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(
                        size=self.VECTOR_DIM,
                        distance=Distance.COSINE
                    )
                )
        except Exception:
            pass

    def _load_persistent_memory(self):
        """Load memory from disk."""
        memory_file = self.MEMORY_DIR / "memory_state.pkl"
        if memory_file.exists():
            try:
                with open(memory_file, 'rb') as f:
                    saved_memory = pickle.load(f)
                    # Only load long-term and episodic memory
                    if MemoryType.LONG_TERM in saved_memory:
                        self._local_memory[MemoryType.LONG_TERM] = saved_memory[MemoryType.LONG_TERM]
                    if MemoryType.EPISODIC in saved_memory:
                        self._local_memory[MemoryType.EPISODIC] = saved_memory[MemoryType.EPISODIC]
                    if MemoryType.SEMANTIC in saved_memory:
                        self._local_memory[MemoryType.SEMANTIC] = saved_memory[MemoryType.SEMANTIC]
            except Exception as e:
                print(f"[AETHERBOT] Memory load failed: {e}")

    def _save_persistent_memory(self):
        """Save memory to disk."""
        memory_file = self.MEMORY_DIR / "memory_state.pkl"
        try:
            # Only save long-term, episodic, and semantic memory
            to_save = {
                MemoryType.LONG_TERM: self._local_memory[MemoryType.LONG_TERM],
                MemoryType.EPISODIC: self._local_memory[MemoryType.EPISODIC],
                MemoryType.SEMANTIC: self._local_memory[MemoryType.SEMANTIC]
            }
            with open(memory_file, 'wb') as f:
                pickle.dump(to_save, f)
        except Exception as e:
            print(f"[AETHERBOT] Memory save failed: {e}")

    def _generate_embedding(self, text: str) -> List[float]:
        """Generate a simple embedding vector for text."""
        # Simple hash-based embedding (for production, use sentence-transformers)
        vector = [0.0] * self.VECTOR_DIM
        text_bytes = text.encode('utf-8')

        for i, byte in enumerate(text_bytes[:1000]):  # Limit input
            idx = (i + byte) % self.VECTOR_DIM
            vector[idx] += (byte / 255.0 - 0.5) * 0.1

        # Normalize
        magnitude = sum(v * v for v in vector) ** 0.5
        if magnitude > 0:
            vector = [v / magnitude for v in vector]

        return vector

    def _generate_id(self, content: str, memory_type: MemoryType) -> str:
        """Generate unique ID for memory entry."""
        hash_input = f"{content}:{memory_type.value}:{datetime.now().isoformat()}"
        return hashlib.md5(hash_input.encode()).hexdigest()

    # =========================================================================
    # CORE MEMORY OPERATIONS
    # =========================================================================

    def remember(self,
                 content: str,
                 memory_type: MemoryType = MemoryType.SHORT_TERM,
                 metadata: Optional[Dict] = None,
                 importance: float = 0.5) -> str:
        """
        Store a memory in the AETHERBOT system.

        Args:
            content: The content to remember
            memory_type: Type of memory (short/long term, episodic, etc.)
            metadata: Additional metadata
            importance: How important this memory is (0-1)

        Returns:
            Memory ID
        """
        memory_id = self._generate_id(content, memory_type)
        embedding = self._generate_embedding(content)

        entry = MemoryEntry(
            id=memory_id,
            content=content,
            memory_type=memory_type,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {},
            importance=importance,
            embedding=embedding
        )

        # Store locally
        self._local_memory[memory_type].append(entry)

        # Store in vector DB if available
        if self.use_vector_db and self.client:
            try:
                collection = self.COLLECTIONS[memory_type]
                self.client.upsert(
                    collection_name=collection,
                    points=[PointStruct(
                        id=abs(hash(memory_id)) % (2**63),
                        vector=embedding,
                        payload={
                            "memory_id": memory_id,
                            "content": content,
                            "timestamp": entry.timestamp,
                            "importance": importance,
                            "metadata": metadata or {}
                        }
                    )]
                )
            except Exception:
                pass

        # Auto-save for persistent memory types
        if memory_type in [MemoryType.LONG_TERM, MemoryType.EPISODIC, MemoryType.SEMANTIC]:
            self._save_persistent_memory()

        return memory_id

    def recall(self,
               query: str,
               memory_type: Optional[MemoryType] = None,
               limit: int = 5,
               min_importance: float = 0.0) -> List[MemoryEntry]:
        """
        Recall memories similar to a query.

        Args:
            query: Search query
            memory_type: Specific memory type to search (None = all)
            limit: Maximum results
            min_importance: Minimum importance threshold

        Returns:
            List of relevant memories
        """
        results = []
        query_embedding = self._generate_embedding(query)

        # Search vector DB if available
        if self.use_vector_db and self.client:
            types_to_search = [memory_type] if memory_type else list(MemoryType)

            for mt in types_to_search:
                try:
                    collection = self.COLLECTIONS[mt]
                    hits = self.client.search(
                        collection_name=collection,
                        query_vector=query_embedding,
                        limit=limit
                    )

                    for hit in hits:
                        if hit.payload.get("importance", 0) >= min_importance:
                            entry = MemoryEntry(
                                id=hit.payload.get("memory_id", ""),
                                content=hit.payload.get("content", ""),
                                memory_type=mt,
                                timestamp=hit.payload.get("timestamp", ""),
                                metadata=hit.payload.get("metadata", {}),
                                importance=hit.payload.get("importance", 0.5)
                            )
                            results.append((hit.score, entry))
                except Exception:
                    pass

        # Also search local memory
        types_to_search = [memory_type] if memory_type else list(MemoryType)
        for mt in types_to_search:
            for entry in self._local_memory[mt]:
                if entry.importance >= min_importance:
                    # Simple text matching for local search
                    if query.lower() in entry.content.lower():
                        results.append((0.8, entry))

        # Sort by score and deduplicate
        results.sort(key=lambda x: x[0], reverse=True)
        seen_ids = set()
        unique_results = []
        for score, entry in results:
            if entry.id not in seen_ids:
                seen_ids.add(entry.id)
                unique_results.append(entry)
                if len(unique_results) >= limit:
                    break

        return unique_results

    def forget(self, memory_id: str, memory_type: MemoryType) -> bool:
        """Remove a specific memory."""
        # Remove from local
        self._local_memory[memory_type] = [
            m for m in self._local_memory[memory_type]
            if m.id != memory_id
        ]

        # Remove from vector DB
        if self.use_vector_db and self.client:
            try:
                collection = self.COLLECTIONS[memory_type]
                self.client.delete(
                    collection_name=collection,
                    points_selector=models.PointIdsList(
                        points=[abs(hash(memory_id)) % (2**63)]
                    )
                )
            except Exception:
                pass

        self._save_persistent_memory()
        return True

    # =========================================================================
    # EPISODIC MEMORY - ANALYSIS RECORDS
    # =========================================================================

    def record_analysis(self, record: AnalysisRecord) -> str:
        """
        Record a completed analysis in episodic memory.

        Args:
            record: The analysis record to store

        Returns:
            Memory ID
        """
        content = json.dumps(asdict(record), default=str)
        metadata = {
            "type": "analysis_record",
            "repo_name": record.repo_name,
            "entropy_score": record.entropy_score,
            "severity": record.severity
        }

        # Higher importance for critical findings
        importance = 0.5 + (record.entropy_score / 200)  # 0.5-1.0 based on entropy

        return self.remember(
            content=content,
            memory_type=MemoryType.EPISODIC,
            metadata=metadata,
            importance=min(1.0, importance)
        )

    def get_similar_analyses(self,
                             repo_name: str = "",
                             severity: str = "",
                             limit: int = 5) -> List[AnalysisRecord]:
        """
        Find similar past analyses.

        Args:
            repo_name: Repository name to search for
            severity: Severity level filter
            limit: Maximum results

        Returns:
            List of similar analysis records
        """
        query = f"analysis {repo_name} {severity}".strip()
        memories = self.recall(query, MemoryType.EPISODIC, limit=limit)

        records = []
        for memory in memories:
            try:
                data = json.loads(memory.content)
                record = AnalysisRecord(**data)
                if (not repo_name or repo_name.lower() in record.repo_name.lower()) and \
                   (not severity or severity.lower() == record.severity.lower()):
                    records.append(record)
            except Exception:
                pass

        return records

    # =========================================================================
    # SEMANTIC MEMORY - PATTERNS
    # =========================================================================

    def learn_pattern(self, pattern: str, examples: List[str], category: str) -> str:
        """
        Learn a code pattern for future recognition.

        Args:
            pattern: Description of the pattern
            examples: Example code snippets
            category: Category (security, performance, etc.)

        Returns:
            Memory ID
        """
        content = json.dumps({
            "pattern": pattern,
            "examples": examples,
            "category": category,
            "learned_at": datetime.now().isoformat()
        })

        return self.remember(
            content=content,
            memory_type=MemoryType.SEMANTIC,
            metadata={"category": category, "type": "pattern"},
            importance=0.7
        )

    def recognize_pattern(self, code_snippet: str) -> List[Dict]:
        """
        Try to recognize patterns in a code snippet.

        Args:
            code_snippet: Code to analyze

        Returns:
            List of recognized patterns with confidence
        """
        memories = self.recall(code_snippet, MemoryType.SEMANTIC, limit=10)

        patterns = []
        for memory in memories:
            try:
                data = json.loads(memory.content)
                patterns.append({
                    "pattern": data.get("pattern", ""),
                    "category": data.get("category", ""),
                    "confidence": memory.importance
                })
            except Exception:
                pass

        return patterns

    # =========================================================================
    # MEMORY CONSOLIDATION
    # =========================================================================

    def consolidate(self):
        """
        Consolidate memories - move important short-term to long-term.
        This simulates sleep-based memory consolidation in humans.
        """
        # Find important short-term memories
        for entry in self._local_memory[MemoryType.SHORT_TERM]:
            if entry.importance >= 0.7 or entry.access_count >= 3:
                # Promote to long-term
                self.remember(
                    content=entry.content,
                    memory_type=MemoryType.LONG_TERM,
                    metadata=entry.metadata,
                    importance=entry.importance
                )

        # Clear short-term memory
        self._local_memory[MemoryType.SHORT_TERM] = []
        self._local_memory[MemoryType.WORKING] = []

        self._save_persistent_memory()

    def get_memory_stats(self) -> Dict[str, int]:
        """Get statistics about memory usage."""
        stats = {}
        for mt in MemoryType:
            stats[mt.value] = len(self._local_memory[mt])
        return stats

    def clear_session(self):
        """Clear session-specific memory (short-term and working)."""
        self._local_memory[MemoryType.SHORT_TERM] = []
        self._local_memory[MemoryType.WORKING] = []
