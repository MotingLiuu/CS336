from typing import Optional, List, Dict
from utils import find_chunk_boundaries
from collections import defaultdict, Counter
import regex as re
import os

class BPETokenizer:
    def __init__(self, vocab_size: int, special_tokens: Optional[List[str]] = None):
        self.vocab_size = vocab_size
        self.special_tokens = special_tokens if special_tokens else []
        self.vocab = {}
        self.merges = []
        self.PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    
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
                token_counts.update(Counter([re_match.group() for re_match in re.finditer(self.PAT, chunk)]))
        return token_counts
    
    def pretokenize(self, input_path: str) -> Dict[str, int]:
        token_counts = defaultdict(int)
        with open(input_path, 'rb') as f:
            chunk = f.read().decode("utf-8", errors='ignore')
            chunks = re.split(r'<|endoftext|>', chunk)
            for chunk in chunks:
                tokens = [re_match.group() for re_match in re.finditer(self.PAT, chunk)]
                counts = Counter(tokens)
                token_counts.update(counts)
        return token_counts
                
if __name__ == '__main__':
    BPE = BPETokenizer(30, [r'<|endoftext|>'])
    DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/TinyStoriesV2-GPT4-valid.txt')
    DATA_PATH = os.path.abspath(DATA_PATH)
    token_counts = BPE.pretokenize(DATA_PATH)
    print(token_counts)