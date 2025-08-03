"""
新しい3テーブル構造に対応したAPI v3
- 旧APIとの互換性を保ちつつ新構造に対応
- パフォーマンス改善
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from datetime import datetime
import numpy as np
import pandas as pd
import re
import io
import os
import json
import jwt
import hashlib
from functools import wraps

# 新しいマネージャーをインポート
from user_manager import user_manager  # ユーザー管理は既存のままでOK
from calculation_manager_v3 import calculation_manager_v3

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app)

# 認証設定
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.current_user = payload
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(*args, **kwargs)
    return decorated

# =====================================
# 認証エンドポイント（既存のまま）
# =====================================

@app.route('/api/login', methods=['POST'])
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'message': 'ユーザー名とパスワードが必要です'}), 400
        
        user = user_manager.authenticate_user(username, password)
        
        if user:
            from datetime import datetime, timezone
            token = jwt.encode({
                'user_id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'exp': datetime.now(timezone.utc).timestamp() + 3600
            }, SECRET_KEY, algorithm='HS256')
            
            return jsonify({
                'token': token, 
                'message': 'ログインに成功しました',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'role': user['role']
                }
            })
        else:
            return jsonify({'message': 'ユーザー名またはパスワードが間違っています'}), 401
    
    except Exception as e:
        print(f"❌ Login error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'サーバーエラーが発生しました'}), 500

# =====================================
# 計算関連エンドポイント（v3対応）
# =====================================

@app.route('/api/save-calculation', methods=['POST'])
@app.route('/save-calculation', methods=['POST'])
@token_required
def save_calculation():
    """計算結果を新しい3テーブル構造に保存"""
    try:
        print("=== Save Calculation API v3 Called ===")
        data = request.json
        print(f"Request data keys: {list(data.keys()) if data else 'None'}")
        
        if not data:
            return jsonify({'error': 'No JSON provided'}), 400
        
        user_id = request.current_user.get('user_id')
        calculation_name = data.get('calculation_name', f"計算_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        item_data = data.get('item_data', [])
        calculation_results = data.get('calculation_results', {})
        
        print(f"User ID: {user_id}, Calculation name: {calculation_name}")
        print(f"Item data count: {len(item_data)}")
        
        if not item_data:
            return jsonify({'error': 'アイテムデータが必要です'}), 400
        
        if not user_id:
            return jsonify({'error': 'ユーザーIDが見つかりません'}), 400
        
        # 新しいマネージャーで保存
        history_id = calculation_manager_v3.save_calculation(
            user_id=user_id,
            calculation_name=calculation_name,
            item_data=item_data,
            calculation_results=calculation_results
        )
        
        if history_id:
            return jsonify({
                'message': '計算結果が保存されました（v3）',
                'history_id': history_id
            }), 201
        else:
            return jsonify({'error': '計算結果の保存に失敗しました'}), 500
            
    except Exception as e:
        print(f"Exception in save_calculation v3: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculation-history', methods=['GET'])
@app.route('/calculation-history', methods=['GET'])
@token_required
def get_calculation_history():
    """ユーザーの計算履歴一覧を取得（v3対応）"""
    try:
        user_id = request.current_user.get('user_id')
        limit = request.args.get('limit', 50, type=int)
        
        print(f"📋 計算履歴取得開始 v3 - User ID: {user_id}, Limit: {limit}")
        histories = calculation_manager_v3.get_calculation_history(user_id, limit)
        print(f"✅ 計算履歴取得完了 v3 - 件数: {len(histories)}")
        return jsonify({'histories': histories})
        
    except Exception as e:
        print(f"❌ 計算履歴取得エラー v3: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculation-history/<int:history_id>', methods=['GET'])
@app.route('/calculation-history/<int:history_id>', methods=['GET'])
@token_required
def get_calculation_detail(history_id):
    """計算履歴の詳細を取得（v3対応）"""
    try:
        user_id = request.current_user.get('user_id')
        
        detail = calculation_manager_v3.get_calculation_detail(history_id, user_id)
        if detail:
            return jsonify(detail)
        else:
            return jsonify({'error': '計算履歴が見つかりません'}), 404
            
    except Exception as e:
        print(f"❌ 計算詳細取得エラー v3: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculation-history/box-groups', methods=['GET'])
@app.route('/calculation-history/box-groups', methods=['GET'])
@token_required
def get_calculation_box_groups():
    """箱番号ごとにグループ化された計算履歴を取得（v3対応・最適化版）"""
    try:
        user_id = request.current_user.get('user_id')
        max_per_box = request.args.get('max_per_box', 10, type=int)
        
        print(f"📦 箱番号グループ取得開始 v3 - User ID: {user_id}, Max per box: {max_per_box}")
        
        # 新しいマネージャーで最適化されたクエリを実行
        box_groups = calculation_manager_v3.get_box_groups(user_id, max_per_box)
        
        print(f"✅ 箱番号グループ取得完了 v3 - グループ数: {len(box_groups)}")
        return jsonify({'box_groups': box_groups})
        
    except Exception as e:
        print(f"❌ 箱番号グループ取得エラー v3: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculation-history/<int:history_id>/box-groups', methods=['GET'])
@app.route('/calculation-history/<int:history_id>/box-groups', methods=['GET'])
@token_required
def get_calculation_box_groups_by_history(history_id):
    """特定の計算履歴内で箱番号ごとにグループ化されたアイテムを取得"""
    try:
        user_id = request.current_user.get('user_id')
        
        print(f"📦 特定履歴内箱番号グループ取得開始 - History ID: {history_id}, User ID: {user_id}")
        
        # 特定の計算履歴内でのボックスグループを取得
        box_groups = calculation_manager_v3.get_box_groups_by_calculation(history_id, user_id)
        
        print(f"✅ 特定履歴内箱番号グループ取得完了 - グループ数: {len(box_groups)}")
        return jsonify({'box_groups': box_groups, 'history_id': history_id})
        
    except Exception as e:
        print(f"❌ 特定履歴内箱番号グループ取得エラー: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculation-history/<int:history_id>', methods=['DELETE'])
@app.route('/calculation-history/<int:history_id>', methods=['DELETE'])
@token_required
def delete_calculation(history_id):
    """計算履歴を削除（v3対応）"""
    try:
        user_id = request.current_user.get('user_id')
        
        success = calculation_manager_v3.delete_calculation(history_id, user_id)
        if success:
            return jsonify({'message': '計算履歴が削除されました'})
        else:
            return jsonify({'error': '計算履歴の削除に失敗しました'}), 404
            
    except Exception as e:
        print(f"❌ 計算履歴削除エラー v3: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculation-stats', methods=['GET'])
@app.route('/calculation-stats', methods=['GET'])
@token_required
def get_calculation_stats():
    """ユーザーの計算統計を取得（v3対応）"""
    try:
        user_id = request.current_user.get('user_id')
        
        stats = calculation_manager_v3.get_user_statistics(user_id)
        return jsonify(stats)
        
    except Exception as e:
        print(f"❌ 統計情報取得エラー v3: {e}")
        return jsonify({'error': str(e)}), 500

# =====================================
# 既存の計算処理エンドポイント（そのまま）
# =====================================

def load_material_aliases(json_path="material_price_map.json"):
    with open(json_path, encoding='utf-8') as f:
        raw = json.load(f)
    alias_to_main = {}
    for main, aliases in raw.items():
        for alias in aliases:
            alias_to_main[alias.lower()] = main.lower()
    return alias_to_main

material_aliases = load_material_aliases()

def ensure_required_columns(df, required_columns):
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
    return df

def calculate_items(item_df, price_df):
    price_df['price'] = pd.to_numeric(price_df['price'], errors='coerce').fillna(0)
    price_dict_raw = dict(zip(price_df['material'].str.lower(), price_df['price']))

    price_dict = {}
    for alias, main in material_aliases.items():
        if main in price_dict_raw:
            price_dict[alias] = price_dict_raw[main]

    def calculate(row):
        try:
            raw = str(row['weight']).split('g')[0]
            cleaned = re.sub(r'[^0-9.]', '', raw)
            total_weight = float(cleaned) if cleaned else 0.0
        except Exception:
            total_weight = 0.0

        gemstone_weight = 0.0
        material_price = 0.0
        parts = str(row['misc']).split() if pd.notna(row['misc']) else []
        material_field = str(row['material']).strip().lower() if pd.notna(row['material']) else ""

        if "/" in material_field:
            sub_materials = material_field.split("/")
            prices = [price_dict.get(m.strip()) for m in sub_materials]
            valid_prices = [p for p in prices if p is not None]
            material_price = np.mean(valid_prices) if len(valid_prices) == len(sub_materials) else 0
        else:
            material_price = price_dict.get(material_field, 0)

        for part in parts:
            if any(x in part for x in ['#', 'cm', '%']):
                continue
            matches = re.findall(r'(\d+(?:\.\d+)?)', part)
            if matches:
                num = float(matches[0])
                if 'mm' in part:
                    gemstone_weight += num ** 3 / 700
                elif '.' in part:
                    gemstone_weight += num * 0.2

        material_weight = total_weight - gemstone_weight
        material_value = material_weight * material_price

        return pd.Series([
            material_value, material_price, total_weight,
            gemstone_weight, material_weight
        ])

    item_df[['jewelry_price', 'material_price', 'total_weight', 'gemstone_weight', 'material_weight']] = item_df.apply(calculate, axis=1)
    return item_df

@app.route('/api/calculate-fixed', methods=['POST'])
@app.route('/calculate-fixed', methods=['POST'])
@token_required
def calculate_fixed():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON provided'}), 400

        item_df = pd.DataFrame(data.get('item_data', []))
        price_df = pd.DataFrame(data.get('price_data', []))

        for idx, row in item_df.iterrows():
            if 'weight' in row and str(row['weight']).strip() == "":
                item_df.at[idx, 'weight'] = None

        required_columns = ['box_id', 'box_no', 'material', 'misc', 'weight']
        item_df = ensure_required_columns(item_df, required_columns)

        result_df = calculate_items(item_df, price_df)

        result_df['box_no'] = pd.to_numeric(result_df['box_no'], errors='coerce').fillna(0).astype(int)
        result_df['box_id'] = pd.to_numeric(result_df['box_id'], errors='coerce').fillna(0).astype(int)
        result_df = result_df.sort_values(by=['box_id', 'box_no'])

        output_columns = [
            'box_id', 'box_no', 'material', 'misc', 'weight',
            'jewelry_price', 'material_price', 'total_weight',
            'gemstone_weight', 'material_weight'
        ]
        result_df = result_df[[col for col in output_columns if col in result_df.columns]]

        return_format = request.args.get('format', 'csv')
        
        if return_format == 'json':
            calculated_items = result_df.to_dict('records')
            return jsonify({
                'calculated_items': calculated_items,
                'total_items': len(calculated_items),
                'total_value': sum(float(item.get('jewelry_price', 0)) for item in calculated_items)
            })
        else:
            output = io.StringIO()
            result_df.to_csv(output, index=False)
            output.seek(0)

            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename_cal = f"calculated_result_{timestamp}.csv"

            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8-sig')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename_cal
            )

    except Exception as e:
        print(f"❌ Calculate fixed error: {e}")
        return jsonify({'error': str(e)}), 500

# =====================================
# 管理者専用エンドポイント
# =====================================

@app.route('/api/admin/db-content', methods=['GET'])
@app.route('/admin/db-content', methods=['GET'])
@token_required
def admin_view_db_content():
    """管理者専用: データベースの全内容を確認"""
    try:
        # 管理者権限チェック
        if request.current_user.get('role') != 'admin':
            return jsonify({'message': '管理者権限が必要です'}), 403
        
        import sqlite3
        from calculation_manager_v3 import DATABASE_PATH
        
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # テーブル一覧を取得
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        db_content = {}
        max_rows = request.args.get('max_rows', 100, type=int)  # デフォルト100件制限
        
        for table in tables:
            if table == 'sqlite_sequence':
                continue  # システムテーブルをスキップ
                
            # 件数制限付きでデータ取得
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            total_count = cursor.fetchone()[0]
            
            cursor.execute(f"SELECT * FROM {table} LIMIT {max_rows}")
            rows = cursor.fetchall()
            
            db_content[table] = {
                'data': [dict(row) for row in rows],
                'total_count': total_count,
                'displayed_count': len(rows),
                'limited': total_count > max_rows
            }
        
        conn.close()
        
        return jsonify({
            'tables': tables,
            'content': db_content,
            'database_path': DATABASE_PATH
        })
        
    except Exception as e:
        print(f"❌ Admin DB content error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/download-db', methods=['GET'])
@app.route('/admin/download-db', methods=['GET'])
@token_required
def admin_download_db():
    """管理者専用: SQLiteデータベースファイルをダウンロード"""
    try:
        # 管理者権限チェック
        if request.current_user.get('role') != 'admin':
            return jsonify({'message': '管理者権限が必要です'}), 403
        
        from calculation_manager_v3 import DATABASE_PATH
        import os
        
        if not os.path.exists(DATABASE_PATH):
            return jsonify({'error': 'データベースファイルが見つかりません'}), 404
        
        return send_file(
            DATABASE_PATH,
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name='mb_jewelry_database.db'
        )
        
    except Exception as e:
        print(f"❌ Admin DB download error: {e}")
        return jsonify({'error': str(e)}), 500

# =====================================
# アイテム更新エンドポイント
# =====================================

@app.route('/api/calculation-history/<int:history_id>/item/<int:item_index>', methods=['PUT'])
@app.route('/calculation-history/<int:history_id>/item/<int:item_index>', methods=['PUT'])
@token_required
def update_calculation_item(history_id, item_index):
    """計算履歴の特定のアイテムを更新（v3版）"""
    try:
        user_id = request.current_user.get('user_id')
        
        # 計算履歴の詳細を取得
        detail = calculation_manager_v3.get_calculation_detail(history_id, user_id)
        if not detail:
            return jsonify({'error': '計算履歴が見つかりません'}), 404
        
        # アイテムインデックスの検証
        items = detail['calculation_data']['items']
        if item_index < 0 or item_index >= len(items):
            return jsonify({'error': '無効なアイテムインデックスです'}), 400
        
        # 更新データの取得
        update_data = request.get_json()
        if not update_data:
            return jsonify({'error': '更新データが必要です'}), 400
        
        # 該当アイテムのIDを取得
        item_id = items[item_index].get('id')
        if not item_id:
            return jsonify({'error': 'アイテムIDが見つかりません'}), 400
        
        # アイテムデータの更新
        success = calculation_manager_v3.update_calculation_item(
            calculation_id=history_id,
            item_id=item_id,
            user_id=user_id,
            update_data=update_data
        )
        
        if success:
            return jsonify({'message': 'アイテムが正常に更新されました'})
        else:
            return jsonify({'error': 'アイテム更新に失敗しました'}), 500
        
    except Exception as e:
        print(f"❌ アイテム更新エラー: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# =====================================
# その他のエンドポイント（既存のまま）
# =====================================

@app.route('/')
def serve_vue():
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(error):
    """404エラーハンドラー - Vue Router用のSPA対応"""
    path = request.path
    
    if path.startswith('/api/') or path.startswith('/api'):
        return jsonify({'error': 'API endpoint not found'}), 404
    
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print(f"✅ Starting Flask v3 on port {port}")
    app.run(debug=False, host="0.0.0.0", port=port)