#!/usr/bin/env python3
"""
ローカル開発環境用データベース初期化スクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/backend')

from user_manager import user_manager
import json

def init_database():
    """データベースとテストデータを初期化"""
    print("🔧 ローカルデータベースを初期化中...")
    
    # 管理者ユーザーを作成
    try:
        # 既存ユーザーをチェック
        existing_user = user_manager.authenticate_user('admin', 'admin123')
        if existing_user:
            print("✅ 管理者ユーザーは既に存在します")
        else:
            # 新規作成
            user_id = user_manager.create_user('admin', 'admin123', 'admin')
            if user_id:
                print(f"✅ 管理者ユーザーを作成しました (ID: {user_id})")
            else:
                print("❌ 管理者ユーザーの作成に失敗しました")
                
    except Exception as e:
        print(f"❌ ユーザー作成エラー: {e}")
    
    # テスト用計算履歴を作成
    try:
        from calculation_manager import calculation_manager
        
        # テストデータ
        test_items = [
            {
                'box_id': 1,
                'box_no': 1,
                'material': 'Gold',
                'weight': '10.5g',
                'jewelry_price': 25000
            },
            {
                'box_id': 1,
                'box_no': 2,
                'material': 'Silver',
                'weight': '15.2g',
                'jewelry_price': 8000
            },
            {
                'box_id': 2,
                'box_no': 1,
                'material': 'Platinum',
                'weight': '5.8g',
                'jewelry_price': 45000
            }
        ]
        
        test_results = {
            'total_value': sum(item['jewelry_price'] for item in test_items),
            'item_count': len(test_items)
        }
        
        # 管理者の計算履歴として保存
        history_id = calculation_manager.save_calculation(
            user_id=1,
            calculation_name="テスト計算 - 箱番号別",
            item_data=test_items,
            calculation_results=test_results
        )
        
        if history_id:
            print(f"✅ テスト計算履歴を作成しました (ID: {history_id})")
        else:
            print("⚠️ テスト計算履歴の作成をスキップしました")
            
    except Exception as e:
        print(f"⚠️ テスト履歴作成エラー: {e}")
    
    print("✅ ローカルデータベース初期化完了")

if __name__ == "__main__":
    init_database()