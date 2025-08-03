#!/usr/bin/env python3
"""
シンプルなWebベースのDBビューワー
http://localhost:8081 でアクセス可能
"""

from flask import Flask, render_template_string, request, jsonify
import sqlite3
import json

app = Flask(__name__)

DATABASE_PATH = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>MB Jewelry - Database Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .query-box { width: 100%; height: 100px; margin: 10px 0; }
        .btn { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .btn:hover { background-color: #45a049; }
        .stats { display: flex; gap: 20px; margin: 20px 0; }
        .stat-card { background: #f5f5f5; padding: 15px; border-radius: 5px; flex: 1; }
        .error { color: red; background: #ffe6e6; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗄️ MB Jewelry Database Viewer</h1>
        
        <!-- 統計情報 -->
        <div class="stats">
            <div class="stat-card">
                <h3>Users</h3>
                <p id="user-count">Loading...</p>
            </div>
            <div class="stat-card">
                <h3>Calculations</h3>
                <p id="calc-count">Loading...</p>
            </div>
            <div class="stat-card">
                <h3>Items</h3>
                <p id="item-count">Loading...</p>
            </div>
        </div>

        <!-- テーブル選択 -->
        <h2>📊 Table Viewer</h2>
        <button class="btn" onclick="showTable('users')">Users</button>
        <button class="btn" onclick="showTable('calculations')">Calculations</button>
        <button class="btn" onclick="showTable('calculation_items')">Items</button>
        <button class="btn" onclick="showBoxStats()">Box Statistics</button>

        <!-- SQL実行 -->
        <h2>💻 Custom Query</h2>
        <textarea class="query-box" id="sqlQuery" placeholder="Enter SQL query here...">
SELECT box_id, COUNT(*) as count, SUM(jewelry_price) as total_value 
FROM calculation_items 
GROUP BY box_id 
ORDER BY total_value DESC 
LIMIT 10;
        </textarea><br>
        <button class="btn" onclick="executeQuery()">Execute Query</button>

        <!-- 結果表示 -->
        <div id="results"></div>
    </div>

    <script>
        // 統計情報を読み込み
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                document.getElementById('user-count').textContent = stats.users + ' users';
                document.getElementById('calc-count').textContent = stats.calculations + ' calculations';
                document.getElementById('item-count').textContent = stats.items + ' items';
            } catch (error) {
                console.error('Failed to load stats:', error);
            }
        }

        // テーブル表示
        async function showTable(tableName) {
            let query;
            switch(tableName) {
                case 'users':
                    query = 'SELECT id, username, role, is_active, created_at FROM users ORDER BY id;';
                    break;
                case 'calculations':
                    query = 'SELECT id, user_id, calculation_name, created_at FROM calculations ORDER BY id;';
                    break;
                case 'calculation_items':
                    query = 'SELECT id, calculation_id, box_id, box_no, material, weight_text, jewelry_price FROM calculation_items ORDER BY box_id, box_no LIMIT 50;';
                    break;
            }
            await executeCustomQuery(query);
        }

        // 箱統計表示
        async function showBoxStats() {
            const query = `
                SELECT 
                    box_id,
                    COUNT(*) as item_count,
                    ROUND(SUM(jewelry_price), 2) as total_value,
                    GROUP_CONCAT(DISTINCT material) as materials
                FROM calculation_items 
                WHERE box_id IS NOT NULL 
                GROUP BY box_id 
                ORDER BY total_value DESC 
                LIMIT 20;
            `;
            await executeCustomQuery(query);
        }

        // クエリ実行
        async function executeQuery() {
            const query = document.getElementById('sqlQuery').value;
            await executeCustomQuery(query);
        }

        // カスタムクエリ実行
        async function executeCustomQuery(query) {
            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });
                
                const result = await response.json();
                
                if (result.error) {
                    document.getElementById('results').innerHTML = 
                        '<div class="error">Error: ' + result.error + '</div>';
                    return;
                }

                // テーブル形式で結果表示
                let html = '<h3>Query Results (' + result.rows.length + ' rows)</h3>';
                
                if (result.rows.length > 0) {
                    html += '<table>';
                    html += '<tr>';
                    Object.keys(result.rows[0]).forEach(key => {
                        html += '<th>' + key + '</th>';
                    });
                    html += '</tr>';
                    
                    result.rows.forEach(row => {
                        html += '<tr>';
                        Object.values(row).forEach(value => {
                            html += '<td>' + (value !== null ? value : '') + '</td>';
                        });
                        html += '</tr>';
                    });
                    html += '</table>';
                } else {
                    html += '<p>No results found.</p>';
                }
                
                document.getElementById('results').innerHTML = html;
            } catch (error) {
                document.getElementById('results').innerHTML = 
                    '<div class="error">Network error: ' + error.message + '</div>';
            }
        }

        // ページ読み込み時に統計を表示
        window.onload = function() {
            loadStats();
            showTable('users'); // デフォルトでユーザーテーブルを表示
        };
    </script>
</body>
</html>
    ''')

@app.route('/api/stats')
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM calculations')
        calc_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM calculation_items')
        item_count = cursor.fetchone()[0]
        
        return jsonify({
            'users': user_count,
            'calculations': calc_count,
            'items': item_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/query', methods=['POST'])
def execute_query():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query.strip():
            return jsonify({'error': 'Empty query'}), 400
        
        # 安全性チェック（基本的な制限）
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE']
        query_upper = query.upper()
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return jsonify({'error': f'Dangerous keyword "{keyword}" not allowed'}), 400
        
        cursor.execute(query)
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        
        # Row オブジェクトを辞書に変換
        result_rows = []
        for row in rows:
            result_rows.append(dict(zip(columns, row)))
        
        return jsonify({
            'columns': columns,
            'rows': result_rows
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    print("🌐 Database Viewer starting at http://localhost:8081")
    print("📊 Features:")
    print("   - View all tables")
    print("   - Execute custom SQL queries")
    print("   - Real-time statistics")
    print("   - Box number analysis")
    app.run(debug=True, host='0.0.0.0', port=8081)