# Offline AI-Driven ERP — Local API Starter

A minimal FastAPI service that stores project work-progress records in local JSON files. It is intentionally cloud-independent and provides a foundation for the PySide6 desktop client discussed earlier.

## Run
`python -m pip install fastapi uvicorn`
`uvicorn app:app --host 127.0.0.1 --port 8765`
Open http://127.0.0.1:8765/docs.

## Scope and security
This is not the complete ERP desktop application. It does not yet implement authentication, role-based access control, audit trails, document OCR, procurement, finance, backups or concurrency-safe database transactions. Do not expose it to a network or store confidential institutional data until those controls are implemented. JSON is suitable only for a small single-user prototype.
