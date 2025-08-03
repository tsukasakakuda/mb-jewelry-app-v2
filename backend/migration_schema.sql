-- =====================================
-- 新データベーススキーマ（3テーブル構成）
-- =====================================

-- 1. 新しいusersテーブル（改良版）
CREATE TABLE users_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    role TEXT DEFAULT 'user',
    is_active INTEGER DEFAULT 1,  -- SQLiteではBOOLEANがINTEGER
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 新しいcalculationsテーブル
CREATE TABLE calculations_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    calculation_name TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users_new (id) ON DELETE CASCADE
);

-- 3. 新しいcalculation_itemsテーブル
CREATE TABLE calculation_items_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    calculation_id INTEGER NOT NULL,
    box_id INTEGER NOT NULL,
    box_no INTEGER,
    material TEXT,
    weight_text TEXT,
    weight_grams REAL,
    misc TEXT,
    
    -- 計算結果
    jewelry_price REAL,
    material_price REAL,
    total_weight REAL,
    gemstone_weight REAL,
    material_weight REAL,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (calculation_id) REFERENCES calculations_new (id) ON DELETE CASCADE
);

-- インデックス作成
CREATE INDEX idx_users_new_username ON users_new(username);
CREATE INDEX idx_users_new_role ON users_new(role);
CREATE INDEX idx_users_new_active ON users_new(is_active);

CREATE INDEX idx_calculations_new_user_id ON calculations_new(user_id);
CREATE INDEX idx_calculations_new_created_at ON calculations_new(created_at);

CREATE INDEX idx_calculation_items_new_calculation_id ON calculation_items_new(calculation_id);
CREATE INDEX idx_calculation_items_new_box_id ON calculation_items_new(box_id);
CREATE INDEX idx_calculation_items_new_box_combo ON calculation_items_new(box_id, box_no);
CREATE INDEX idx_calculation_items_new_material ON calculation_items_new(material);

-- 集計用VIEW（パフォーマンス向上のため）
CREATE VIEW calculation_summaries_view AS
SELECT 
    calculation_id,
    COUNT(*) as total_items,
    COALESCE(SUM(jewelry_price), 0) as total_value,
    COALESCE(SUM(total_weight), 0) as total_weight,
    COUNT(DISTINCT box_id) as unique_boxes,
    COALESCE(AVG(jewelry_price), 0) as average_item_value,
    MIN(created_at) as first_item_created,
    MAX(created_at) as last_item_created
FROM calculation_items_new
GROUP BY calculation_id;