from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_connection, init_db
from app.schemas import Inquiry, InquiryCreate, Property


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Rental Search API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def to_property(row) -> Property:
    data = dict(row)
    amenities = data.pop("amenities")
    return Property(
        **data,
        amenities=[item.strip() for item in amenities.split(",") if item.strip()],
    )


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/properties", response_model=list[Property])
def list_properties(
    keyword: str | None = None,
    station: str | None = None,
    max_rent: int | None = Query(default=None, ge=0),
    layout: str | None = None,
    max_walk_minutes: int | None = Query(default=None, ge=0),
) -> list[Property]:
    query = "SELECT * FROM properties WHERE 1 = 1"
    params: list[object] = []
    if keyword:
        query += " AND (title LIKE ? OR building_name LIKE ? OR address LIKE ? OR station LIKE ?)"
        keyword_param = f"%{keyword}%"
        params.extend([keyword_param, keyword_param, keyword_param, keyword_param])
    if station:
        query += " AND station LIKE ?"
        params.append(f"%{station}%")
    if max_rent is not None:
        query += " AND rent_yen <= ?"
        params.append(max_rent)
    if layout:
        query += " AND layout = ?"
        params.append(layout)
    if max_walk_minutes is not None:
        query += " AND walk_minutes <= ?"
        params.append(max_walk_minutes)
    query += " ORDER BY availability DESC, rent_yen ASC"

    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()
    return [to_property(row) for row in rows]


@app.get("/api/properties/{property_id}", response_model=Property)
def get_property(property_id: int) -> Property:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM properties WHERE id = ?", (property_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return to_property(row)


@app.post("/api/inquiries", response_model=Inquiry, status_code=201)
def create_inquiry(
    request: InquiryCreate,
    user_id: Annotated[str, Header(alias="X-Demo-User-Id")] = "demo-user-1",
) -> Inquiry:
    with get_connection() as connection:
        exists = connection.execute(
            "SELECT 1 FROM properties WHERE id = ?", (request.property_id,)
        ).fetchone()
        if exists is None:
            raise HTTPException(status_code=404, detail="Property not found")
        cursor = connection.execute(
            """
            INSERT INTO inquiries (user_id, property_id, name, email, phone, message)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                request.property_id,
                request.name,
                request.email,
                request.phone,
                request.message,
            ),
        )
        row = connection.execute(
            "SELECT * FROM inquiries WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return Inquiry(**dict(row))


@app.get("/api/inquiries/{inquiry_id}", response_model=Inquiry)
def get_inquiry(
    inquiry_id: int,
    user_id: Annotated[str, Header(alias="X-Demo-User-Id")] = "demo-user-1",
) -> Inquiry:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM inquiries WHERE id = ?", (inquiry_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return Inquiry(**dict(row))
