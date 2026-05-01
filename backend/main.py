from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import time

from blockchain import Blockchain, Block
from detector import is_suspicious
from database import init_db, save_block, load_all_blocks, clear_db

# ── App setup ────────────────────────────────────────────────────
app = FastAPI(
    title="Public Fund Tracker API",
    description="Blockchain-based transparent government fund tracker",
    version="1.0.0"
)

# Allow React (port 3000) to talk to this backend (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Admin key for protected routes (change this in production!)
ADMIN_KEY = "hackathon-admin-2025"

# ── Initialize blockchain and database ───────────────────────────
init_db()
blockchain = Blockchain()

# Load saved blocks from DB into the blockchain on startup
saved_blocks = load_all_blocks()
if saved_blocks:
    # Re-hydrate the blockchain from database
    blockchain.chain = []
    for row in saved_blocks:
        block = Block(
            index=row["idx"],
            sender=row["sender"],
            receiver=row["receiver"],
            amount=row["amount"],
            category=row["category"],
            previous_hash=row["prev_hash"]
        )
        block.hash = row["hash"]
        block.timestamp = row["timestamp"]
        blockchain.chain.append(block)
    print(f"Loaded {len(saved_blocks)} blocks from database.")
else:
    # Save genesis block to DB
    save_block({**blockchain.chain[0].to_dict(), "index": 0})
    print("Started fresh chain with genesis block.")


# ── Request / Response Models ─────────────────────────────────────
class TransactionRequest(BaseModel):
    sender: str = Field(..., min_length=1, description="Who is sending the funds")
    receiver: str = Field(..., min_length=1, description="Who is receiving the funds")
    amount: float = Field(..., gt=0, description="Amount in INR")
    category: Optional[str] = Field("General", description="Type of expenditure")


# ── Helper: get transaction history for anomaly detection ─────────
def get_amount_history() -> list:
    chain = blockchain.get_chain()
    return [b["amount"] for b in chain if b["index"] != 0]  # skip genesis


# ── Routes ────────────────────────────────────────────────────────

@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "project": "Public Fund Tracker",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/transaction")
def add_transaction(
    tx: TransactionRequest,
    x_api_key: Optional[str] = Header(None)
):
    """
    Add a new transaction to the blockchain.
    Requires admin API key header: X-Api-Key: hackathon-admin-2025
    """
    if x_api_key != ADMIN_KEY:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Admin API key required. Pass header: X-Api-Key"
        )

    # Add to blockchain
    new_block = blockchain.add_block(
        sender=tx.sender,
        receiver=tx.receiver,
        amount=tx.amount,
        category=tx.category
    )

    # Run suspicious detection
    history = get_amount_history()
    detection = is_suspicious(tx.amount, history, tx.sender)

    # Save to database
    save_block(new_block)

    return {
        "success": True,
        "message": "Transaction added to blockchain",
        "block": new_block,
        "suspicious_analysis": detection
    }


@app.get("/chain")
def get_chain():
    """
    Get the full blockchain with suspicious flags on each block.
    Public endpoint — no auth required.
    """
    chain = blockchain.get_chain()
    history = get_amount_history()

    # Annotate each block with suspicious analysis
    annotated = []
    for block in chain:
        if block["index"] == 0:
            block["suspicious_analysis"] = {"flagged": False, "reasons": [], "risk_level": "low"}
        else:
            block["suspicious_analysis"] = is_suspicious(
                block["amount"],
                [b["amount"] for b in chain[:block["index"]] if b["index"] != 0],
                block["sender"]
            )
        annotated.append(block)

    return {
        "chain": annotated,
        "length": len(chain)
    }


@app.get("/verify")
def verify_chain():
    """
    Verify the entire blockchain's integrity.
    Public endpoint — anyone can verify the chain.
    """
    result = blockchain.verify_integrity()
    return result


@app.get("/stats")
def get_stats():
    """
    Analytics: summary statistics of all transactions.
    """
    return blockchain.get_stats()


@app.get("/search")
def search_transactions(q: str = "", category: str = ""):
    """
    Search transactions by sender, receiver, or category.
    Example: /search?q=health or /search?category=Roads
    """
    chain = blockchain.get_chain()[1:]  # skip genesis

    results = []
    for block in chain:
        q_lower = q.lower()
        matches_q = (
            q_lower in block["sender"].lower() or
            q_lower in block["receiver"].lower() or
            q_lower == str(int(block["amount"]))
        ) if q else True

        matches_cat = (
            category.lower() in block["category"].lower()
        ) if category else True

        if matches_q and matches_cat:
            results.append(block)

    return {
        "results": results,
        "count": len(results),
        "query": q,
        "category_filter": category
    }


@app.delete("/reset")
def reset_chain(x_api_key: Optional[str] = Header(None)):
    """
    DANGER: Wipes the entire chain and starts fresh.
    Admin only — use only for demos/testing.
    """
    if x_api_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Admin access required")

    global blockchain
    clear_db()
    blockchain = Blockchain()
    save_block({**blockchain.chain[0].to_dict(), "index": 0})

    return {"success": True, "message": "Chain reset. Genesis block created."}


