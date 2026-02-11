"""
Fixed version of notes.py with security vulnerabilities remediated.

Fixes applied:
1. SQL injection (line 71) - replaced raw SQL with SQLAlchemy ORM
2. Weak crypto MD5 (line 98) - replaced MD5 with SHA-256
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note
from ..schemas import NoteCreate, NotePatch, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteRead])
def list_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[NoteRead]:
    stmt = select(Note)
    if q:
        stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if hasattr(Note, sort_field):
        stmt = stmt.order_by(order_fn(getattr(Note, sort_field)))
    else:
        stmt = stmt.order_by(desc(Note.created_at))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.patch("/{note_id}", response_model=NoteRead)
def patch_note(note_id: int, payload: NotePatch, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


# FIX #1: SQL Injection - replaced raw SQL with SQLAlchemy ORM
@router.get("/search", response_model=list[NoteRead])
def search_notes(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
    """
    Search notes by title or content using SQLAlchemy ORM.

    This prevents SQL injection by using parameterized queries.
    The .contains() method automatically escapes user input.

    Before (VULNERABLE):
        sql = text(f"SELECT * FROM notes WHERE title LIKE '%{q}%'")
        # Allows injection: '; DROP TABLE notes; --

    After (SECURE):
        stmt = select(Note).where(Note.title.contains(q))
        # User input is treated as DATA, not CODE
    """
    # SQLAlchemy ORM automatically uses parameterized queries
    stmt = select(Note).where(
        (Note.title.contains(q)) | (Note.content.contains(q))
    ).order_by(desc(Note.created_at)).limit(50)

    rows = db.execute(stmt).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


# FIX #3: Weak Crypto - replaced MD5 with SHA-256
@router.get("/debug/hash-sha256")
def debug_hash_sha256(q: str) -> dict[str, str]:
    """
    Generate SHA-256 hash for debugging purposes.

    Note: SHA-256 is suitable for:
    - Checksums and file integrity verification
    - Cache key generation
    - Non-password hashing

    For password hashing, use bcrypt, scrypt, or argon2 instead.
    These are intentionally slow to resist brute-force attacks.

    Before (VULNERABLE):
        hashlib.md5(q.encode()).hexdigest()
        # MD5 is cryptographically broken:
        # - Collision attacks are trivial
        # - Can be reversed with rainbow tables
        # - Not suitable for any security purpose

    After (SECURE):
        hashlib.sha256(q.encode()).hexdigest()
        # SHA-256 is secure for non-password use cases
    """
    import hashlib

    return {"algo": "sha256", "hex": hashlib.sha256(q.encode()).hexdigest()}
