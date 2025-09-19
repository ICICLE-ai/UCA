import os
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

import requests
import jwt
from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.database.rules_engine.rules_engine_client import RuleEngineClient
from src.database.rules_engine.exceptions import RuleValidationError, RuleNotFoundError
from src.database.rules_engine.config import Config

app = FastAPI(title="Rules API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = RuleEngineClient(
    tapis_url=Config.TAPIS_URL,
    tapis_user=getattr(Config, "TAPIS_USER", None),
    tapis_pass=getattr(Config, "TAPIS_PASS", None),
    mongo_uri=Config.MONGO_URI,
    db_name=getattr(Config, "RULES_DB", "IMT_Rules_engine_database"),
)

# ---------- Models ----------
class RuleCreate(BaseModel):
    CI: str
    Type: str 
    Services: List[str]
    Data_Rules: List[Dict[str, Any]]
    Active_To: Optional[str] = None

class RuleUpdate(BaseModel):
    updates: Dict[str, Any]


# ---------- Auth: ONLY Tapis endpoints ----------
def _issuer_base_v3(iss: str) -> str:
    """
    Access tokens often have iss like:
      https://<tenant>.tapis.io/v3/tokens
    OAuth endpoints live under:
      https://<tenant>.tapis.io/v3/oauth2/...
    Tokens utility endpoints live under:
      https://<tenant>.tapis.io/v3/tokens/...
    """
    parts = iss.rstrip("/").split("/v3/")
    return parts[0] + "/v3" if len(parts) >= 2 else iss.rstrip("/")

def _userinfo(token: str, iss: str):
    """Try userinfo with both header styles."""
    base = _issuer_base_v3(iss or Config.TAPIS_URL)
    url = f"{base}/oauth2/userinfo"
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=8)
    if r.ok:
        return r
    r2 = requests.get(url, headers={"X-Tapis-Token": token}, timeout=8)
    return r2

def _tokens_validate(token: str, iss: str):
    """
    Some tenants expose tokens/validate; others may not.
    Try JSON body first, then header style.
    """
    base = _issuer_base_v3(iss or Config.TAPIS_URL)
    url = f"{base}/tokens/validate"
    r = requests.post(url, json={"token": token}, timeout=8)
    if r.ok:
        return r
    r2 = requests.post(url, headers={"X-Tapis-Token": token}, timeout=8)
    return r2

def claims_from_request(
    Authorization: Optional[str] = Header(None, alias="Authorization"),
    tapis_token: Optional[str] = Query(default=None),
) -> dict:
    """
    Validate the presented token *with Tapis only* on every request.
    1) Extract token (Authorization: Bearer … or ?tapis_token=)
    2) Quick local 'exp' check to fail fast on obviously stale tokens
    3) Call Tapis /oauth2/userinfo; if not OK, fallback to /tokens/validate
    """
    token = None
    if Authorization and Authorization.startswith("Bearer "):
        token = Authorization.split(" ", 1)[1]
    elif tapis_token:
        token = tapis_token
    if not token:
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    try:
        unv = jwt.decode(token, options={"verify_signature": False, "verify_aud": False})
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")

    exp = unv.get("exp")
    if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(tz=timezone.utc):
        raise HTTPException(status_code=401, detail="expired token")

    iss = (unv.get("iss") or Config.TAPIS_URL).rstrip("/")

    try:
        u = _userinfo(token, iss)
        if u.ok:
            j = u.json()
            return {
                "sub": j.get("sub") or unv.get("sub"),
                "tapis/username": j.get("username")
                    or j.get("tapis/username")
                    or unv.get("tapis/username"),
            }
        u_status, u_text = u.status_code, u.text[:200]
    except Exception:
        u_status, u_text = "ERR", ""

    try:
        v = _tokens_validate(token, iss)
        if v.ok:
            if v.headers.get("content-type", "").startswith("application/"):
                data = v.json()
                if isinstance(data, dict) and (data.get("valid") is True or data.get("sub")):
                    return {
                        "sub": data.get("sub") or unv.get("sub"),
                        "tapis/username": data.get("username")
                            or data.get("tapis/username")
                            or unv.get("tapis/username"),
                    }
            return {
                "sub": unv.get("sub"),
                "tapis/username": unv.get("tapis/username"),
            }

        raise HTTPException(status_code=401, detail=f"tokens/validate {v.status_code}: {v.text[:200]}")
    except HTTPException:
        raise
    except Exception:
        pass

    raise HTTPException(status_code=401, detail=f"userinfo {u_status}: {u_text}")


# ---------- Routes ----------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/rules")
def create_rule(rule: RuleCreate, claims=Depends(claims_from_request)):
    try:
        rule_uuid = client.create_rule(rule.model_dump(), claims=claims)
        return {"Rule_UUID": rule_uuid}
    except RuleValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/rules")
def list_rules(claims=Depends(claims_from_request)):
    items = client.list_rules({}, claims=claims)
    return {"items": [getattr(x, "__dict__", x) for x in items]}

@app.get("/rules/{rule_uuid}")
def get_rule(rule_uuid: str, claims=Depends(claims_from_request)):
    try:
        r = client.get_rule(rule_uuid, claims=claims)
        return getattr(r, "__dict__", r)
    except RuleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.patch("/rules/{rule_uuid}")
def update_rule(rule_uuid: str, payload: RuleUpdate, claims=Depends(claims_from_request)):
    try:
        client.update_rule(rule_uuid, payload.updates, claims=claims)
        return {"ok": True}
    except RuleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/rules/{rule_uuid}")
def delete_rule(rule_uuid: str, claims=Depends(claims_from_request)):
    try:
        client.delete_rule(rule_uuid, claims=claims)
        return {"ok": True}
    except RuleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))