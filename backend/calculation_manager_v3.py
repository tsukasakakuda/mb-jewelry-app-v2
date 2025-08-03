"""
新しい3テーブル構造に対応した計算データマネージャー v3
- calculations テーブル: 計算セッション
- calculation_items テーブル: 個別アイテム
- calculation_summaries_view: 集計ビュー
"""

import sqlite3
import json
from datetime import datetime
import re
from typing import List, Dict, Optional, Any

DATABASE_PATH = 'users.db'

class CalculationManagerV3:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
    
    def _get_connection(self):
        """データベース接続を取得"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def normalize_box_id(self, box_id: Any) -> Optional[int]:
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
    
    def parse_weight(self, weight_text: Any) -> Optional[float]:
        """重量テキストから数値を抽出"""
        if not weight_text:
            return None
        try:
            weight_str = str(weight_text).strip()
            cleaned = re.sub(r'[^0-9.]', '', weight_str.split('g')[0])
            return float(cleaned) if cleaned else None
        except (ValueError, TypeError):
            return None
    
    def save_calculation(self, user_id: int, calculation_name: str, item_data: List[Dict], calculation_results: Dict = None) -> Optional[int]:
        """
        計算結果を新しい3テーブル構造に保存
        
        Args:
            user_id: ユーザーID
            calculation_name: 計算名
            item_data: アイテムデータのリスト
            calculation_results: 計算結果の追加情報
        
        Returns:
            作成された計算ID、失敗時はNone
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # calculationsテーブルに基本情報を挿入
            cursor.execute("""
                INSERT INTO calculations (user_id, calculation_name, description, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                user_id, 
                calculation_name,
                json.dumps(calculation_results, ensure_ascii=False) if calculation_results else None,
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            calculation_id = cursor.lastrowid
            
            # calculation_itemsテーブルにアイテムデータを挿入
            for item in item_data:
                box_id = self.normalize_box_id(item.get('box_id'))
                box_no = item.get('box_no')
                if box_no is not None:
                    try:
                        box_no = int(box_no)
                    except (ValueError, TypeError):
                        box_no = None
                
                weight_grams = self.parse_weight(item.get('weight'))
                
                cursor.execute("""
                    INSERT INTO calculation_items (
                        calculation_id, box_id, box_no, material, weight_text, weight_grams,
                        misc, jewelry_price, material_price, total_weight,
                        gemstone_weight, material_weight, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    calculation_id,
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
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            print(f"✅ 計算データ保存完了: ID {calculation_id}, {len(item_data)}アイテム")
            return calculation_id
            
        except Exception as e:
            conn.rollback()
            print(f"❌ 計算データ保存エラー: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            conn.close()
    
    def get_calculation_history(self, user_id: int, limit: int = 50) -> List[Dict]:
        """
        ユーザーの計算履歴一覧を取得（集計情報付き）
        
        Args:
            user_id: ユーザーID
            limit: 取得件数制限
        
        Returns:
            計算履歴のリスト
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    c.id,
                    c.calculation_name,
                    c.created_at,
                    COALESCE(s.total_items, 0) as item_count,
                    COALESCE(s.total_value, 0) as total_value,
                    COALESCE(s.total_weight, 0) as total_weight,
                    COALESCE(s.unique_boxes, 0) as unique_boxes
                FROM calculations c
                LEFT JOIN calculation_summaries_view s ON c.id = s.calculation_id
                WHERE c.user_id = ?
                ORDER BY c.created_at DESC
                LIMIT ?
            """, (user_id, limit))
            
            histories = []
            for row in cursor.fetchall():
                histories.append({
                    'id': row['id'],
                    'calculation_name': row['calculation_name'],
                    'created_at': row['created_at'],
                    'item_count': row['item_count'],
                    'total_value': row['total_value'],
                    'total_weight': row['total_weight'],
                    'unique_boxes': row['unique_boxes']
                })
            
            return histories
            
        except Exception as e:
            print(f"❌ 計算履歴取得エラー: {e}")
            return []
        finally:
            conn.close()
    
    def get_calculation_detail(self, calculation_id: int, user_id: int) -> Optional[Dict]:
        """
        計算履歴の詳細情報を取得
        
        Args:
            calculation_id: 計算ID
            user_id: ユーザーID
        
        Returns:
            計算詳細データ、見つからない場合はNone
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # 基本情報を取得
            cursor.execute("""
                SELECT 
                    c.id,
                    c.calculation_name,
                    c.description,
                    c.created_at,
                    s.total_items,
                    s.total_value,
                    s.total_weight,
                    s.unique_boxes,
                    s.average_item_value
                FROM calculations c
                LEFT JOIN calculation_summaries_view s ON c.id = s.calculation_id
                WHERE c.id = ? AND c.user_id = ?
            """, (calculation_id, user_id))
            
            calc_row = cursor.fetchone()
            if not calc_row:
                return None
            
            # アイテム情報を取得
            cursor.execute("""
                SELECT *
                FROM calculation_items
                WHERE calculation_id = ?
                ORDER BY box_id, box_no
            """, (calculation_id,))
            
            items = []
            for item_row in cursor.fetchall():
                items.append({
                    'id': item_row['id'],
                    'box_id': item_row['box_id'],
                    'box_no': item_row['box_no'],
                    'material': item_row['material'],
                    'weight': item_row['weight_text'],
                    'weight_text': item_row['weight_text'],
                    'weight_grams': item_row['weight_grams'],
                    'misc': item_row['misc'],
                    'jewelry_price': item_row['jewelry_price'],
                    'material_price': item_row['material_price'],
                    'total_weight': item_row['total_weight'],
                    'gemstone_weight': item_row['gemstone_weight'],
                    'material_weight': item_row['material_weight'],
                    'brand_name': item_row['brand_name'],
                    'subcategory_name': item_row['subcategory_name'],
                    'accessory_comment': item_row['accessory_comment'],
                    'budget_lower': item_row['budget_lower'],
                    'budget_upper': item_row['budget_upper'],
                    'budget_reserve': item_row['budget_reserve'],
                    'frame_price': item_row['frame_price'],
                    'side_stone_price': item_row['side_stone_price'],
                    'live': item_row['live'],
                    'rank': item_row['rank'],
                    'created_at': item_row['created_at']
                })
            
            # 旧形式と互換性のあるレスポンス構造
            result = {
                'id': calc_row['id'],
                'calculation_name': calc_row['calculation_name'],
                'created_at': calc_row['created_at'],
                'item_count': calc_row['total_items'] or 0,
                'total_value': calc_row['total_value'] or 0,
                'total_weight': calc_row['total_weight'] or 0,
                'unique_boxes': calc_row['unique_boxes'] or 0,
                'calculation_data': {
                    'items': items,
                    'results': {
                        'total_value': calc_row['total_value'] or 0,
                        'item_count': calc_row['total_items'] or 0
                    },
                    'summary': {
                        'item_count': calc_row['total_items'] or 0,
                        'total_value': calc_row['total_value'] or 0,
                        'total_weight': calc_row['total_weight'] or 0,
                        'unique_boxes': calc_row['unique_boxes'] or 0,
                        'average_item_value': calc_row['average_item_value'] or 0
                    }
                }
            }
            
            return result
            
        except Exception as e:
            print(f"❌ 計算詳細取得エラー: {e}")
            return None
        finally:
            conn.close()
    
    def update_calculation_detail(self, calculation_id: int, user_id: int, calculation_data: Dict) -> bool:
        """
        計算データの更新（互換性のため）
        
        Args:
            calculation_id: 計算ID
            user_id: ユーザーID
            calculation_data: 更新するデータ
        
        Returns:
            更新成功時True
        """
        # TODO: 新構造での部分更新実装
        print(f"⚠️ 計算データ更新は新構造で再実装が必要です: {calculation_id}")
        return False
    
    def delete_calculation(self, calculation_id: int, user_id: int) -> bool:
        """
        計算履歴を削除
        
        Args:
            calculation_id: 計算ID
            user_id: ユーザーID
        
        Returns:
            削除成功時True
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # 権限確認
            cursor.execute("""
                SELECT id FROM calculations WHERE id = ? AND user_id = ?
            """, (calculation_id, user_id))
            
            if not cursor.fetchone():
                return False
            
            # CASCADE制約により関連アイテムも自動削除される
            cursor.execute("""
                DELETE FROM calculations WHERE id = ? AND user_id = ?
            """, (calculation_id, user_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            conn.rollback()
            print(f"❌ 計算履歴削除エラー: {e}")
            return False
        finally:
            conn.close()
    
    def get_user_statistics(self, user_id: int) -> Dict:
        """
        ユーザーの統計情報を取得
        
        Args:
            user_id: ユーザーID
        
        Returns:
            統計情報
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT c.id) as total_calculations,
                    COUNT(DISTINCT ci.id) as total_items,
                    COALESCE(SUM(ci.jewelry_price), 0) as total_value,
                    MAX(c.created_at) as last_calculation
                FROM calculations c
                LEFT JOIN calculation_items ci ON c.id = ci.calculation_id
                WHERE c.user_id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            
            return {
                'total_calculations': row['total_calculations'] or 0,
                'total_items': row['total_items'] or 0,
                'total_value': row['total_value'] or 0,
                'last_calculation': row['last_calculation']
            }
            
        except Exception as e:
            print(f"❌ 統計情報取得エラー: {e}")
            return {
                'total_calculations': 0,
                'total_items': 0,
                'total_value': 0,
                'last_calculation': None
            }
        finally:
            conn.close()
    
    def get_box_groups(self, user_id: int, max_per_box: int = 10) -> Dict:
        """
        箱番号別のグループ化データを取得（最適化版）
        
        Args:
            user_id: ユーザーID
            max_per_box: 箱ごとの最大取得数
        
        Returns:
            箱番号別グループデータ
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # 各箱ごとに最新のアイテムを取得
            cursor.execute("""
                SELECT 
                    ci.box_id,
                    c.id as calculation_id,
                    c.calculation_name,
                    c.created_at,
                    ci.id as item_id,
                    ci.box_no,
                    ci.material,
                    ci.weight_text as weight,
                    ci.jewelry_price,
                    ci.material_price,
                    ci.total_weight,
                    ci.gemstone_weight,
                    ci.material_weight,
                    ci.misc,
                    ROW_NUMBER() OVER (PARTITION BY ci.box_id ORDER BY c.created_at DESC, ci.id DESC) as rn
                FROM calculation_items ci
                JOIN calculations c ON ci.calculation_id = c.id
                WHERE c.user_id = ? AND ci.box_id IS NOT NULL
            """, (user_id,))
            
            box_groups = {}
            for row in cursor.fetchall():
                if row['rn'] <= max_per_box:  # 最大件数制限
                    box_id = str(row['box_id'])  # 文字列として統一
                    
                    if box_id not in box_groups:
                        box_groups[box_id] = []
                    
                    box_groups[box_id].append({
                        'history_id': row['calculation_id'],
                        'calculation_name': row['calculation_name'],
                        'created_at': row['created_at'],
                        'item': {
                            'id': row['item_id'],
                            'box_id': row['box_id'],
                            'box_no': row['box_no'],
                            'material': row['material'],
                            'weight': row['weight'],
                            'jewelry_price': row['jewelry_price'],
                            'material_price': row['material_price'],
                            'total_weight': row['total_weight'],
                            'gemstone_weight': row['gemstone_weight'],
                            'material_weight': row['material_weight'],
                            'misc': row['misc']
                        }
                    })
            
            # 箱番号でソート
            sorted_box_ids = sorted(box_groups.keys(), key=lambda x: int(x) if x.isdigit() else 999999)
            sorted_groups = {box_id: box_groups[box_id] for box_id in sorted_box_ids}
            
            return sorted_groups
            
        except Exception as e:
            print(f"❌ 箱グループ取得エラー: {e}")
            import traceback
            traceback.print_exc()
            return {}
        finally:
            conn.close()
    
    def get_box_groups_by_calculation(self, calculation_id: int, user_id: int) -> Dict:
        """
        特定の計算履歴内で箱番号別のグループ化データを取得
        
        Args:
            calculation_id: 計算履歴ID
            user_id: ユーザーID
        
        Returns:
            箱番号別グループデータ
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # 指定された計算履歴内のアイテムを箱番号でグループ化（全フィールド取得）
            cursor.execute("""
                SELECT 
                    ci.box_id,
                    c.id as calculation_id,
                    c.calculation_name,
                    c.created_at,
                    ci.id as item_id,
                    ci.box_no,
                    ci.material,
                    ci.weight_text as weight,
                    ci.weight_grams,
                    ci.jewelry_price,
                    ci.material_price,
                    ci.total_weight,
                    ci.gemstone_weight,
                    ci.material_weight,
                    ci.misc,
                    ci.brand_name,
                    ci.subcategory_name,
                    ci.accessory_comment,
                    ci.budget_lower,
                    ci.budget_upper,
                    ci.budget_reserve,
                    ci.frame_price,
                    ci.side_stone_price,
                    ci.live,
                    ci.rank
                FROM calculation_items ci
                JOIN calculations c ON ci.calculation_id = c.id
                WHERE c.id = ? AND c.user_id = ? AND ci.box_id IS NOT NULL
                ORDER BY ci.box_id, ci.box_no
            """, (calculation_id, user_id))
            
            box_groups = {}
            for row in cursor.fetchall():
                box_id = str(row['box_id'])  # 文字列として統一
                
                if box_id not in box_groups:
                    box_groups[box_id] = []
                
                box_groups[box_id].append({
                    'history_id': row['calculation_id'],
                    'calculation_name': row['calculation_name'],
                    'created_at': row['created_at'],
                    'item': {
                        'id': row['item_id'],
                        'box_id': row['box_id'],
                        'box_no': row['box_no'],
                        'material': row['material'],
                        'weight': row['weight'],
                        'weight_text': row['weight'],
                        'weight_grams': row['weight_grams'],
                        'jewelry_price': row['jewelry_price'],
                        'material_price': row['material_price'],
                        'total_weight': row['total_weight'],
                        'gemstone_weight': row['gemstone_weight'],
                        'material_weight': row['material_weight'],
                        'misc': row['misc'],
                        'brand_name': row['brand_name'],
                        'subcategory_name': row['subcategory_name'],
                        'accessory_comment': row['accessory_comment'],
                        'budget_lower': row['budget_lower'],
                        'budget_upper': row['budget_upper'],
                        'budget_reserve': row['budget_reserve'],
                        'frame_price': row['frame_price'],
                        'side_stone_price': row['side_stone_price'],
                        'live': row['live'],
                        'rank': row['rank']
                    }
                })
            
            # 箱番号でソート
            sorted_box_ids = sorted(box_groups.keys(), key=lambda x: int(x) if x.isdigit() else 999999)
            sorted_groups = {box_id: box_groups[box_id] for box_id in sorted_box_ids}
            
            return sorted_groups
            
        except Exception as e:
            print(f"❌ 特定計算履歴内箱グループ取得エラー: {e}")
            import traceback
            traceback.print_exc()
            return {}
        finally:
            conn.close()
    
    def update_calculation_item(self, calculation_id: int, item_id: int, user_id: int, update_data: Dict) -> bool:
        """
        計算アイテムを更新
        
        Args:
            calculation_id: 計算ID
            item_id: アイテムID
            user_id: ユーザーID
            update_data: 更新データ
        
        Returns:
            更新成功時True
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # 権限確認：計算がユーザーのものかチェック
            cursor.execute("""
                SELECT c.id FROM calculations c
                JOIN calculation_items ci ON c.id = ci.calculation_id
                WHERE c.id = ? AND c.user_id = ? AND ci.id = ?
            """, (calculation_id, user_id, item_id))
            
            if not cursor.fetchone():
                return False
            
            # 更新可能なフィールドを定義（実際のDBカラムに合わせる）
            allowed_fields = [
                'box_id', 'box_no', 'material', 'weight_text', 'weight_grams',
                'jewelry_price', 'material_price', 'total_weight',
                'gemstone_weight', 'material_weight', 'misc',
                'brand_name', 'subcategory_name', 'accessory_comment',
                'budget_lower', 'budget_upper', 'budget_reserve',
                'frame_price', 'side_stone_price', 'live', 'rank'
            ]
            
            # 更新データをフィルタリング
            filtered_data = {k: v for k, v in update_data.items() if k in allowed_fields}
            
            print(f"🔍 Original update_data: {update_data}")
            print(f"🔍 Filtered data: {filtered_data}")
            
            if not filtered_data:
                print("❌ フィルタリング後のデータが空です")
                return False
            
            # SQL構築
            set_clauses = []
            values = []
            for field, value in filtered_data.items():
                set_clauses.append(f"{field} = ?")
                values.append(value)
            
            values.append(item_id)
            
            update_sql = f"""
                UPDATE calculation_items 
                SET {', '.join(set_clauses)}
                WHERE id = ?
            """
            
            print(f"🔍 Executing SQL: {update_sql}")
            print(f"🔍 With values: {values}")
            
            cursor.execute(update_sql, values)
            conn.commit()
            
            updated_rows = cursor.rowcount
            print(f"🔍 Updated rows: {updated_rows}")
            
            return updated_rows > 0
            
        except Exception as e:
            conn.rollback()
            print(f"❌ アイテム更新エラー: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            conn.close()

# シングルトンインスタンス
calculation_manager_v3 = CalculationManagerV3()