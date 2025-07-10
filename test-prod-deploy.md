# Production Deploy Test

このファイルはProduction環境の自動デプロイ機能をテストするためのものです。

## テスト時刻
2025-07-10

## テスト内容
- GitHub ActionsでのProduction環境自動デプロイ機能の動作確認
- GCP Cloud Runへのデプロイ成功確認
- 権限設定の確認
- 新しいサービスアカウントキーでの認証テスト

## テスト2回目
手動で新しいサービスアカウントキーを設定してテスト実行

## テスト3回目
JSON解析エラーを修正し、正しい形式のキーを設定完了
- 余分な改行を削除
- 完全な1行JSONとして設定

## テスト4回目（最終）
Private key形式エラーを修正し、新しいサービスアカウントキーを生成
- Production環境: private_key_id: de5a8ad5603ac89eafc72f1d26b1a2c1da780cb2
- Development環境: private_key_id: aa448bfd7636926c0d584fe6147f41ebc532ee5f
- 圧縮JSON形式で再設定完了