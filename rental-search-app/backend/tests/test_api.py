from pathlib import Path

from fastapi.testclient import TestClient

from app.database import DB_PATH, init_db
from app.main import app


def setup_function() -> None:
    if Path(DB_PATH).exists():
        Path(DB_PATH).unlink()
    init_db()


client = TestClient(app)


def test_list_properties_filters_by_rent() -> None:
    response = client.get("/api/properties", params={"max_rent": 100000})

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 1
    assert all(item["rent_yen"] <= 100000 for item in data)


def test_list_properties_returns_100_seeded_items() -> None:
    response = client.get("/api/properties")

    assert response.status_code == 200
    assert len(response.json()) == 100


def test_seeded_properties_use_local_property_images() -> None:
    response = client.get("/api/properties")

    assert response.status_code == 200
    image_urls = {item["image_url"] for item in response.json()}
    assert image_urls == {
        f"/property-images/property-images-{image_number}.png"
        for image_number in range(1, 11)
    }


def test_property_images_are_assigned_by_property_id() -> None:
    first_response = client.get("/api/properties/1")
    tenth_response = client.get("/api/properties/10")
    eleventh_response = client.get("/api/properties/11")

    assert first_response.status_code == 200
    assert tenth_response.status_code == 200
    assert eleventh_response.status_code == 200
    assert first_response.json()["image_url"] == "/property-images/property-images-1.png"
    assert tenth_response.json()["image_url"] == "/property-images/property-images-10.png"
    assert eleventh_response.json()["image_url"] == "/property-images/property-images-1.png"


def test_seed_data_hits_common_filter_conditions() -> None:
    filter_cases = [
        {"max_rent": 90000},
        {"max_rent": 140000},
        {"layout": "1R"},
        {"layout": "1LDK"},
        {"layout": "2LDK"},
        {"max_walk_minutes": 5},
        {"max_walk_minutes": 10},
        {"station": "中野駅"},
        {"station": "豊洲駅"},
    ]

    for params in filter_cases:
        response = client.get("/api/properties", params=params)

        assert response.status_code == 200
        assert len(response.json()) > 0, params


def test_get_property_detail() -> None:
    response = client.get("/api/properties/1")

    assert response.status_code == 200
    assert response.json()["station"] == "中野駅"


def test_create_inquiry() -> None:
    response = client.post(
        "/api/inquiries",
        json={
            "property_id": 1,
            "name": "山田 太郎",
            "email": "taro@example.com",
            "phone": "090-0000-0000",
            "message": "週末に詳細を確認したいです。",
        },
        headers={"X-Demo-User-Id": "user-a"},
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == "user-a"


def test_get_inquiry_detail_by_id() -> None:
    created = client.post(
        "/api/inquiries",
        json={
            "property_id": 1,
            "name": "山田 太郎",
            "email": "taro@example.com",
            "phone": "090-0000-0000",
            "message": "個人情報を含む問い合わせです。",
        },
        headers={"X-Demo-User-Id": "user-a"},
    )
    inquiry_id = created.json()["id"]

    response = client.get(f"/api/inquiries/{inquiry_id}", headers={"X-Demo-User-Id": "user-b"})

    assert response.status_code == 200
    assert response.json()["email"] == "taro@example.com"
