"""
🧠 NOVA Vector Store - Qdrant Integration
For semantic search and context retrieval.
"""

import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    from qdrant_client.http.models import Distance, VectorParams, PointStruct
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False


@dataclass
class CodeChunk:
    """A chunk of code with metadata."""
    id: str
    content: str
    filepath: str
    start_line: int
    end_line: int
    language: str
    function_name: Optional[str] = None
    class_name: Optional[str] = None


class VectorStore:
    """
    Vector database interface for NOVA.
    Uses Qdrant for storing and retrieving code embeddings.
    """

    COLLECTION_NAME = "nova_code_chunks"
    CHUNK_SIZE = 500  # characters
    CHUNK_OVERLAP = 50

    CODE_EXTENSIONS = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust',
        '.rb': 'ruby',
        '.php': 'php',
        '.c': 'c',
        '.cpp': 'cpp',
        '.cs': 'csharp',
    }

    def __init__(self, host: str = "localhost", port: int = 6333, in_memory: bool = True):
        """
        Initialize the vector store.

        Args:
            host: Qdrant server host
            port: Qdrant server port
            in_memory: Use in-memory storage (no external server needed)
        """
        self.host = host
        self.port = port
        self.in_memory = in_memory
        self.client: Optional[QdrantClient] = None
        self._initialized = False

    def initialize(self) -> bool:
        """Initialize the Qdrant client and collection."""
        if not QDRANT_AVAILABLE:
            return False

        try:
            if self.in_memory:
                self.client = QdrantClient(":memory:")
            else:
                self.client = QdrantClient(host=self.host, port=self.port)

            # Create collection if it doesn't exist
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.COLLECTION_NAME not in collection_names:
                self.client.create_collection(
                    collection_name=self.COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=384,  # For simple hash-based vectors
                        distance=Distance.COSINE
                    )
                )

            self._initialized = True
            return True

        except Exception as e:
            print(f"Failed to initialize vector store: {e}")
            return False

    def index_repository(self, repo_path: str) -> int:
        """
        Index all code files in a repository.

        Args:
            repo_path: Path to the repository

        Returns:
            Number of chunks indexed
        """
        if not self._initialized:
            if not self.initialize():
                return 0

        repo_path = Path(repo_path)
        chunks = []

        for filepath in repo_path.rglob('*'):
            if not filepath.is_file():
                continue

            # Skip non-code files
            if filepath.suffix not in self.CODE_EXTENSIONS:
                continue

            # Skip hidden/vendor directories
            path_str = str(filepath)
            if any(skip in path_str for skip in ['.git', 'node_modules', '__pycache__', 'venv', '.venv']):
                continue

            try:
                content = filepath.read_text(encoding='utf-8', errors='ignore')
                relative_path = str(filepath.relative_to(repo_path))
                language = self.CODE_EXTENSIONS.get(filepath.suffix, 'text')

                file_chunks = self._chunk_file(content, relative_path, language)
                chunks.extend(file_chunks)

            except Exception:
                pass

        # Store chunks in Qdrant
        if chunks:
            points = []
            for chunk in chunks:
                vector = self._simple_hash_vector(chunk.content)
                points.append(PointStruct(
                    id=abs(hash(chunk.id)) % (2**63),  # Ensure positive int64
                    vector=vector,
                    payload={
                        "content": chunk.content,
                        "filepath": chunk.filepath,
                        "start_line": chunk.start_line,
                        "end_line": chunk.end_line,
                        "language": chunk.language,
                        "function_name": chunk.function_name,
                        "class_name": chunk.class_name
                    }
                ))

            self.client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=points
            )

        return len(chunks)

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant code chunks.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching code chunks with scores
        """
        if not self._initialized:
            return []

        try:
            query_vector = self._simple_hash_vector(query)

            results = self.client.search(
                collection_name=self.COLLECTION_NAME,
                query_vector=query_vector,
                limit=limit
            )

            return [
                {
                    "score": hit.score,
                    "content": hit.payload.get("content", ""),
                    "filepath": hit.payload.get("filepath", ""),
                    "start_line": hit.payload.get("start_line", 0),
                    "end_line": hit.payload.get("end_line", 0),
                    "language": hit.payload.get("language", ""),
                }
                for hit in results
            ]

        except Exception:
            return []

    def _chunk_file(self, content: str, filepath: str, language: str) -> List[CodeChunk]:
        """Split file content into chunks."""
        chunks = []
        lines = content.split('\n')

        current_chunk = []
        current_start = 1
        current_size = 0

        for i, line in enumerate(lines, 1):
            current_chunk.append(line)
            current_size += len(line)

            if current_size >= self.CHUNK_SIZE:
                chunk_content = '\n'.join(current_chunk)
                chunk_id = hashlib.md5(f"{filepath}:{current_start}:{i}".encode()).hexdigest()

                chunks.append(CodeChunk(
                    id=chunk_id,
                    content=chunk_content,
                    filepath=filepath,
                    start_line=current_start,
                    end_line=i,
                    language=language
                ))

                # Overlap: keep last few lines
                overlap_lines = current_chunk[-3:] if len(current_chunk) > 3 else []
                current_chunk = overlap_lines
                current_start = max(1, i - len(overlap_lines) + 1)
                current_size = sum(len(l) for l in current_chunk)

        # Handle remaining content
        if current_chunk:
            chunk_content = '\n'.join(current_chunk)
            chunk_id = hashlib.md5(f"{filepath}:{current_start}:{len(lines)}".encode()).hexdigest()

            chunks.append(CodeChunk(
                id=chunk_id,
                content=chunk_content,
                filepath=filepath,
                start_line=current_start,
                end_line=len(lines),
                language=language
            ))

        return chunks

    def _simple_hash_vector(self, text: str, dim: int = 384) -> List[float]:
        """
        Create a simple hash-based vector for text.
        Note: For production, use proper embeddings (e.g., sentence-transformers).
        """
        # Simple character-based hashing
        vector = [0.0] * dim
        text_bytes = text.encode('utf-8')

        for i, byte in enumerate(text_bytes):
            idx = (i + byte) % dim
            vector[idx] += (byte / 255.0 - 0.5) * 0.1

        # Normalize
        magnitude = sum(v * v for v in vector) ** 0.5
        if magnitude > 0:
            vector = [v / magnitude for v in vector]

        return vector

    def clear(self):
        """Clear all indexed data."""
        if self._initialized and self.client:
            try:
                self.client.delete_collection(self.COLLECTION_NAME)
                self._initialized = False
            except Exception:
                pass
