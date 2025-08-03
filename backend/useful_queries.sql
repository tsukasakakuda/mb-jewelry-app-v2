-- =====================================
-- MB Jewelry Database - 実用的なクエリ集
-- =====================================

-- 1. 基本的な統計情報
SELECT 
    'Total Users' as metric, COUNT(*) as value FROM users
UNION ALL
SELECT 'Total Calculations', COUNT(*) FROM calculations
UNION ALL
SELECT 'Total Items', COUNT(*) FROM calculation_items
UNION ALL
SELECT 'Unique Boxes', COUNT(DISTINCT box_id) FROM calculation_items WHERE box_id IS NOT NULL;

-- 2. 箱番号別の詳細統計（価値の高い順）
SELECT 
    box_id,
    COUNT(*) as item_count,
    ROUND(SUM(jewelry_price), 2) as total_value,
    ROUND(AVG(jewelry_price), 2) as avg_value,
    GROUP_CONCAT(DISTINCT material) as materials,
    MAX(created_at) as last_updated
FROM calculation_items 
WHERE box_id IS NOT NULL 
GROUP BY box_id 
ORDER BY total_value DESC 
LIMIT 20;

-- 3. 素材別の統計
SELECT 
    material,
    COUNT(*) as item_count,
    ROUND(SUM(jewelry_price), 2) as total_value,
    ROUND(AVG(jewelry_price), 2) as avg_value,
    COUNT(DISTINCT box_id) as box_count
FROM calculation_items 
WHERE material IS NOT NULL AND material != ''
GROUP BY material 
ORDER BY total_value DESC;

-- 4. ユーザー別の活動統計
SELECT 
    u.username,
    u.role,
    COUNT(c.id) as calculation_count,
    COUNT(ci.id) as total_items,
    ROUND(COALESCE(SUM(ci.jewelry_price), 0), 2) as total_value,
    MAX(c.created_at) as last_calculation
FROM users u
LEFT JOIN calculations c ON u.id = c.user_id
LEFT JOIN calculation_items ci ON c.id = ci.calculation_id
GROUP BY u.id, u.username, u.role
ORDER BY total_value DESC;

-- 5. 計算履歴の詳細（最新順）
SELECT 
    c.id,
    c.calculation_name,
    c.created_at,
    COUNT(ci.id) as item_count,
    ROUND(COALESCE(SUM(ci.jewelry_price), 0), 2) as total_value,
    COUNT(DISTINCT ci.box_id) as unique_boxes
FROM calculations c
LEFT JOIN calculation_items ci ON c.id = ci.calculation_id
GROUP BY c.id, c.calculation_name, c.created_at
ORDER BY c.created_at DESC;

-- 6. 高額アイテムトップ20
SELECT 
    ci.box_id,
    ci.box_no,
    ci.material,
    ci.weight_text,
    ROUND(ci.jewelry_price, 2) as price,
    c.calculation_name,
    ci.created_at
FROM calculation_items ci
JOIN calculations c ON ci.calculation_id = c.id
WHERE ci.jewelry_price IS NOT NULL
ORDER BY ci.jewelry_price DESC
LIMIT 20;

-- 7. 箱番号の使用頻度分析
SELECT 
    'Low value (< 10,000)' as price_range,
    COUNT(*) as box_count
FROM (
    SELECT box_id, SUM(jewelry_price) as total_value
    FROM calculation_items 
    WHERE box_id IS NOT NULL
    GROUP BY box_id
    HAVING total_value < 10000
)
UNION ALL
SELECT 'Medium value (10,000 - 100,000)', COUNT(*)
FROM (
    SELECT box_id, SUM(jewelry_price) as total_value
    FROM calculation_items 
    WHERE box_id IS NOT NULL
    GROUP BY box_id
    HAVING total_value BETWEEN 10000 AND 100000
)
UNION ALL
SELECT 'High value (> 100,000)', COUNT(*)
FROM (
    SELECT box_id, SUM(jewelry_price) as total_value
    FROM calculation_items 
    WHERE box_id IS NOT NULL
    GROUP BY box_id
    HAVING total_value > 100000
);

-- 8. 月別の活動統計
SELECT 
    strftime('%Y-%m', created_at) as month,
    COUNT(*) as calculation_count,
    SUM(item_count) as total_items
FROM (
    SELECT 
        c.created_at,
        COUNT(ci.id) as item_count
    FROM calculations c
    LEFT JOIN calculation_items ci ON c.id = ci.calculation_id
    GROUP BY c.id, c.created_at
)
GROUP BY strftime('%Y-%m', created_at)
ORDER BY month DESC;

-- 9. データ品質チェック
SELECT 
    'Items without box_id' as check_name,
    COUNT(*) as count
FROM calculation_items 
WHERE box_id IS NULL
UNION ALL
SELECT 'Items without material', COUNT(*)
FROM calculation_items 
WHERE material IS NULL OR material = ''
UNION ALL
SELECT 'Items without price', COUNT(*)
FROM calculation_items 
WHERE jewelry_price IS NULL OR jewelry_price = 0
UNION ALL
SELECT 'Items without weight', COUNT(*)
FROM calculation_items 
WHERE weight_text IS NULL OR weight_text = '';

-- 10. 最近の活動（直近7日）
SELECT 
    DATE(created_at) as date,
    COUNT(*) as new_items,
    ROUND(SUM(jewelry_price), 2) as daily_value
FROM calculation_items 
WHERE created_at >= datetime('now', '-7 days')
GROUP BY DATE(created_at)
ORDER BY date DESC;