from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from blockchain import Blockchain
from fraud_detection import analyze_risk
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from database import users_db
from models import UserRegister, UserLogin, TransactionCreate, Token

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

public_ledger = Blockchain()

# --- AUTO SETUP USERS ---
def bootstrap_users():
    default_users = [
        ("admin", "admin123", "admin"),
        ("auditor", "auditor123", "auditor"),
        ("public", "public123", "public"),
    ]
    for uname, pwd, role in default_users:
        if uname not in users_db:
            users_db[uname] = {"username": uname, "password": get_password_hash(pwd), "role": role}
    print("✅ System Bootstrap: Default users created.")

bootstrap_users()

# --- ROLE CHECKER ---
def role_required(allowed):
    def checker(user=Depends(get_current_user)):
        if user["role"] not in allowed:
            raise HTTPException(status_code=403, detail="Permission Denied")
        return user
    return checker

@app.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user = users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Wrong credentials")
    token = create_access_token({"sub": db_user["username"], "role": db_user["role"]})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/transactions")
async def get_txs(user=Depends(get_current_user)):
    return [b.__dict__ for b in public_ledger.chain]

@app.post("/transaction")
async def add_tx(tx: TransactionCreate, user=Depends(role_required(["admin"]))):
    risk = analyze_risk(tx.amount, public_ledger.chain)
    new_block = public_ledger.add_block(tx.sender, tx.receiver, tx.amount, risk)
    return new_block.__dict__

@app.get("/validate")
async def validate(user=Depends(get_current_user)):
    valid = public_ledger.is_chain_valid()
    return {"status": "VALID" if valid else "TAMPERED", "isValid": valid}

@app.post("/tamper/{index}")
async def tamper(index: int, amount: float, user=Depends(role_required(["admin"]))):
    if public_ledger.tamper_block(index, amount):
        return {"message": "Tampered successfully"}
    raise HTTPException(status_code=404)

@app.get("/suspicious")
async def get_susp(user=Depends(role_required(["admin", "auditor"]))):
    return [b.__dict__ for b in public_ledger.chain if b.risk_level != "LOW"]

@app.get("/report")
async def report(user=Depends(role_required(["admin", "auditor"]))):
    high = len([b for b in public_ledger.chain if b.risk_level == "HIGH"])
    med = len([b for b in public_ledger.chain if b.risk_level == "MEDIUM"])
    return {"total": len(public_ledger.chain)-1, "high": high, "med": med, "summary": f"Audit: {high+med} issues found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
