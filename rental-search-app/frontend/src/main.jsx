import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Building2, Mail, Search, TrainFront } from 'lucide-react';
import './styles.css';

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';
const DEMO_USER_ID = 'demo-user-1';
const STATIONS = [
  '中野駅',
  '桜新町駅',
  '大塚駅',
  '田町駅',
  '大井町駅',
  '荻窪駅',
  '石神井公園駅',
  '学芸大学駅',
  '豊洲駅',
  '茗荷谷駅',
];

function fieldNameFromLocation(location = []) {
  return location[location.length - 1];
}

function validationMessageFor(detail) {
  if (!Array.isArray(detail)) {
    if (detail === 'Property not found') {
      return '選択中の物件が見つかりません。再度検索して選び直してください。';
    }
    if (detail === 'Inquiry not found') {
      return '問い合わせ情報が見つかりません。';
    }
    return detail || '入力内容を確認してください。';
  }

  const fields = new Set(detail.map((item) => fieldNameFromLocation(item.loc)));
  if (fields.has('email')) return 'メールアドレスの形式を確認してください。';
  if (fields.has('phone')) return '電話番号は8文字以上で入力してください。';
  if (fields.has('name')) return '氏名を入力してください。';
  if (fields.has('message')) return '問い合わせ内容を入力してください。';
  if (fields.has('property_id')) return '選択中の物件が見つかりません。再度検索して選び直してください。';
  return '入力内容を確認してください。';
}

async function api(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-Demo-User-Id': DEMO_USER_ID,
      ...(options.headers ?? {}),
    },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(validationMessageFor(body.detail));
  }
  return response.json();
}

function yen(value) {
  return `${(value / 10000).toFixed(value % 10000 === 0 ? 0 : 1)}万円`;
}

function App() {
  const [filters, setFilters] = useState({
    keyword: '',
    station: '',
    max_rent: '',
    layout: '',
    max_walk_minutes: '',
  });
  const [properties, setProperties] = useState([]);
  const [selected, setSelected] = useState(null);
  const [inquiry, setInquiry] = useState({ name: '', email: '', phone: '', message: '' });
  const [notice, setNotice] = useState('');
  const [error, setError] = useState('');

  async function loadProperties(nextFilters = filters) {
    const params = new URLSearchParams();
    Object.entries(nextFilters).forEach(([key, value]) => {
      if (value) params.set(key, value);
    });
    const data = await api(`/api/properties?${params.toString()}`);
    setProperties(data);
    if (!selected && data.length > 0) setSelected(data[0]);
  }

  useEffect(() => {
    loadProperties().catch((err) => setError(err.message));
  }, []);

  function updateFilter(key, value) {
    setFilters((current) => ({ ...current, [key]: value }));
  }

  async function submitSearch(event) {
    event.preventDefault();
    setError('');
    await loadProperties(filters).catch((err) => setError(err.message));
  }

  async function chooseProperty(propertyId) {
    setError('');
    const detail = await api(`/api/properties/${propertyId}`).catch((err) => setError(err.message));
    if (detail) setSelected(detail);
  }

  async function submitInquiry(event) {
    event.preventDefault();
    if (!selected) return;
    setError('');
    setNotice('');
    const created = await api('/api/inquiries', {
      method: 'POST',
      body: JSON.stringify({ property_id: selected.id, ...inquiry }),
    }).catch((err) => setError(err.message));
    if (created) {
      setInquiry({ name: '', email: '', phone: '', message: '' });
      setNotice(`問い合わせを受け付けました。受付番号: ${created.id}`);
    }
  }

  return (
    <main>
      <header className="topbar">
        <div>
          <p className="eyebrow">Rental Search Mock</p>
          <h1>賃貸物件検索</h1>
        </div>
        <div className="userBadge">Demo user: {DEMO_USER_ID}</div>
      </header>

      <section className="searchBand">
        <form className="searchForm" onSubmit={submitSearch}>
          <label>
            キーワード
            <div className="inputIcon">
              <Search size={18} />
              <input
                value={filters.keyword}
                onChange={(event) => updateFilter('keyword', event.target.value)}
                placeholder="駅名・住所・物件名"
              />
            </div>
          </label>
          <label>
            駅名
            <select value={filters.station} onChange={(event) => updateFilter('station', event.target.value)}>
              <option value="">指定なし</option>
              {STATIONS.map((station) => (
                <option key={station} value={station}>
                  {station}
                </option>
              ))}
            </select>
          </label>
          <label>
            上限家賃
            <select value={filters.max_rent} onChange={(event) => updateFilter('max_rent', event.target.value)}>
              <option value="">指定なし</option>
              <option value="90000">9万円以下</option>
              <option value="140000">14万円以下</option>
              <option value="200000">20万円以下</option>
              <option value="300000">30万円以下</option>
            </select>
          </label>
          <label>
            間取り
            <select value={filters.layout} onChange={(event) => updateFilter('layout', event.target.value)}>
              <option value="">指定なし</option>
              <option value="1R">1R</option>
              <option value="1LDK">1LDK</option>
              <option value="2LDK">2LDK</option>
            </select>
          </label>
          <label>
            駅徒歩
            <select
              value={filters.max_walk_minutes}
              onChange={(event) => updateFilter('max_walk_minutes', event.target.value)}
            >
              <option value="">指定なし</option>
              <option value="5">5分以内</option>
              <option value="10">10分以内</option>
              <option value="15">15分以内</option>
            </select>
          </label>
          <button className="primaryButton" type="submit">
            <Search size={18} />
            検索
          </button>
        </form>
      </section>

      {error && <p className="message error">{error}</p>}
      {notice && <p className="message success">{notice}</p>}

      <div className="workspace">
        <section className="listPane">
          <div className="sectionHeader">
            <h2>
              検索結果
              <span>{properties.length}件</span>
            </h2>
          </div>
          <div className="propertyList">
            {properties.map((property) => (
              <article
                className={`propertyCard ${selected?.id === property.id ? 'active' : ''}`}
                key={property.id}
                onClick={() => chooseProperty(property.id)}
              >
                <img src={property.image_url} alt={property.building_name} />
                <div className="propertyCardBody">
                  <div className="cardTitleRow">
                    <h3>{property.building_name}</h3>
                    <span className={property.availability === '募集中' ? 'statusOpen' : 'statusPending'}>
                      {property.availability}
                    </span>
                  </div>
                  <p className="muted">
                    <TrainFront size={16} /> {property.station} 徒歩{property.walk_minutes}分
                  </p>
                  <p className="rent">{yen(property.rent_yen)} + 管理費 {yen(property.management_fee_yen)}</p>
                  <p className="muted">
                    {property.layout} / {property.area_sqm}m² / {property.floor}
                  </p>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="detailPane">
          {selected && (
            <>
              <img className="detailImage" src={selected.image_url} alt={selected.building_name} />
              <div className="detailHeader">
                <div>
                  <p className="eyebrow">{selected.title}</p>
                  <h2>{selected.building_name}</h2>
                </div>
              </div>

              <div className="factGrid">
                <div>
                  <span>家賃</span>
                  <strong>{yen(selected.rent_yen)}</strong>
                </div>
                <div>
                  <span>間取り</span>
                  <strong>{selected.layout}</strong>
                </div>
                <div>
                  <span>専有面積</span>
                  <strong>{selected.area_sqm}m²</strong>
                </div>
                <div>
                  <span>築年</span>
                  <strong>{selected.built_year}年</strong>
                </div>
              </div>

              <p className="address">
                <Building2 size={18} /> {selected.address}
              </p>
              <p>{selected.description}</p>
              <div className="tags">
                {selected.amenities.map((item) => (
                  <span key={item}>{item}</span>
                ))}
              </div>

              <form className="inquiryForm" onSubmit={submitInquiry}>
                <h3>
                  <Mail size={18} />
                  問い合わせ
                </h3>
                <input
                  required
                  value={inquiry.name}
                  onChange={(event) => setInquiry((current) => ({ ...current, name: event.target.value }))}
                  placeholder="氏名"
                />
                <input
                  required
                  type="email"
                  value={inquiry.email}
                  onChange={(event) => setInquiry((current) => ({ ...current, email: event.target.value }))}
                  placeholder="メールアドレス"
                />
                <input
                  required
                  value={inquiry.phone}
                  onChange={(event) => setInquiry((current) => ({ ...current, phone: event.target.value }))}
                  placeholder="電話番号"
                />
                <textarea
                  required
                  value={inquiry.message}
                  onChange={(event) => setInquiry((current) => ({ ...current, message: event.target.value }))}
                  placeholder="問い合わせ内容"
                  rows="4"
                />
                <button className="primaryButton" type="submit">
                  <Mail size={18} />
                  送信
                </button>
              </form>
            </>
          )}
        </section>

        <aside className="reservedPane" aria-hidden="true" />
      </div>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
