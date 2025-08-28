from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Message
from .forms import LoginForm, RegisterForm, MessageForm, UserForm
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, and_

bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f'Logged in successfully! Welcome, {current_user.username}', 'success')
                print(current_user.is_authenticated)
                return redirect(url_for('app.index'))
            else:
                flash('Invalid password.')
                return redirect(url_for('app.login'))
        else:
            flash('The email adress is not registered.')
            return redirect(url_for('app.login'))
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        #ユーザー名やメールアドレスが既に存在するかを確認
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('app.register'))
        
        email = User.query.filter_by(email=form.email.data).first()
        if email:
            flash('Email already registered. Please use a different one.')
            return redirect(url_for('app.register'))
        
        #パスワードをハッシュ化して新しいユーザーを作成
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            hobby=form.hobby.data
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.')
        return redirect(url_for('app.login'))
    return render_template('register.html',form=form)

@bp.route('/')
@login_required
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@bp.route('/chat', methods=['GET', 'POST'])
@bp.route('/chat/<int:to_>', methods=['GET', 'POST'])
@login_required
def chat(to_=None):
    form = MessageForm()
    messages = []
    
    # to_パラメータがある場合、セッションに保存
    if to_:
        session['to_'] = to_
        print(f"Debug: Path parameter 'to_' = {to_}, saved to session")
    
    # URLクエリパラメータからto_を取得してセッションに保存
    if request.args.get('to'):
        session['to_'] = int(request.args.get('to'))
        print(f"Debug: Query parameter 'to' = {request.args.get('to')}, saved to session")
    
    print(f"Debug: Current session 'to_' = {session.get('to_', 'Not set')}")
    
    # セッションにto_が保存されている場合、メッセージを取得
    if 'to_' in session:
        print(f"Debug: Session 'to_' = {session['to_']}")
        print(f"Debug: Current user ID = {current_user.id}")
        
        # データベース内の全メッセージを確認（デバッグ用）
        all_messages = Message.query.all()
        print(f"Debug: Total messages in database: {len(all_messages)}")
        for msg in all_messages:
            print(f"Debug: All messages - ID: {msg.id}, from: {msg.from_}, to: {msg.to_}, body: '{msg.body}'")
        
        # 送信者と受信者の間のメッセージを取得
        messages = Message.query.filter(
            or_(
                and_(
                    Message.from_ == current_user.id,
                    Message.to_ == session['to_']
                ),
                and_(
                    Message.from_ == session['to_'],
                    Message.to_ == current_user.id
                )
            )
        ).order_by(Message.timestanp).all()
        
        # メッセージに日時情報を追加
        from datetime import datetime, date, timedelta
        today = date.today()
        yesterday = today - timedelta(days=1)
        current_year = today.year
        
        for message in messages:
            if message.timestanp:
                message_date = message.timestanp.date()
                message.is_today = message_date == today
                message.is_yesterday = message_date == yesterday
                message.is_this_year = message_date.year == current_year
        
        print(f"Debug: Found {len(messages)} messages between users")
        for msg in messages:
            print(f"Debug: Filtered messages - ID: {msg.id}, from: {msg.from_}, to: {msg.to_}, body: '{msg.body}'")
        
        if form.validate_on_submit():
            print(f"Debug: Form submitted with message: '{form.message.data}'")
            
            # メッセージの保存
            message = Message(
                body=form.message.data,
                from_=current_user.id,
                to_=session['to_']
            )
            db.session.add(message)
            db.session.commit()
            
            print(f"Debug: Message saved with ID: {message.id}")
            print(f"Debug: Saved message - from: {message.from_}, to: {message.to_}, body: '{message.body}'")
            
            # メッセージ送信後、最新のメッセージを再取得
            messages = Message.query.filter(
                or_(
                    and_(
                        Message.from_ == current_user.id,
                        Message.to_ == session['to_']
                    ),
                    and_(
                        Message.from_ == session['to_'],
                        Message.to_ == current_user.id
                    )
                )
            ).order_by(Message.timestanp).all()
            
            # 再取得したメッセージにも日時情報を追加
            for message in messages:
                if message.timestanp:
                    message_date = message.timestanp.date()
                    message.is_today = message_date == today
                    message.is_yesterday = message_date == yesterday
                    message.is_this_year = message_date.year == current_year
            
            print(f"Debug: After sending, found {len(messages)} messages")
            for msg in messages:
                print(f"Debug: After sending - Message {msg.id}: from={msg.from_}, to={msg.to_}, body='{msg.body}'")
            
            # フォームをクリア
            form.message.data = ''
            
            # 成功メッセージを表示
            flash('メッセージを送信しました！', 'success')
            
            # 同じチャットページにリダイレクト（URLパラメータを保持）
            return redirect(url_for('app.chat', to_=session['to_']))
        else:
            print(f"Debug: Form validation failed: {form.errors}")
            print(f"Debug: Form data: {form.data}")
            print(f"Debug: Form is_submitted: {form.is_submitted()}")
            print(f"Debug: Form validate_on_submit: {form.validate_on_submit()}")
    else:
        print("Debug: No 'to_' in session")
    
    # チャット相手の情報を取得
    chat_user = None
    if 'to_' in session:
        chat_user = User.query.get(session['to_'])
    
    return render_template('chat.html', form=form, messages=messages, chat_user=chat_user)

@bp.route('/user/<int:user_id>/update', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = generate_password_hash(form.password.data)
        user.hobby = form.hobby.data
        db.session.commit()
        flash('Your info has been updated!', 'success')
        return redirect(url_for('app.index'))
    
    return render_template('user.html', form=form, user=user)

@bp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)