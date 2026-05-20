from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "rental.db"
PROPERTY_IMAGE_COUNT = 10


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                building_name TEXT NOT NULL,
                address TEXT NOT NULL,
                station TEXT NOT NULL,
                walk_minutes INTEGER NOT NULL,
                rent_yen INTEGER NOT NULL,
                management_fee_yen INTEGER NOT NULL,
                deposit_months REAL NOT NULL,
                key_money_months REAL NOT NULL,
                layout TEXT NOT NULL,
                area_sqm REAL NOT NULL,
                built_year INTEGER NOT NULL,
                floor TEXT NOT NULL,
                image_url TEXT NOT NULL,
                amenities TEXT NOT NULL,
                availability TEXT NOT NULL,
                description TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                property_id INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, property_id),
                FOREIGN KEY(property_id) REFERENCES properties(id)
            );

            CREATE TABLE IF NOT EXISTS inquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                property_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(property_id) REFERENCES properties(id)
            );
            """
        )
        count = connection.execute("SELECT COUNT(*) FROM properties").fetchone()[0]
        if count == 0:
            seed_properties(connection)
        update_property_images(connection)


def property_image_url(property_id: int) -> str:
    image_number = ((property_id - 1) % PROPERTY_IMAGE_COUNT) + 1
    return f"/property-images/property-images-{image_number}.png"


def update_property_images(connection: sqlite3.Connection) -> None:
    property_ids = connection.execute("SELECT id FROM properties").fetchall()
    connection.executemany(
        "UPDATE properties SET image_url = ? WHERE id = ?",
        [(property_image_url(row["id"]), row["id"]) for row in property_ids],
    )


def seed_properties(connection: sqlite3.Connection) -> None:
    areas = [
        ("中野区", "中野", "中野駅", "中央"),
        ("世田谷区", "桜新町", "桜新町駅", "弦巻"),
        ("豊島区", "大塚", "大塚駅", "南大塚"),
        ("港区", "芝浦", "田町駅", "芝浦"),
        ("品川区", "大井町", "大井町駅", "東大井"),
        ("杉並区", "荻窪", "荻窪駅", "天沼"),
        ("練馬区", "石神井公園", "石神井公園駅", "石神井町"),
        ("目黒区", "学芸大学", "学芸大学駅", "鷹番"),
        ("江東区", "豊洲", "豊洲駅", "豊洲"),
        ("文京区", "茗荷谷", "茗荷谷駅", "小石川"),
    ]
    layouts = [
        ("1R", 24.5, 78000),
        ("1LDK", 42.0, 128000),
        ("2LDK", 59.0, 188000),
    ]
    building_prefixes = [
        "グリーンレジデンス",
        "D-room",
        "アーバンコート",
        "ベイフロント",
        "プライムメゾン",
        "ラフィネ",
        "コンフォリア",
        "ブランシェ",
        "リバーサイド",
        "パークハイム",
    ]
    title_patterns = [
        "駅近・南向き",
        "ペット相談可",
        "敷金礼金ゼロ",
        "在宅勤務向け",
        "ファミリー向け",
        "築浅・設備充実",
        "眺望良好",
        "商店街近く",
        "収納豊富",
        "セキュリティ重視",
    ]
    amenity_sets = [
        "オートロック,宅配ボックス,浴室乾燥機,独立洗面台,インターネット無料",
        "ペット相談,追い焚き,システムキッチン,ウォークインクローゼット,防犯カメラ",
        "敷金礼金ゼロ,エレベーター,温水洗浄便座,モニター付きインターホン",
        "床暖房,ディスポーザー,駐車場相談,コンシェルジュ,24時間ゴミ出し",
        "角部屋,二面採光,カウンターキッチン,室内物干し,駐輪場",
    ]
    walk_minutes = [3, 5, 8, 10, 12, 15, 4, 6, 9, 14]
    rent_adjustments = [-8000, 0, 12000, 26000, 42000, 64000, 88000, 112000, 138000, 164000]
    management_fees = [5000, 6000, 7000, 8000, 9000, 10000, 12000, 13000, 15000, 18000]

    rows = []
    property_id = 1
    for area_index, (ward, area_name, station, town) in enumerate(areas):
        for item_index in range(10):
            layout, base_area, base_rent = layouts[(area_index + item_index) % len(layouts)]
            floor_number = (item_index % 9) + 1
            total_floors = floor_number + 4 + (area_index % 5)
            built_year = 2008 + ((area_index * 3 + item_index) % 17)
            rent_yen = base_rent + rent_adjustments[item_index] + area_index * 3500
            management_fee_yen = management_fees[(area_index + item_index) % len(management_fees)]
            area_sqm = round(base_area + item_index * 1.6 + area_index * 0.7, 1)
            walk = walk_minutes[item_index]
            prefix = building_prefixes[(area_index + item_index) % len(building_prefixes)]
            title = f"{title_patterns[(area_index + item_index) % len(title_patterns)]}の{layout}"
            building_name = f"{prefix}{area_name}{item_index + 1:02d}"
            availability = "申込あり" if (area_index * 10 + item_index) % 7 == 0 else "募集中"
            deposit_months = [0.0, 1.0, 2.0][(area_index + item_index) % 3]
            key_money_months = [0.0, 0.5, 1.0][(area_index * 2 + item_index) % 3]

            rows.append(
                (
                    property_id,
                    title,
                    building_name,
                    f"東京都{ward}{town}{item_index + 1}-{area_index + 2}-{floor_number}",
                    station,
                    walk,
                    rent_yen,
                    management_fee_yen,
                    deposit_months,
                    key_money_months,
                    layout,
                    area_sqm,
                    built_year,
                    f"{floor_number}階/{total_floors}階建",
                    property_image_url(property_id),
                    amenity_sets[(area_index + item_index) % len(amenity_sets)],
                    availability,
                    f"{station}徒歩{walk}分。{area_name}エリアで{layout}を探す方向けの賃貸物件です。",
                )
            )
            property_id += 1

    connection.executemany(
        """
        INSERT INTO properties (
            id, title, building_name, address, station, walk_minutes, rent_yen,
            management_fee_yen, deposit_months, key_money_months, layout,
            area_sqm, built_year, floor, image_url, amenities, availability,
            description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
