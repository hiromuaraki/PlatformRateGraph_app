## 📝 概要
例）User登録・ログインAPIを追加しました。

## 🔧 変更内容
- `UserSerializer`, `UserViewSet` を作成
- `/api/users/` `/api/login/` をルーティング追加

## 🧪 動作確認
1. `python manage.py runserver`
2. Postman or curlでAPI動作確認
3. 新規登録・ログイン成功を確認

## ✅ 結果
| API | Method | 結果 |
|------|---------|------|
| `/api/users/` | POST | ✅ 登録成功 |
| `/api/login/` | POST | ✅ トークン発行 |

## 📚 補足
- 認証ライブラリ: `djangorestframework-simplejwt`

## 🔗 関連Issue
close #2
