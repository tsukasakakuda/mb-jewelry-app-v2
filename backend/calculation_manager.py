"""
計算履歴管理モジュール
地金計算結果のデータベース保存・取得機能を提供
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Optional, Dict, List
from user_manager import DATABASE_PATH

class CalculationManager:
    """計算履歴管理クラス"""
    
    def __init__(self):
        self.db_path = DATABASE_PATH
    
    def _get_connection(self):
        """データベース接続を取得"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 辞書形式でアクセス可能
        return conn
    
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
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # 計算データをJSON形式で保存
            calculation_data = {
                'items': item_data,
                'results': calculation_results,
                'summary': {
                    'item_count': len(item_data),
                    'total_value': sum(item.get('jewelry_price', 0) for item in item_data),
                    'total_weight': sum(item.get('total_weight', 0) for item in item_data)
                }
            }
            
            cursor.execute('''
                INSERT INTO calculation_history 
                (user_id, calculation_name, item_count, total_value, calculation_data, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                user_id,
                calculation_name,
                calculation_data['summary']['item_count'],
                calculation_data['summary']['total_value'],
                json.dumps(calculation_data, ensure_ascii=False, indent=2)
            ))
            
            history_id = cursor.lastrowid
            conn.commit()
            
            print(f"✅ 計算結果を保存しました (ID: {history_id})")
            return history_id
            
        except Exception as e:
            print(f"計算結果保存エラー: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def get_calculation_history(self, user_id: int, limit: int = 50) -> List[Dict]:
        """
        ユーザーの計算履歴を取得
        
        Args:
            user_id: ユーザーID
            limit: 取得件数制限
            
        Returns:
            計算履歴のリスト
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, calculation_name, item_count, total_value, created_at
                FROM calculation_history
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            histories = cursor.fetchall()
            return [dict(history) for history in histories]
            
        except Exception as e:
            print(f"計算履歴取得エラー: {e}")
            return []
        finally:
            conn.close()
    
    def get_calculation_detail(self, history_id: int, user_id: int) -> Optional[Dict]:
        """
        計算履歴の詳細を取得
        
        Args:
            history_id: 計算履歴ID
            user_id: ユーザーID（権限確認用）
            
        Returns:
            計算履歴の詳細データ
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, calculation_name, item_count, total_value, calculation_data, created_at
                FROM calculation_history
                WHERE id = ? AND user_id = ?
            ''', (history_id, user_id))
            
            history = cursor.fetchone()
            if not history:
                return None
            
            result = dict(history)
            # JSON文字列をパース
            result['calculation_data'] = json.loads(result['calculation_data'])
            
            return result
            
        except Exception as e:
            print(f"計算履歴詳細取得エラー: {e}")
            return None
        finally:
            conn.close()
    
    def delete_calculation(self, history_id: int, user_id: int) -> bool:
        """
        計算履歴を削除
        
        Args:
            history_id: 計算履歴ID
            user_id: ユーザーID（権限確認用）
            
        Returns:
            削除成功時True、失敗時False
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                DELETE FROM calculation_history
                WHERE id = ? AND user_id = ?
            ''', (history_id, user_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"✅ 計算履歴を削除しました (ID: {history_id})")
                return True
            
            return False
            
        except Exception as e:
            print(f"計算履歴削除エラー: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_user_statistics(self, user_id: int) -> Dict:
        """
        ユーザーの計算統計を取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            計算統計データ
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_calculations,
                    SUM(item_count) as total_items,
                    SUM(total_value) as total_value,
                    MAX(created_at) as last_calculation
                FROM calculation_history
                WHERE user_id = ?
            ''', (user_id,))
            
            stats = cursor.fetchone()
            return dict(stats) if stats else {}
            
        except Exception as e:
            print(f"計算統計取得エラー: {e}")
            return {}
        finally:
            conn.close()

# シングルトンインスタンス
calculation_manager = CalculationManager()