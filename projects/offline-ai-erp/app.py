"""Local-first ERP API starter. Stores records in JSON; no cloud service required."""
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DATA=Path("data"); DATA.mkdir(exist_ok=True)
DB=DATA/"work_records.json"
app=FastAPI(title="Offline AI ERP API",version="0.1.0")
class WorkRecord(BaseModel):
    employee: str = Field(min_length=1,max_length=100)
    project: str = Field(min_length=1,max_length=150)
    description: str = Field(min_length=1,max_length=2000)
    progress: int = Field(ge=0,le=100)
def read_all():
    if not DB.exists(): return []
    try: return json.loads(DB.read_text(encoding="utf-8"))
    except json.JSONDecodeError: raise HTTPException(500,"Local data file is invalid JSON")
def write_all(rows):
    tmp=DB.with_suffix(".tmp"); tmp.write_text(json.dumps(rows,indent=2),encoding="utf-8"); tmp.replace(DB)
@app.get("/health")
def health(): return {"status":"ok","storage":"local-json"}
@app.get("/records")
def list_records(): return read_all()
@app.post("/records",status_code=201)
def add_record(record:WorkRecord):
    rows=read_all(); item=record.model_dump()
    item.update(id=str(uuid4()),created_at=datetime.now(timezone.utc).isoformat())
    rows.append(item); write_all(rows); return item
@app.get("/records/{record_id}")
def get_record(record_id:str):
    for item in read_all():
        if item["id"]==record_id: return item
    raise HTTPException(404,"Record not found")
