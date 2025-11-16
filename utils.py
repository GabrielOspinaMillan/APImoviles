from fastapi import Header, HTTPException
from typing import Optional

idempotency_cache = set()

def check_idempotency(idempotency_key: Optional[str] = Header(None)):
    if idempotency_key is None:
        return

    if idempotency_key in idempotency_cache:
        raise HTTPException(status_code=409, detail="Duplicate request")

    idempotency_cache.add(idempotency_key)
