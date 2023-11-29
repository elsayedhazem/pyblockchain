import sys
import hashlib
from block import Block
from typing import Any
import time

class PoWBlockProvider:
	def __init__(self, start=0, difficulty=3):
		self.start = start
		self.difficulty = difficulty

	def genesis(self) -> Block:
		return self.new_block(
			previous_hash="0",
			data=["Genesis block."],
			id=0,
		)

	def _validate_hash(self, hash_attempt: str):
		return hash_attempt.startswith('0' * self.difficulty)

	def _calc_hash(self, nonce: int, previous_hash: str, id: int, data: Any, timestamp: float) -> str:	
		# concatenate the nonce, previous hash, id, data, and timestamp
		concatenated = previous_hash + str(data) + str(nonce) + str(id) + str(timestamp)

		# use sha256 hash function
		hashed = hashlib.sha256(concatenated.encode("utf-8"))
		return hashed.hexdigest()
	
	def new_block(self, previous_hash: str, data: Any, id: int) -> Block:
		timestamp = time.time()

		for i in range(self.start, sys.maxsize):
			hash_attempt = self._calc_hash(
				nonce=i,
				previous_hash=previous_hash,
				id=id,
				data=data,
				timestamp=timestamp,
			)

			if self._validate_hash(hash_attempt):
				return Block(
					previous_hash=previous_hash,
					nonce=i,
					id=id,
					timestamp=timestamp,
					data=data,
					hash=hash_attempt,
				)
		
		raise Exception("Could not find a nonce in the given range.")