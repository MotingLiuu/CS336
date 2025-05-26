from typing import Optional, List, Dict
from utils import find_chunk_boundaries
from collections import defaultdict

class BPETokenizer:
    def __init__(self, vocab_size: int, special_tokens: Optional[List[str]] = None):
        self.vocab_size = vocab_size
        self.special_tokens = special_tokens if special_tokens else []
        self.vocab = {}
        self.merges = []
    
    def train(self, input_path: str):
        pass
        
    def parallel_pretokenize(self, input_path: str) -> Dict[str, int]:
        token_counts = defaultdict(int)
        with open(input_path, 'rb') as f:
            boundaries = find_chunk_boundaries(
                f, 1, "<|endoftext|>".encode("utf-8")
            )
            for start, end in zip(boundaries[:-1], boundaries[1:]):
                f.seek(start)
                chunk = f.read(end - start).decode("utf-8", errors="ignore")
        return token_counts
    
    def pretokenize(self, input_path: str) -> Dict[str, int]:
        with open(input_path, 'rb') as f:
            chunk = f.read().decode("utf-8", errors='ignore')
            