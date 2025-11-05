## 📝 概要
例）Userモデルを新規作成しました。

## 🔧 変更内容
- Userモデルを作成
- マイグレーション追加
- Adminに登録

## 🧪 動作確認
1. `python manage.py makemigrations && python manage.py migrate`
2. `python manage.py runserver`
3. `/admin/` にアクセスしUserが登録可能であることを確認

## ✅ 結果
- [x] マイグレーション成功
- [x] 管理画面で動作確認済み

## 📚 補足
- 認証関連APIは次PRで追加予定

## 🔗 関連Issue
close #1
