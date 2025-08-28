# ChatProject - チャットアプリケーション

## 概要
ChatProjectは、ユーザー間でリアルタイムチャットができるWebアプリケーションです。ユーザー登録・認証機能、プロフィール管理、1対1のメッセージング機能を提供します。

## 主な機能

### 🔐 ユーザー認証・管理
- ユーザー登録（ユーザー名、メールアドレス、パスワード、趣味）
- ログイン・ログアウト機能
- パスワードハッシュ化によるセキュリティ
- ユーザープロフィールの編集・更新

### 💬 チャット機能
- 1対1のプライベートメッセージング
- リアルタイムメッセージ送受信
- チャット履歴の保存・表示
- セッション管理によるチャット相手の保持

### 👥 ユーザー管理
- 全ユーザー一覧の表示
- 趣味によるユーザー分類（アニメ、スポーツ、音楽、ゲーム）
- ユーザープロフィールの閲覧

## 技術スタック

### バックエンド
- **Python 3.x** - メイン言語
- **Flask** - Webフレームワーク
- **Flask-SQLAlchemy** - ORM（Object-Relational Mapping）
- **Flask-Migrate** - データベースマイグレーション
- **Flask-Login** - ユーザー認証管理
- **Flask-WTF** - フォーム処理・CSRF保護
- **Werkzeug** - パスワードハッシュ化

### データベース
- **SQLite** - 軽量データベース
- **Alembic** - データベースマイグレーション管理

### フロントエンド
- **HTML5** - マークアップ
- **CSS3** - スタイリング
- **Jinja2** - テンプレートエンジン

### セキュリティ
- **CSRF保護** - クロスサイトリクエストフォージェリ対策
- **パスワードハッシュ化** - PBKDF2-SHA256
- **セッション管理** - ユーザー認証状態の管理

## プロジェクト構造

```
ChatProject/
├── app/                          # メインアプリケーションディレクトリ
│   ├── __init__.py              # Flaskアプリケーションの初期化
│   ├── models.py                # データベースモデル（User, Message）
│   ├── views.py                 # ルート・ビュー関数
│   ├── forms.py                 # フォームクラス
│   ├── app.db                   # SQLiteデータベースファイル
│   ├── static/                  # 静的ファイル
│   │   ├── chat.css            # チャット画面用スタイル
│   │   ├── style.css           # メインスタイル
│   │   └── top-fixed.css       # トップ固定用スタイル
│   └── templates/               # HTMLテンプレート
│       ├── base.html           # ベーステンプレート
│       ├── index.html          # ホーム画面
│       ├── login.html          # ログイン画面
│       ├── register.html       # ユーザー登録画面
│       ├── chat.html           # チャット画面
│       └── user.html           # ユーザー管理画面
├── migrations/                   # データベースマイグレーションファイル
│   ├── alembic.ini             # Alembic設定ファイル
│   ├── env.py                  # マイグレーション環境設定
│   └── versions/               # マイグレーションバージョンファイル
├── main.py                      # アプリケーション起動ファイル
└── README.md                    # このファイル
```

## データベース設計

### User テーブル
- `id`: 主キー（整数）
- `username`: ユーザー名（一意）
- `email`: メールアドレス（一意）
- `password`: ハッシュ化されたパスワード
- `hobby`: 趣味（アニメ、スポーツ、音楽、ゲーム）

### Message テーブル
- `id`: 主キー（整数）
- `from_`: 送信者ID（外部キー）
- `to_`: 受信者ID（外部キー）
- `body`: メッセージ内容
- `timestanp`: 送信日時

## セットアップ・インストール

### 前提条件
- Python 3.7以上
- pip（Pythonパッケージマネージャー）

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd ChatProject
```

### 2. 仮想環境の作成・有効化
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 依存関係のインストール
```bash
pip install flask
pip install flask-sqlalchemy
pip install flask-migrate
pip install flask-login
pip install flask-wtf
pip install werkzeug
```

### 4. データベースの初期化
```bash
# データベースの作成
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 起動方法

### 開発サーバーの起動
```bash
python main.py
```

または

```bash
flask run
```

### アクセス
ブラウザで `http://localhost:5000` にアクセスしてください。

## 使用方法

### 1. ユーザー登録
- `/register` にアクセス
- ユーザー名、メールアドレス、パスワード、趣味を入力
- 登録完了後、ログイン画面にリダイレクト

### 2. ログイン
- `/login` にアクセス
- 登録済みのメールアドレスとパスワードでログイン

### 3. チャット
- ホーム画面でチャットしたいユーザーを選択
- チャット画面でメッセージの送受信
- リアルタイムでメッセージが表示・保存される

### 4. プロフィール管理
- ユーザー画面でプロフィールの編集・更新
- パスワードの変更も可能

## 環境変数・設定

### 必須設定
- `SECRET_KEY`: セッション暗号化用の秘密鍵
- `SQLALCHEMY_DATABASE_URI`: データベース接続URI

### 推奨設定
- `FLASK_ENV`: 環境設定（development/production）
- `DEBUG`: デバッグモードの有効/無効

## 開発・デバッグ

### ログ出力
アプリケーションには詳細なデバッグログが含まれており、チャット機能の動作確認が可能です。

### データベース操作
```bash
# マイグレーションの作成
flask db migrate -m "Description of changes"

# マイグレーションの適用
flask db upgrade

# マイグレーション履歴の確認
flask db history
```

## セキュリティ機能

- **CSRF保護**: すべてのフォームにCSRFトークンを実装
- **パスワードハッシュ化**: PBKDF2-SHA256アルゴリズムを使用
- **セッション管理**: 安全なユーザー認証状態の管理
- **入力検証**: フォームデータの適切な検証

## 今後の拡張予定

- リアルタイム通信（WebSocket）
- グループチャット機能
- ファイル添付機能
- プッシュ通知
- モバイルアプリ対応

## トラブルシューティング

### よくある問題

1. **データベースエラー**
   - マイグレーションが正しく適用されているか確認
   - `flask db upgrade` を実行

2. **ログインできない**
   - ユーザーが正しく登録されているか確認
   - パスワードが正しいか確認

3. **チャットが表示されない**
   - セッションにチャット相手が設定されているか確認
   - データベースにメッセージが保存されているか確認

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

バグレポートや機能リクエスト、プルリクエストを歓迎します。

## 連絡先

プロジェクトに関する質問や提案がある場合は、イシューを作成してください。
