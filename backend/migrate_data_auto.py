#!/usr/bin/env python3
"""
データベース移行スクリプト（自動実行版）
旧構造から新3テーブル構造への一括移行
"""

import sqlite3
import json
import re
from datetime import datetime
import traceback

DATABASE_PATH = 'users.db'

def normalize_box_id(box_id):
    """box_idを統一されたINTEGER形式に正規化"""
    if box_id is None:
        return None
    try:
        if isinstance(box_id, (int, float)):
            return int(box_id)
        elif isinstance(box_id, str):
            if box_id.strip().isdigit():
                return int(box_id.strip())
            else:
                # 数字以外の文字列の場合、ハッシュ値を使用
                return hash(box_id) % 999999
        else:
            return hash(str(box_id)) % 999999
    except (ValueError, TypeError):
        return None

def parse_weight(weight_text):
    """重量テキストから数値を抽出"""
    if not weight_text:
        return None
    try:
        # "11.3g" や "11.3" から数値部分を抽出
        weight_str = str(weight_text).strip()
        cleaned = re.sub(r'[^0-9.]', '', weight_str.split('g')[0])
        return float(cleaned) if cleaned else None
    except (ValueError, TypeError):
        return None

def migrate_database():
    """データベース移行のメイン処理"""
    print("🚀 データベース移行を開始します...")
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # 新スキーマの読み込みと実行
        print("📋 新しいスキーマを作成中...")
        with open('migration_schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # SQLファイルを文ごとに分割して実行
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        for statement in statements:
            try:
                cursor.execute(statement)
            except sqlite3.Error as e:
                print(f"⚠️ スキーマ実行警告: {e}")
                print(f"   SQL: {statement[:100]}...")
        
        print("✅ 新しいスキーマを作成完了")
        
        # ユーザーデータの移行
        print("👥 ユーザーデータを移行中...")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        for user in users:
            updated_at = user['updated_at'] if 'updated_at' in user.keys() else user['created_at']
            cursor.execute("""
                INSERT INTO users_new (id, username, password_hash, email, role, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user['id'], user['username'], user['password_hash'], 
                user['email'], user['role'], user['is_active'],
                user['created_at'], updated_at
            ))
        
        print(f"✅ {len(users)}件のユーザーデータを移行完了")
        
        # 計算履歴データの移行
        print("📊 計算履歴データを移行中...")
        cursor.execute("SELECT * FROM calculation_history ORDER BY id")
        histories = cursor.fetchall()
        
        total_items_migrated = 0
        
        for history in histories:
            print(f"📄 処理中: ID {history['id']} - {history['calculation_name']}")
            
            # calculationsテーブルに基本情報を挿入
            item_count = history['item_count'] if 'item_count' in history.keys() else 0
            total_value = history['total_value'] if 'total_value' in history.keys() else 0
            cursor.execute("""
                INSERT INTO calculations_new (id, user_id, calculation_name, description, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                history['id'], history['user_id'], history['calculation_name'],
                f"Migrated from old system. Original item_count: {item_count}, total_value: {total_value}",
                history['created_at'], history['created_at']
            ))
            
            # JSONデータの解析とアイテム移行
            if history['calculation_data']:
                try:
                    calc_data = json.loads(history['calculation_data'])
                    items = calc_data.get('items', [])
                    
                    for item in items:
                        # データの正規化
                        box_id = normalize_box_id(item.get('box_id'))
                        box_no = item.get('box_no')
                        if box_no is not None:
                            try:
                                box_no = int(box_no)
                            except (ValueError, TypeError):
                                box_no = None
                        
                        weight_grams = parse_weight(item.get('weight'))
                        
                        # calculation_itemsテーブルに挿入
                        cursor.execute("""
                            INSERT INTO calculation_items_new (
                                calculation_id, box_id, box_no, material, weight_text, weight_grams,
                                misc, jewelry_price, material_price, total_weight, 
                                gemstone_weight, material_weight, created_at
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            history['id'],
                            box_id,
                            box_no,
                            item.get('material'),
                            str(item.get('weight', '')) if item.get('weight') else None,
                            weight_grams,
                            item.get('misc'),
                            item.get('jewelry_price'),
                            item.get('material_price'),
                            item.get('total_weight'),
                            item.get('gemstone_weight'),
                            item.get('material_weight'),
                            history['created_at']
                        ))
                        total_items_migrated += 1
                
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析エラー (ID: {history['id']}): {e}")
                except Exception as e:
                    print(f"❌ アイテム移行エラー (ID: {history['id']}): {e}")
                    traceback.print_exc()
        
        print(f"✅ {len(histories)}件の計算履歴と{total_items_migrated}個のアイテムを移行完了")
        
        # データ整合性の確認
        print("🔍 データ整合性を確認中...")
        
        # ユーザー数の確認
        cursor.execute("SELECT COUNT(*) FROM users")
        old_user_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM users_new")
        new_user_count = cursor.fetchone()[0]
        
        # 計算履歴数の確認
        cursor.execute("SELECT COUNT(*) FROM calculation_history")
        old_calc_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM calculations_new")
        new_calc_count = cursor.fetchone()[0]
        
        # アイテム数の確認（サンプル）
        cursor.execute("SELECT COUNT(*) FROM calculation_items_new")
        new_item_count = cursor.fetchone()[0]
        
        print(f"📊 移行結果:")
        print(f"   ユーザー: {old_user_count} → {new_user_count}")
        print(f"   計算履歴: {old_calc_count} → {new_calc_count}")
        print(f"   アイテム: ? → {new_item_count}")
        
        if old_user_count == new_user_count and old_calc_count == new_calc_count:
            print("✅ データ整合性チェック完了")
        else:
            print("⚠️ データ数に差異があります")
        
        # 集計テストの実行
        print("🧪 集計機能のテスト中...")
        cursor.execute("""
            SELECT c.calculation_name, s.total_items, s.total_value, s.unique_boxes
            FROM calculations_new c
            LEFT JOIN calculation_summaries_view s ON c.id = s.calculation_id
            ORDER BY c.id
            LIMIT 3
        """)
        sample_summaries = cursor.fetchall()
        
        for summary in sample_summaries:
            print(f"   📈 {summary[0]}: {summary[1]}アイテム, ¥{summary[2]:.0f}, {summary[3]}箱")
        
        conn.commit()
        print("✅ 移行処理が正常に完了しました")
        
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 移行処理でエラーが発生しました: {e}")
        traceback.print_exc()
        return False
    
    finally:
        conn.close()

def backup_old_tables():
    """旧テーブルのバックアップ"""
    print("💾 旧テーブルをバックアップ中...")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # 旧テーブルをバックアップ用にリネーム
        cursor.execute("ALTER TABLE users RENAME TO users_backup")
        cursor.execute("ALTER TABLE calculation_history RENAME TO calculation_history_backup")
        
        conn.commit()
        print("✅ 旧テーブルのバックアップ完了")
        
    except sqlite3.Error as e:
        print(f"❌ バックアップエラー: {e}")
        conn.rollback()
        raise
    
    finally:
        conn.close()

def finalize_migration():
    """移行の最終処理"""
    print("🎯 移行の最終処理中...")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # 新テーブルを正式名称にリネーム
        cursor.execute("ALTER TABLE users_new RENAME TO users")
        cursor.execute("ALTER TABLE calculations_new RENAME TO calculations")
        cursor.execute("ALTER TABLE calculation_items_new RENAME TO calculation_items")
        
        # VIEWを再作成（テーブル名変更のため）
        cursor.execute("DROP VIEW IF EXISTS calculation_summaries_view")
        cursor.execute("""
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
            FROM calculation_items
            GROUP BY calculation_id
        """)
        
        conn.commit()
        print("✅ 移行の最終処理完了")
        
    except sqlite3.Error as e:
        print(f"❌ 最終処理エラー: {e}")
        conn.rollback()
        raise
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 データベース一括移行スクリプト（自動実行）")
    print("=" * 50)
    
    try:
        # ステップ1: データ移行
        if migrate_database():
            # ステップ2: 旧テーブルのバックアップ
            backup_old_tables()
            
            # ステップ3: 最終処理
            finalize_migration()
            
            print("\n🎉 データベース移行が正常に完了しました！")
            print("📋 新しい構造:")
            print("   - users: ユーザー管理")
            print("   - calculations: 計算セッション")
            print("   - calculation_items: 個別アイテム")
            print("   - calculation_summaries_view: 集計ビュー")
            
        else:
            print("❌ 移行に失敗しました")
            
    except Exception as e:
        print(f"\n💥 予期しないエラーが発生しました: {e}")
        traceback.print_exc()