import json
from block import Block

class InvalidChain(Exception):
	"""Exception raised when a chain is invalid."""
	pass


class Blockchain:
	def __init__(self, file=None, blocks=None):
		"""
		Initialize a new blockchain with a genesis block.
		Iterating over the Blockchain object returns blocks in reverse order.
		"""

		self._blocks = []
		self.count = 0
		self.file = file or None

		if blocks:
			_ = [self._blocks.append(block) for block in blocks]
			self.count = len(blocks)
			return None

		if self.file:
			with open(file, 'r') as f:
				self._blocks = [Block.from_dict(block) for block in json.load(f)]
				self.count = len(self._blocks)

		
	def add_block(self, block):
		"""Add a new block to the blockchain."""
		self._blocks.append(block)
		self.count += 1

	def as_dict_list(self, reverse=False):
		if reverse:
			return [block.__dict__ for block in self._blocks[::-1]]	
		
		return [block.__dict__ for block in self._blocks]


	def blocks(self, reverse=False):
		if reverse:
			return self._blocks[::-1]
		return self._blocks

	def dump(self):
		"""Dump the blockchain in json file."""
		if not self.file:
			return

		with open(self.file, 'w') as f:
			json.dump(self.as_dict_list(), f, indent=2)

	@staticmethod
	def validate_chain(chain, difficulty) -> bool:
		"""
		Validates the given blockchain. Uses difficulty to verify proof of Work.
		"""
		for block, previous_block in zip(chain.blocks(reverse=True), chain.blocks(reverse=True)[1:]):
			if not Block.validate_hash(block):
				raise InvalidChain(f"Block {block.id} has invalid hash.")
			
			if not block.hash.startswith('0' * difficulty):
				raise InvalidChain(f"Block {block.id} has invalid proof of work.")

			if len(chain) == 1:
				return True

			if block.previous_hash != previous_block.hash:
				raise InvalidChain(f"Block {block.id} has invalid previous hash.")
		return True

	@property
	def last_block(self):
		if len(self._blocks) < 1:
			return None
		return self._blocks[-1]

	def __len__(self):
		return len(self._blocks)