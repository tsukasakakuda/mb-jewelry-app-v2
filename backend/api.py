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
import os

# 環境変数でマネージャーのバージョンを選択
USE_CLOUD_SQL = os.getenv('DB_TYPE') == 'postgresql'

if USE_CLOUD_SQL:
    from user_manager_v2 import UserManager
    from calculation_manager_v2 import CalculationManager
    user_manager = UserManager()
    calculation_manager = CalculationManager()
else:
    from user_manager import user_manager
    from calculation_manager import calculation_manager

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app)

# 認証設定
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# 旧方式のユーザー辞書は削除（データベースを使用）

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
            # トークンからユーザー情報を取得してrequestに設定
            request.current_user = payload
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(*args, **kwargs)
    return decorated

@app.route('/api/login', methods=['POST'])
@app.route('/login', methods=['POST'])  # For local development with Vite proxy
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'message': 'ユーザー名とパスワードが必要です'}), 400
        
        # データベースでユーザー認証
        user = user_manager.authenticate_user(username, password)
        
        if user:
            from datetime import datetime, timezone
            token = jwt.encode({
                'user_id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'exp': datetime.now(timezone.utc).timestamp() + 3600  # 1時間有効
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

# ユーザー情報取得エンドポイント
@app.route('/api/user/profile', methods=['GET'])
@app.route('/user/profile', methods=['GET'])
@token_required
def get_user_profile():
    """現在のユーザー情報を取得"""
    try:
        user_id = request.current_user.get('user_id')
        user = user_manager.get_user_by_id(user_id)
        
        if user:
            return jsonify({
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role'],
                    'created_at': user['created_at']
                }
            })
        else:
            return jsonify({'message': 'ユーザーが見つかりません'}), 404
            
    except Exception as e:
        return jsonify({'message': 'サーバーエラーが発生しました'}), 500

# パスワード変更エンドポイント
@app.route('/api/user/change-password', methods=['POST'])
@app.route('/user/change-password', methods=['POST'])
@token_required
def change_password():
    """パスワード変更"""
    try:
        data = request.json
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'message': '現在のパスワードと新しいパスワードが必要です'}), 400
        
        user_id = request.current_user.get('user_id')
        username = request.current_user.get('username')
        
        # 現在のパスワードを確認
        if not user_manager.authenticate_user(username, current_password):
            return jsonify({'message': '現在のパスワードが間違っています'}), 400
        
        # パスワード更新
        if user_manager.update_password(user_id, new_password):
            return jsonify({'message': 'パスワードが正常に更新されました'})
        else:
            return jsonify({'message': 'パスワードの更新に失敗しました'}), 500
            
    except Exception as e:
        return jsonify({'message': 'サーバーエラーが発生しました'}), 500

# 管理者専用: ユーザー一覧取得
@app.route('/api/admin/users', methods=['GET'])
@app.route('/admin/users', methods=['GET'])
@token_required
def admin_list_users():
    """管理者専用: ユーザー一覧取得"""
    try:
        # 管理者権限チェック
        if request.current_user.get('role') != 'admin':
            return jsonify({'message': '管理者権限が必要です'}), 403
        
        users = user_manager.list_users(active_only=False)
        return jsonify({'users': users})
        
    except Exception as e:
        return jsonify({'message': 'サーバーエラーが発生しました'}), 500

# 管理者専用: ユーザー作成
@app.route('/api/admin/users', methods=['POST'])
@app.route('/admin/users', methods=['POST'])
@token_required
def admin_create_user():
    """管理者専用: 新しいユーザーを作成"""
    try:
        # 管理者権限チェック
        if request.current_user.get('role') != 'admin':
            return jsonify({'message': '管理者権限が必要です'}), 403
        
        data = request.json
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role', 'user')
        
        if not username or not password:
            return jsonify({'message': 'ユーザー名とパスワードが必要です'}), 400
        
        user_id = user_manager.create_user(username, password, email, role)
        
        if user_id:
            return jsonify({
                'message': 'ユーザーが正常に作成されました',
                'user_id': user_id
            }), 201
        else:
            return jsonify({'message': 'ユーザーの作成に失敗しました'}), 400
            
    except Exception as e:
        return jsonify({'message': 'サーバーエラーが発生しました'}), 500

@app.route('/api/edit-csv', methods=['POST'])
@app.route('/edit-csv', methods=['POST'])  # For local development with Vite proxy
@token_required
def edit_csv():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'CSVファイルが必要です'}), 400

        df = pd.read_csv(file)

        # カラム結合（NaN対応）: "misc + weight" → "詳細情報"
        #['misc', 'weight', 'jewelry_carat', 'jewelry_color', 'jewelry_clarity', 'jewelry_cutting', 'jewelry_shape', 'jewelry_polish', 'jewelry_symmetry', 'jewelry_3ex', 'jewelry_h_c', 'jewelry_fluorescence']
        df['feature'] = df[['misc', 'weight', 'jewelry_carat', 'jewelry_color', 'jewelry_clarity', 'jewelry_cutting', 'jewelry_shape', 'jewelry_polish', 'jewelry_symmetry', 'jewelry_fluorescence']].fillna('').astype(str).agg(' '.join, axis=1).str.strip()


        # 残したいカラムと対応する日本語ラベル
        column_map = {
            'end_date': '大会日',
            'box_id': '箱番',
            'box_no': '枝番',
            'subcategory_name': '品目',
            'brand_name': 'ブランド',
            'material': '素材',
            'feature': '備考',
            'accessory_comment': '付属品'
        }

        # 必要なカラムだけを抽出
        needed_columns = [col for col in column_map.keys() if col in df.columns]
        df = df[needed_columns]

        # カラム名を日本語に変換
        df = df.rename(columns=column_map)

        # CSVをバイトストリームにして返す
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename_edt = f"edited_result_{timestamp}.csv"

        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename_edt
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- エイリアスマップ読み込み ---
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

def check_invalid_weights(df):
    invalid_rows = []
    for idx, row in df.iterrows():
        weight_value = str(row.get('weight', '')).strip()
        if weight_value:
            try:
                cleaned = re.sub(r'[^0-9.]', '', weight_value.split('g')[0])
                float(cleaned)
            except ValueError:
                invalid_rows.append({
                    'index': idx,
                    'weight': weight_value,
                    'row_data': row.to_dict()
                })
    return invalid_rows

def calculate_items(item_df, price_df):
    # --- 金額辞書を作る（素材名はエイリアス含む） ---
    price_df['price'] = pd.to_numeric(price_df['price'], errors='coerce').fillna(0)
    price_dict_raw = dict(zip(price_df['material'].str.lower(), price_df['price']))

    # エイリアス展開
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

        # 複数素材を処理（例: "pt900/k18"）
        if "/" in material_field:
            sub_materials = material_field.split("/")
            prices = [price_dict.get(m.strip()) for m in sub_materials]
            valid_prices = [p for p in prices if p is not None]
            material_price = np.mean(valid_prices) if len(valid_prices) == len(sub_materials) else 0
        else:
            material_price = price_dict.get(material_field, 0)

        # 宝石重量推定
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

@app.route('/api/check-weights', methods=['POST'])
@app.route('/check-weights', methods=['POST'])  # For local development with Vite proxy
@token_required
def check_weights():
    try:
        file = request.files.get('item_file')
        if not file:
            return jsonify({'error': 'item_file is required'}), 400

        df = pd.read_csv(file)

        required_columns = ['box_id', 'box_no', 'material', 'misc', 'weight']
        df = ensure_required_columns(df, required_columns)

        invalids = []
        for idx, row in df.iterrows():
            val = row.get('weight')
            if pd.isna(val) or str(val).strip() == "":
                continue
            val = str(val).strip()
            try:
                cleaned = re.sub(r'[^0-9.]', '', val.split('g')[0])
                float(cleaned)
            except Exception:
                clean_row = row.to_dict()
                for k, v in clean_row.items():
                    if pd.isna(v) or (isinstance(v, float) and np.isnan(v)):
                        clean_row[k] = ""
                invalids.append({
                    'index': idx,
                    'weight': val,
                    'box_id': row.get('box_id', ''),
                    'box_no': row.get('box_no', ''),
                    'row_data': clean_row
                })

        return jsonify({'invalid_weights': invalids})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculate-fixed', methods=['POST'])
@app.route('/calculate-fixed', methods=['POST'])  # For local development with Vite proxy
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

        # ✅ 出力対象のカラムだけに制限
        output_columns = [
            'box_id', 'box_no', 'material', 'misc', 'weight',
            'jewelry_price', 'material_price', 'total_weight',
            'gemstone_weight', 'material_weight'
        ]
        result_df = result_df[[col for col in output_columns if col in result_df.columns]]

        # クエリパラメータで戻り値形式を選択
        return_format = request.args.get('format', 'csv')
        
        if return_format == 'json':
            # JSONで計算結果を返す（DB保存用）
            calculated_items = result_df.to_dict('records')
            return jsonify({
                'calculated_items': calculated_items,
                'total_items': len(calculated_items),
                'total_value': sum(float(item.get('jewelry_price', 0)) for item in calculated_items)
            })
        else:
            # CSV形式で返す（既存の動作）
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
        return jsonify({'error': str(e)}), 500

# 計算結果をJSONで返すエンドポイント（DB保存用）
@app.route('/api/calculate-for-save', methods=['POST'])
@app.route('/calculate-for-save', methods=['POST'])
@token_required
def calculate_for_save():
    """計算結果をJSONで返す（DB保存専用）"""
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

        # 出力対象のカラムだけに制限
        output_columns = [
            'box_id', 'box_no', 'material', 'misc', 'weight',
            'jewelry_price', 'material_price', 'total_weight',
            'gemstone_weight', 'material_weight'
        ]
        result_df = result_df[[col for col in output_columns if col in result_df.columns]]

        # DataFrameを辞書のリストに変換
        calculated_items = result_df.to_dict('records')
        
        return jsonify({
            'calculated_items': calculated_items,
            'total_items': len(calculated_items),
            'total_value': sum(float(item.get('jewelry_price', 0)) for item in calculated_items)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 計算履歴保存エンドポイント
@app.route('/api/save-calculation', methods=['POST'])
@app.route('/save-calculation', methods=['POST'])
@token_required
def save_calculation():
    """計算結果をデータベースに保存"""
    try:
        print("=== Save Calculation API Called ===")
        data = request.json
        print(f"Request data: {data}")
        
        if not data:
            print("Error: No JSON provided")
            return jsonify({'error': 'No JSON provided'}), 400
        
        user_id = request.current_user.get('user_id')
        print(f"User ID: {user_id}")
        
        calculation_name = data.get('calculation_name', f"計算_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        item_data = data.get('item_data', [])
        calculation_results = data.get('calculation_results', {})
        
        print(f"Calculation name: {calculation_name}")
        print(f"Item data count: {len(item_data)}")
        print(f"Calculation results: {calculation_results}")
        
        if not item_data:
            print("Error: No item data provided")
            return jsonify({'error': 'アイテムデータが必要です'}), 400
        
        if not user_id:
            print("Error: No user_id in token")
            return jsonify({'error': 'ユーザーIDが見つかりません'}), 400
        
        print("Calling calculation_manager.save_calculation...")
        history_id = calculation_manager.save_calculation(
            user_id=user_id,
            calculation_name=calculation_name,
            item_data=item_data,
            calculation_results=calculation_results
        )
        
        print(f"Save result: history_id = {history_id}")
        
        if history_id:
            return jsonify({
                'message': '計算結果が保存されました',
                'history_id': history_id
            }), 201
        else:
            print("Error: calculation_manager.save_calculation returned None")
            return jsonify({'error': '計算結果の保存に失敗しました'}), 500
            
    except Exception as e:
        print(f"Exception in save_calculation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# 計算履歴一覧取得エンドポイント
@app.route('/api/calculation-history', methods=['GET'])
@app.route('/calculation-history', methods=['GET'])
@token_required
def get_calculation_history():
    """ユーザーの計算履歴一覧を取得"""
    try:
        user_id = request.current_user.get('user_id')
        limit = request.args.get('limit', 50, type=int)
        
        print(f"📋 計算履歴取得開始 - User ID: {user_id}, Limit: {limit}")
        histories = calculation_manager.get_calculation_history(user_id, limit)
        print(f"✅ 計算履歴取得完了 - 件数: {len(histories) if histories else 0}")
        return jsonify({'histories': histories})
        
    except Exception as e:
        print(f"❌ 計算履歴取得エラー: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# 計算履歴詳細取得エンドポイント
@app.route('/api/calculation-history/<int:history_id>', methods=['GET'])
@app.route('/calculation-history/<int:history_id>', methods=['GET'])
@token_required
def get_calculation_detail(history_id):
    """計算履歴の詳細を取得"""
    try:
        user_id = request.current_user.get('user_id')
        
        detail = calculation_manager.get_calculation_detail(history_id, user_id)
        if detail:
            return jsonify(detail)
        else:
            return jsonify({'error': '計算履歴が見つかりません'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 計算履歴削除エンドポイント
@app.route('/api/calculation-history/<int:history_id>', methods=['DELETE'])
@app.route('/calculation-history/<int:history_id>', methods=['DELETE'])
@token_required
def delete_calculation(history_id):
    """計算履歴を削除"""
    try:
        user_id = request.current_user.get('user_id')
        
        success = calculation_manager.delete_calculation(history_id, user_id)
        if success:
            return jsonify({'message': '計算履歴が削除されました'})
        else:
            return jsonify({'error': '計算履歴の削除に失敗しました'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 計算統計取得エンドポイント
@app.route('/api/calculation-stats', methods=['GET'])
@app.route('/calculation-stats', methods=['GET'])
@token_required
def get_calculation_stats():
    """ユーザーの計算統計を取得"""
    try:
        user_id = request.current_user.get('user_id')
        
        stats = calculation_manager.get_user_statistics(user_id)
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 管理者専用: 全DB内容確認
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
        from user_manager import DATABASE_PATH
        
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # テーブル一覧を取得
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        db_content = {}
        
        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            db_content[table] = [dict(row) for row in rows]
        
        conn.close()
        
        return jsonify({
            'tables': tables,
            'content': db_content,
            'database_path': DATABASE_PATH
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 管理者専用: SQLiteファイルをダウンロード
@app.route('/api/admin/download-db', methods=['GET'])
@app.route('/admin/download-db', methods=['GET'])
@token_required
def admin_download_db():
    """管理者専用: SQLiteデータベースファイルをダウンロード"""
    try:
        # 管理者権限チェック
        if request.current_user.get('role') != 'admin':
            return jsonify({'message': '管理者権限が必要です'}), 403
        
        from user_manager import DATABASE_PATH
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
        return jsonify({'error': str(e)}), 500

# 計算履歴からCSVエクスポート
@app.route('/api/export-calculation/<int:history_id>', methods=['GET'])
@app.route('/export-calculation/<int:history_id>', methods=['GET'])
@token_required
def export_calculation_csv(history_id):
    """計算履歴をCSVファイルとしてエクスポート"""
    try:
        user_id = request.current_user.get('user_id')
        
        detail = calculation_manager.get_calculation_detail(history_id, user_id)
        if not detail:
            return jsonify({'error': '計算履歴が見つかりません'}), 404
        
        # 計算データをDataFrameに変換
        item_data = detail['calculation_data']['items']
        df = pd.DataFrame(item_data)
        
        # 出力対象のカラムだけに制限
        output_columns = [
            'box_id', 'box_no', 'material', 'misc', 'weight',
            'jewelry_price', 'material_price', 'total_weight',
            'gemstone_weight', 'material_weight'
        ]
        df = df[[col for col in output_columns if col in df.columns]]
        
        # CSVをバイトストリームにして返す
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"{detail['calculation_name']}_{timestamp}.csv"
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 計算履歴のアイテム更新
@app.route('/api/calculation-history/<int:history_id>/item/<int:item_index>', methods=['PUT'])
@app.route('/calculation-history/<int:history_id>/item/<int:item_index>', methods=['PUT'])
@token_required
def update_calculation_item(history_id, item_index):
    """計算履歴の特定のアイテムを更新"""
    try:
        user_id = request.current_user.get('user_id')
        
        # 計算履歴の詳細を取得
        detail = calculation_manager.get_calculation_detail(history_id, user_id)
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
        
        # アイテムデータの更新
        items[item_index].update(update_data)
        
        # 価格の再計算（material_weight と material_price があれば）
        if 'material_weight' in update_data and 'material_price' in update_data:
            try:
                material_weight = float(update_data['material_weight'])
                material_price = float(update_data['material_price'])
                items[item_index]['jewelry_price'] = material_weight * material_price
            except (ValueError, TypeError):
                pass  # 計算できない場合はそのまま
        
        # データベースの更新
        calculation_manager.update_calculation_detail(history_id, user_id, detail['calculation_data'])
        
        return jsonify({'message': 'アイテムが更新されました', 'item': items[item_index]})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def serve_vue():
    return send_from_directory(app.static_folder, 'index.html')

# SPA用のcatch-allルート（Vue Routerの履歴管理対応）
@app.errorhandler(404)
def not_found(error):
    """404エラーハンドラー - Vue Router用のSPA対応"""
    # リクエストパスを取得
    path = request.path
    
    # APIルートの場合はJSONエラーを返す
    if path.startswith('/api/') or path.startswith('/api'):
        return jsonify({'error': 'API endpoint not found'}), 404
    
    # その他のルートの場合はindex.htmlを返す（Vue Routerに委ねる）
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print(f"✅ Starting Flask on port {port}")
    app.run(debug=False, host="0.0.0.0", port=port)