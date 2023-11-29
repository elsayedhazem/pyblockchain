# setup fastapi app

from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
from typing import List, Any
import json

from chain import Blockchain, InvalidChain
from block import Block

app = FastAPI()

### JSON Request Models ###

class BlockModel(BaseModel):
	id: int
	previous_hash: str
	nonce: int
	timestamp: float
	data: Any
	hash: str

class ChainModel(BaseModel):
	chain: List[BlockModel]

class TransactionsModel(BaseModel):
	transactions: dict


### API ### 

SETTINGS = {
	"difficulty": 5, ### Represents the network difficulty for PoW
}


@app.get("/chain", response_model=ChainModel)
async def get_chain():
	chain = Blockchain(file="chain.json")
	return {
		"chain": [block.__dict__ for block in chain.blocks()]
	}

@app.post("/chain")
async def write_chain(chain: ChainModel):
	
	blocks = [Block.from_dict(block.dict()) for block in chain.chain]
	chain = Blockchain(file="chain.json", blocks=blocks)
	try:
		Blockchain.validate_chain(chain, difficulty=SETTINGS["difficulty"])
	except InvalidChain as e:
		raise HTTPException(status_code=400, detail=str(e))
	
	processed_transactions = chain.last_block.data
	pool = dict()
	with open("transactions.json", 'r') as f:
		pool = json.load(f)

	for key in list(processed_transactions.keys()):
		if key in pool:
			pool.pop(key)
	
	with open("transactions.json", 'w') as f:
		json.dump(pool, f)

	chain.dump()
	return Response(status_code=200, content="Chain saved.")


@app.get("/events", response_model=TransactionsModel)
async def get_transactions():
	transactions = []
	with open("transactions.json", 'r') as f:
		transactions = json.load(f)

	return {
		"transactions": transactions
	}


@app.post("/events")
async def write_transactions(events: TransactionsModel):
	pool = dict()
	with open("transactions.json", 'r') as f:
		pool = json.load(f)

	pool = pool | transactions.transactions
	
	with open("transactions.json", 'w') as f:
		json.dump(pool, f)