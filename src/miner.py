from chain import Blockchain
from block import Block
from pow import PoWBlockProvider


class Miner():
	def __init__(self, wallet_id):
		self.wallet_id = wallet_id

	def mine(self, transaction_pool, blockchain, difficulty):
		# get first 5 transactions or less
		transactions = []
		if len(transaction_pool) < 5:
			if len(transaction_pool) == 0:
				return
			transactions = transaction_pool
		else:
			transactions = {
				k:v for k,v in list(transaction_pool.items())[:5]
			}

		# get previous hash
		previous_hash = blockchain.last_block.hash
		new = self._new_block(previous_hash, transactions, len(blockchain), difficulty)
		blockchain.add_block(new)

	def _new_block(self, previous_hash, data, id, difficulty):
		"""Create a new block."""
		provider = PoWBlockProvider(difficulty=difficulty)
		return provider.new_block(
			previous_hash=previous_hash,
			data=data,
			id=id,
		)

	def genesis(self, difficulty):
		"""Create genesis block."""
		provider = PoWBlockProvider(difficulty=difficulty)
		return provider.genesis()

