from dataclasses import dataclass, field

@dataclass(slots=True)
class Chunk:
    chunk_id: str
    text: str
    metadata: dict = field(default_factory=dict)