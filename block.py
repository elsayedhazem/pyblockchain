from datetime import datetime
import time

from dataclasses import dataclass
from typing import Any
import hashlib

@dataclass(frozen=True)
class Block:
	"""Block class for blockchain. Blocks are generated by PoWBlockProvider."""

	previous_hash: str
	nonce: int
	id: int
	timestamp: float

	# Body fields
	data: Any
	hash: str

	def __repr__(self):
		return f"Block number {self.id}:\nHeader:\n{self.header}\nData:\n{self.data}\nHash:\n{self.hash})"

	def __str__(self):
		return f"Block number {self.id}:\nHeader:\n{self.header}\nData:\n{self.data}\nHash:\n{self.hash})"
	
	@property
	def header(self):
		return {
			"previous_hash": self.previous_hash,
			"nonce": self.nonce,
			"id": self.id,
			"timestamp": self.timestamp,
		}

	@staticmethod
	def validate_hash(block):
		"""Validate header of block."""
		concatenated = block.previous_hash + str(block.data) + str(block.nonce) + str(block.id) + str(block.timestamp)

		# use sha256 hash function
		hashed = hashlib.sha256(concatenated.encode("utf-8")).hexdigest()
		return hashed == block.hash

	@classmethod
	def from_dict(cls, block_dict):
		return cls(
			previous_hash=block_dict["previous_hash"],
			nonce=block_dict["nonce"],
			id=block_dict["id"],
			timestamp=block_dict["timestamp"],
			data=block_dict["data"],
			hash=block_dict["hash"],
		)