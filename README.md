
# 💾 Database Schema: `ledger`

## ⚙️ 실행 명령어

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 3000
```

🧑‍💻 Users Table
Column	Type	Constraints	Description
id	CHAR(36)	PRIMARY KEY, NOT NULL	UUID (user unique ID)
email	VARCHAR(255)	NOT NULL, UNIQUE	사용자 이메일
hashed_password	VARCHAR(255)	NOT NULL	해시된 비밀번호
created_at	TIMESTAMP	DEFAULT CURRENT_TIMESTAMP	생성 시각

🗂️ Categories Table
Column	Type	Constraints	Description
id	CHAR(36)	PRIMARY KEY, NOT NULL	UUID (category unique ID)
user_id	CHAR(36)	NOT NULL, FOREIGN KEY → users(id)	사용자 ID (소유자)
name	VARCHAR(100)	NOT NULL	카테고리 이름
type	ENUM('income', 'expense')	NOT NULL	카테고리 유형 (수입/지출)
color	VARCHAR(7)	DEFAULT '#000000'	색상 코드 (HEX 형식)
created_at	TIMESTAMP	DEFAULT CURRENT_TIMESTAMP	생성 시각

Foreign Keys

user_id → users(id) (ON DELETE CASCADE)

💸 Transactions Table
Column	Type	Constraints	Description
id	CHAR(36)	PRIMARY KEY, NOT NULL	UUID (transaction unique ID)
user_id	CHAR(36)	NOT NULL, FOREIGN KEY → users(id)	사용자 ID
category_id	CHAR(36)	NULL, FOREIGN KEY → categories(id)	카테고리 ID (nullable)
amount	DECIMAL(12,2)	NOT NULL	거래 금액
description	TEXT	—	거래 설명
transaction_date	DATE	NOT NULL	거래 발생일
created_at	TIMESTAMP	DEFAULT CURRENT_TIMESTAMP	생성 시각

Foreign Keys

user_id → users(id) (ON DELETE CASCADE)

category_id → categories(id) (ON DELETE SET NULL)

📄 SQL Schema
sql
코드 복사
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) NOT NULL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id CHAR(36) NOT NULL PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    type ENUM('income', 'expense') NOT NULL,
    color VARCHAR(7) DEFAULT '#000000',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transactions (
    id CHAR(36) NOT NULL PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    category_id CHAR(36) NULL,
    amount DECIMAL(12,2) NOT NULL,
    description TEXT,
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);
🧭 관계 요약 (ER 구조)
scss
코드 복사
Users (1) ────< (N) Categories
Users (1) ────< (N) Transactions
Categories (1) ────< (N) Transactions (nullable)