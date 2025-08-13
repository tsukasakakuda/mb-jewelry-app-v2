"""
計算履歴管理モジュール v2
db_manager を使用した Cloud SQL 対応版
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, List
from db_manager import db_manager

class CalculationManager:
    """計算履歴管理クラス（Cloud SQL対応）"""
    
    def __init__(self):
        self.db = db_manager
    
    def save_calculation(self, user_id: int, calculation_name: str, 
                        item_data: List[Dict], calculation_results: Dict) -> Optional[int]:
        """
        計算結果をデータベースに保存
        
        Args:
            user_id: ユーザーID
            calculation_name: 計算名
            item_data: 計算対象のアイテムデータ
            calculation_results: 計算結果
            
        Returns:
            保存された計算履歴ID、エラー時はNone
        """
        try:
            print(f"📊 Saving calculation for user {user_id}: {calculation_name}")
            print(f"📋 Item count: {len(item_data)}")
            print(f"💰 Results: {calculation_results}")
            
            # 計算データをJSON形式で保存
            calculation_data = {
                'items': item_data,
                'results': calculation_results,
                'summary': {
                    'total_value': calculation_results.get('total_value', 0),
                    'total_weight': sum(self._parse_weight(item.get('weight', 0)) for item in item_data),
                    'item_count': len(item_data)
                }
            }
            
            calculation_data_json = json.dumps(calculation_data, ensure_ascii=False)
            total_value = calculation_results.get('total_value', 0)
            item_count = len(item_data)
            
            placeholder = self.db.get_sql_placeholder()
            
            if self.db.db_type == 'postgresql':
                query = f"""
                INSERT INTO calculation_history 
                (user_id, calculation_name, calculation_data, total_value, item_count)
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
                RETURNING id
                """
            else:
                query = f"""
                INSERT INTO calculation_history 
                (user_id, calculation_name, calculation_data, total_value, item_count)
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
                """
            
            history_id = self.db.execute_insert(
                query,
                (user_id, calculation_name, calculation_data_json, total_value, item_count)
            )
            
            if history_id:
                print(f"✅ 計算履歴を保存しました (ID: {history_id})")
                return history_id
            
            return None
            
        except Exception as e:
            print(f"計算履歴保存エラー: {e}")
            return None
    
    def get_calculation_history(self, user_id: int, limit: int = 50) -> List[Dict]:
        """
        ユーザーの計算履歴を取得（API互換性のためのエイリアス）
        
        Args:
            user_id: ユーザーID
            limit: 取得件数制限
            
        Returns:
            計算履歴のリスト
        """
        try:
            placeholder = self.db.get_sql_placeholder()
            histories = self.db.execute_query(f"""
                SELECT id, calculation_name, total_value, item_count, created_at
                FROM calculation_history
                WHERE user_id = {placeholder}
                ORDER BY created_at DESC
                LIMIT {placeholder}
            """, (user_id, limit))
            
            result = []
            for history in histories or []:
                result.append({
                    'id': history['id'],
                    'calculation_name': history['calculation_name'],
                    'total_value': float(history['total_value']) if history['total_value'] else 0,
                    'item_count': history['item_count'],
                    'created_at': history['created_at']
                })
            
            print(f"✅ 計算履歴を取得しました (User: {user_id}, 件数: {len(result)}, Limit: {limit})")
            return result
            
        except Exception as e:
            print(f"計算履歴取得エラー: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_user_histories(self, user_id: int) -> List[Dict]:
        """
        ユーザーの計算履歴リストを取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            計算履歴のリスト
        """
        try:
            placeholder = self.db.get_sql_placeholder()
            histories = self.db.execute_query(f"""
                SELECT id, calculation_name, total_value, item_count, created_at
                FROM calculation_history
                WHERE user_id = {placeholder}
                ORDER BY created_at DESC
            """, (user_id,))
            
            result = []
            for history in histories or []:
                result.append({
                    'id': history['id'],
                    'calculation_name': history['calculation_name'],
                    'total_value': float(history['total_value']) if history['total_value'] else 0,
                    'item_count': history['item_count'],
                    'created_at': history['created_at']
                })
            
            print(f"📋 Found {len(result)} calculation histories for user {user_id}")
            return result
            
        except Exception as e:
            print(f"計算履歴取得エラー: {e}")
            return []
    
    def get_calculation_detail(self, history_id: int, user_id: int) -> Optional[Dict]:
        """
        計算履歴の詳細を取得
        
        Args:
            history_id: 計算履歴ID
            user_id: ユーザーID（権限確認用）
            
        Returns:
            計算履歴の詳細データ、見つからない場合はNone
        """
        try:
            placeholder = self.db.get_sql_placeholder()
            histories = self.db.execute_query(f"""
                SELECT id, calculation_name, calculation_data, total_value, item_count, created_at
                FROM calculation_history
                WHERE id = {placeholder} AND user_id = {placeholder}
            """, (history_id, user_id))
            
            if not histories:
                print(f"⚠️ 計算履歴が見つかりません (ID: {history_id}, User: {user_id})")
                return None
            
            history = histories[0]
            calculation_data = json.loads(history['calculation_data'])
            
            result = {
                'id': history['id'],
                'calculation_name': history['calculation_name'],
                'calculation_data': calculation_data,
                'total_value': float(history['total_value']) if history['total_value'] else 0,
                'item_count': history['item_count'],
                'created_at': history['created_at']
            }
            
            print(f"✅ 計算履歴詳細を取得しました (ID: {history_id})")
            return result
            
        except Exception as e:
            print(f"計算履歴詳細取得エラー: {e}")
            return None
    
    def update_calculation_detail(self, history_id: int, user_id: int, calculation_data: Dict) -> bool:
        """
        計算履歴の詳細データを更新
        
        Args:
            history_id: 計算履歴ID
            user_id: ユーザーID（権限確認用）
            calculation_data: 更新する計算データ
            
        Returns:
            更新成功時True、失敗時False
        """
        try:
            # データをJSON文字列に変換
            calculation_data_json = json.dumps(calculation_data, ensure_ascii=False)
            
            # 新しい合計値とアイテム数を計算
            items = calculation_data.get('items', [])
            total_value = sum(float(item.get('jewelry_price', 0)) for item in items)
            item_count = len(items)
            
            placeholder = self.db.get_sql_placeholder()
            affected_rows = self.db.execute_query(f"""
                UPDATE calculation_history
                SET calculation_data = {placeholder}, total_value = {placeholder}, item_count = {placeholder}
                WHERE id = {placeholder} AND user_id = {placeholder}
            """, (calculation_data_json, total_value, item_count, history_id, user_id))
            
            if affected_rows > 0:
                print(f"✅ 計算履歴の詳細を更新しました (ID: {history_id})")
                return True
            
            return False
            
        except Exception as e:
            print(f"計算履歴詳細更新エラー: {e}")
            return False
    
    def delete_calculation(self, history_id: int, user_id: int) -> bool:
        """
        計算履歴を削除
        
        Args:
            history_id: 計算履歴ID
            user_id: ユーザーID（権限確認用）
            
        Returns:
            削除成功時True、失敗時False
        """
        try:
            placeholder = self.db.get_sql_placeholder()
            affected_rows = self.db.execute_query(f"""
                DELETE FROM calculation_history
                WHERE id = {placeholder} AND user_id = {placeholder}
            """, (history_id, user_id))
            
            if affected_rows > 0:
                print(f"✅ 計算履歴を削除しました (ID: {history_id})")
                return True
            
            return False
            
        except Exception as e:
            print(f"計算履歴削除エラー: {e}")
            return False
    
    def get_user_statistics(self, user_id: int) -> Dict:
        """
        ユーザーの計算統計を取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            統計情報の辞書
        """
        try:
            placeholder = self.db.get_sql_placeholder()
            
            # 総計算数と総評価額を取得
            stats = self.db.execute_query(f"""
                SELECT 
                    COUNT(*) as total_calculations,
                    COALESCE(SUM(total_value), 0) as total_value,
                    COALESCE(SUM(item_count), 0) as total_items
                FROM calculation_history
                WHERE user_id = {placeholder}
            """, (user_id,))
            
            if stats:
                stat = stats[0]
                result = {
                    'total_calculations': stat['total_calculations'],
                    'total_value': float(stat['total_value']),
                    'total_items': stat['total_items']
                }
            else:
                result = {
                    'total_calculations': 0,
                    'total_value': 0.0,
                    'total_items': 0
                }
            
            print(f"📊 ユーザー統計を取得しました (User: {user_id}): {result}")
            return result
            
        except Exception as e:
            print(f"ユーザー統計取得エラー: {e}")
            return {
                'total_calculations': 0,
                'total_value': 0.0,
                'total_items': 0
            }
    
    def _parse_weight(self, weight_value) -> float:
        """
        重量値を安全にfloatに変換
        
        Args:
            weight_value: 重量値（文字列または数値）
            
        Returns:
            float形式の重量値
        """
        try:
            if isinstance(weight_value, (int, float)):
                return float(weight_value)
            elif isinstance(weight_value, str):
                # 文字列から数値部分を抽出（例: '11.3g' -> 11.3）
                import re
                match = re.search(r'(\d+\.?\d*)', weight_value)
                if match:
                    return float(match.group(1))
                else:
                    return 0.0
            else:
                return 0.0
        except (ValueError, TypeError):
            print(f"⚠️ 重量値の変換に失敗しました: {weight_value}")
            return 0.0