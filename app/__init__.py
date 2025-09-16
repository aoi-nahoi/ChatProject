from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # 環境変数から設定を取得、デフォルト値も設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')
    
    # データベースURIの設定（PostgreSQL優先、SQLiteはフォールバック）
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Renderなどの本番環境用（PostgreSQL）
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # 開発環境用（PostgreSQL）
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '5432')
        db_name = os.environ.get('DB_NAME', 'chatproject')
        db_user = os.environ.get('DB_USER', 'postgres')
        db_password = os.environ.get('DB_PASSWORD', 'password')
        
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app,db)

    login_manager.init_app(app)
    login_manager.login_view = 'app.login'
    
    csrf.init_app(app)

    from app.views import bp
    app.register_blueprint(bp)

    return app
