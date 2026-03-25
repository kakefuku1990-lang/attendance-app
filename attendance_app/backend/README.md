# 勤怠管理アプリ

## 📌 概要

Django + Docker + PostgreSQL を用いた勤怠管理アプリです。
打刻・申請・承認・レポート出力までを実装しています。

---

## 🛠 技術スタック

* Python / Django
* PostgreSQL
* Docker / Docker Compose

---

## 🚀 環境構築

```bash
docker compose up -d
```

---

## 🧩 初回セットアップ

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

---

## 🔑 ログイン

```plaintext
http://localhost:8000/accounts/login/
```

---

## 📊 主な機能

### 勤怠

* 出勤 / 退勤
* 勤務時間・残業時間計算

### 申請

* 休暇申請
* 残業申請

### 承認

* 上長による承認 / 却下
* ロール（社員 / 上長 / 管理者）による制御

### レポート

* 月次勤怠レポート
* CSVエクスポート

---

## 🧪 テスト

```bash
docker compose exec web python manage.py test
```

---

## 📦 バックアップ

```bash
docker compose exec db pg_dump -U <DB_USER> <DB_NAME> > backup.sql
```

---

## 📜 ログ確認

```bash
docker compose logs web
```

---

## 📁 ディレクトリ構成（抜粋）

```plaintext
attendance/
├── models.py
├── views.py
├── services/
└── templates/

accounts/
├── models.py
└── ...
```

---

## 💡 設計ポイント

* Service Layerによるロジック分離
* 認証 / 認可の分離
* 再利用可能な構成

---

## 🎯 今後の拡張案

* API化（Django REST Framework）
* フロントエンド（React）
* 勤務形態（フレックス等）対応
