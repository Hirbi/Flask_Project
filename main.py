from flask import Flask, render_template, redirect, request, make_response, session, abort, jsonify
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, FileField
from wtforms.validators import DataRequired
from flask import Flask, render_template
from data import db_session, objects, users
from werkzeug.utils import secure_filename
import datetime
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'asdads_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
UPLOAD_FOLDER = os.getcwd() + '/static/img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
files = []
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    sessions = db_session.create_session()
    return sessions.query(users.User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


class RegisterForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    town = StringField('Город', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ObjectsForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class EditProfileForm(FlaskForm):
    new_name = StringField('Новое имя')
    new_email = StringField("Новая почта")
    new_password = StringField('Новый пароль')
    new_password_again = StringField('Подтвердите новый пароль')
    new_town = StringField('Новый город')
    new_phone = StringField('Новый телефон')
    submit = SubmitField('Подтвердить изменения')


@app.route('/profile')
@login_required
def profile():
    if str(current_user.objects) == '[]':
        kolvo = 0
    else:
        kolvo = len(str(current_user.objects).split('|, '))
    return render_template('profile_page.html', kolvo=kolvo, title=current_user.name)


@app.route('/obj/<int:id>', methods=['GET', 'POST'])
def show_obj(id):
    session = db_session.create_session()
    obj = session.query(objects.Object).filter(objects.Object.id == id).first()
    if request.method == 'POST':
        file = request.files['file']
        filename = '/'.join(UPLOAD_FOLDER.split('\\')) + '/' + str(id) + '_' + file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if obj:
            if '../static/img/' + str(id) + '_' + file.filename not in obj.pictures:
                obj.pictures = str(obj.pictures) + ' ' + '../static/img/' + str(
                    id) + '_' + file.filename
                session.merge(obj)
                session.commit()
            print(file.filename)
            files = obj.pictures.split()
            print(files)
            return render_template('object_page.html', files=files)
    files = obj.pictures.split()
    return render_template('object_page.html', files=files)


@app.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    if str(current_user.objects) == '[]':
        kolvo = 0
    else:
        kolvo = len(str(current_user.objects).split('|, '))
    form = EditProfileForm()
    if request.method == 'GET':
        sessions = db_session.create_session()
        new = sessions.query(users.User).filter(users.User.id == id).first()
        if new:
            form.new_name.data = new.name
            form.new_email.data = new.email
            form.new_password.data = new.password
            form.new_town.data = new.town
            form.new_phone.data = new.phone
    if form.validate_on_submit():
        sessions = db_session.create_session()
        new = sessions.query(users.User).filter(users.User.id == id).first()
        if new:
            new.name = form.new_name.data
            new.email = form.new_email.data
            new.password = form.new_password.data
            new.password_again = form.new_password_again.data
            new.town = form.new_town.data
            new.phone = form.new_phone.data
            if new.password != new.password_again:
                return render_template('edit_profile.html', name=current_user.name,
                                       email=current_user.email,
                                       password=current_user.password, town=current_user.town,
                                       phone=current_user.phone, message='Пароли не совпадают',
                                       title='Редактирование профиля', form=form)
            else:
                sessions.commit()
                return redirect('/profile')
        else:
            abort(404)
    return render_template('edit_profile.html', name=current_user.name, email=current_user.email,
                           password=current_user.password, town=current_user.town,
                           phone=current_user.phone,
                           kolvo=kolvo, title='Редактирование профиля', form=form)


@app.route('/add_obj', methods=['GET', 'POST'])
@login_required
def add_obj():
    form = ObjectsForm()
    if form.validate_on_submit():
        sessions = db_session.create_session()
        obj = objects.Object()
        obj.name = form.name.data
        obj.description = form.description.data
        current_user.objects.append(obj)
        sessions.merge(current_user)
        sessions.commit()
        return redirect('/')
    return render_template('add_objects.html', title='Добавление новости', form=form, files=files)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sessions = db_session.create_session()
        user = sessions.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают")
        sessions = db_session.create_session()
        if sessions.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            town=form.town.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        sessions.add(user)
        sessions.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/')
@app.route('/index')
def main_page():
    return render_template('main_page.html', current_user=current_user, title='TradeHub')


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    app.run(port=8080, host='127.0.0.1')
