from flask import redirect, request, make_response, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask import Flask, render_template
from data import db_session, objects, users
from flask_restful import abort, Api
import os
from resources import objects_resorce, users_resource
from algorithms.password_algorithms import chek_password_combination
from algorithms.phone_number_algorithms import check_phone
import logging
from forms import RegisterForm, LoginForm, ObjectsForm, SortAscending
from forms import SortDescending, EditProfileForm, FindObjectForm, ConfirmPasswordForm

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'DinoTradeTheBest123_secret_key'
api = Api(app)
ALLOWED_TYPES = ['jpg', 'png', 'jpeg', 'gif']
login_manager = LoginManager()
login_manager.init_app(app)
UPLOAD_FOLDER = os.getcwd() + '/static/img'
files = []
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def return_date(user):
    months = {
        1: 'января',
        2: 'февраля',
        3: 'марта',
        4: 'апреля',
        5: 'мая',
        6: 'июня',
        7: 'июля',
        8: 'августа',
        9: 'сентября',
        10: 'октября',
        11: 'ноября',
        12: 'декабря'
    }
    return f'{user.created_date.date().day} {months[user.created_date.date().month]}' \
           f' {user.created_date.date().year} года'


def log():
    logging.info('Info')
    logging.warning('Warning')
    logging.error('Error')
    logging.critical('Critical or Fatal')


@login_manager.user_loader
def load_user(user_id):
    sessions = db_session.create_session()
    return sessions.query(users.User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def open_file(id, type):
    file = request.files['file']
    if file.filename.split('.')[-1] not in ALLOWED_TYPES:
        return False, False
    if type == 'avatar':
        path_of_folder = '/'.join(UPLOAD_FOLDER.split('\\')) + '/avatar_' + str(id) + '/'
        try:
            os.mkdir(path_of_folder)
        except FileExistsError:
            pass
        filename = path_of_folder + file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    if type == 'object':
        path_of_folder = '/'.join(UPLOAD_FOLDER.split('\\')) + '/object_' + str(id) + '/'
        try:
            os.mkdir(path_of_folder)
        except FileExistsError:
            pass
        filename = path_of_folder + file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return file, '../' + '/'.join(filename.split('/')[-4:])


@app.route('/object_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def object_delete(id):
    sessions = db_session.create_session()
    obj = sessions.query(objects.Object).filter(
        objects.Object.id == id).first()
    if obj:
        sessions.delete(obj)
        sessions.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/edit_object/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_obj(id):
    form = ObjectsForm()
    if request.method == "GET":
        sessions = db_session.create_session()
        obj = sessions.query(objects.Object).filter(objects.Object.id == id).first()
        if obj:
            form.name.data = obj.name
            form.price.data = obj.price
            form.description.data = obj.description
            form.category.data = obj.category
            form.sold.data = obj.sold
        else:
            abort(404)
    if form.validate_on_submit():
        sessions = db_session.create_session()
        obj = sessions.query(objects.Object).filter(objects.Object.id == id).first()
        if obj:
            obj.name = form.name.data
            if form.price.data > 10000000000:
                return render_template('add_objects.html',
                                       title='Новое объявление',
                                       form=form,
                                       files=files,
                                       id=None, incor_ln='Мы не можем брать ответственность'
                                                         ' за столь серьёзную сделку')
            else:
                obj.price = form.price.data
            obj.description = form.description.data
            obj.category = form.category.data
            obj.sold = form.sold.data
            sessions.commit()
            return redirect("/")
        else:
            abort(404)
    return render_template('add_objects.html', title='Редактирование объекта', form=form, id=id)


@app.route('/change_avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    if request.method == 'POST':
        session = db_session.create_session()
        filename = open_file(current_user.id, 'avatar')
        if not filename[0]:
            files = current_user.avatar
            return render_template('change_avatar.html', title='Смена аватарки', files=files)
        current_user.avatar = '../' + '/'.join(filename.split('/')[-4:])
        session.merge(current_user)
        session.commit()
    files = current_user.avatar
    return render_template('change_avatar.html', title='Смена аватарки', files=files)


@app.route('/users_list')
@login_required
def users_list():
    sessions = db_session.create_session()
    users_list = sessions.query(users.User).all()
    return render_template('users_list.html',
                           users_list=users_list,
                           title='Список всех пользователей')


@app.route('/profile/<int:id>')
def profile(id):
    sessions = db_session.create_session()
    user = sessions.query(users.User).filter(users.User.id == id).first()
    not_sold_objs = sessions.query(objects.Object).filter(objects.Object.sold == 0,
                                                          objects.Object.user_id == user.id)
    sold_objs = sessions.query(objects.Object).filter(objects.Object.sold == 1,
                                                      objects.Object.user_id == user.id)
    if request.method == 'POST':
        session = db_session.create_session()
        filename = open_file(current_user.id, 'avatar')
        user.avatar = '../' + '/'.join(filename.split('/')[-4:])
        session.merge(user)
        session.commit()
    files = user.avatar
    if str(user.objects) == '[]':
        kolvo = 0
    else:
        kolvo = len(str(user.objects).split('|, '))
    return render_template('profile_page.html', kolvo=kolvo, title=user.name,
                           files=files, id=id, user=user,
                           not_sold_objs=not_sold_objs,
                           sold_objs=sold_objs,
                           date=return_date(user))


@app.route('/confirm_password/<int:id>', methods=['GET', 'POST'])
@login_required
def confirm_password(id):
    form = ConfirmPasswordForm()
    sessions = db_session.create_session()
    new = sessions.query(users.User).filter(users.User.id == id).first()
    if form.validate_on_submit():
        if form.password.data == new.password:
            return redirect(f'/edit_profile/{new.id}')
        else:
            return render_template('confirm_password.html',
                                   message='Неправильный пароль',
                                   title='Подтверждение пароля',
                                   form=form)
    return render_template('confirm_password.html',
                           title='Подтверждение пароля',
                           form=form)


@app.route('/obj/<int:id>', methods=['GET', 'POST'])
def show_obj(id):
    session = db_session.create_session()
    obj = session.query(objects.Object).filter(objects.Object.id == id).first()
    if request.method == 'POST':
        file, filename = open_file(id, 'object')
        if not file:
            files = obj.pictures.split()
            return render_template('object_page.html', files=files,
                                   author=obj.user,
                                   object=obj,
                                   title=f'Объявление {obj.name}',
                                   date=return_date(obj.user))
        if obj:
            if filename not in obj.pictures:
                obj.pictures = str(obj.pictures) + ' ' + filename + ' '
                session.merge(obj)
                session.commit()
    files = obj.pictures.split()
    return render_template('object_page.html', files=files,
                           author=obj.user,
                           object=obj,
                           title=f'Объявление {obj.name}',
                           date=return_date(obj.user))


@app.route('/object_delete_photos/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_photos(id):
    session = db_session.create_session()
    obj = session.query(objects.Object).filter(objects.Object.id == id).first()
    obj.pictures = ' '
    session.commit()
    return redirect(f'/obj/{id}')


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
            if not chek_password_combination(form.new_password.data):
                return render_template('edit_profile.html',
                                       form=form, title='Регистрация',
                                       pass_message="Слишком слабый пароль")
            if form.new_password.data != form.new_password_again.data:
                return render_template('edit_profile.html', name=current_user.name,
                                       email=current_user.email,
                                       password=current_user.password, town=current_user.town,
                                       phone=current_user.phone, message='Пароли не совпадают',
                                       title='Редактирование профиля', form=form)
            if not check_phone(form.new_phone.data)[0]:
                return render_template('edit_profile.html',
                                       form=form, title='Регистрация',
                                       phone_message=check_phone(form.new_phone.data)[1])
            if sessions.query(users.User).filter(users.User.email == form.new_email.data,
                                                 form.new_email.data != current_user.email
                                                 ).first():
                return render_template('edit_profile.html',
                                       form=form, title='Регистрация',
                                       email_message="Пользователь с такой почтой уже существует")
            else:
                new.name = form.new_name.data
                new.email = form.new_email.data
                new.password = form.new_password.data
                new.town = form.new_town.data
                new.phone = form.new_phone.data
                sessions.commit()
                return redirect(f'/profile/{current_user.id}')
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
        obj.name = form.name.data.lower()
        obj.name_for_find = form.name.data.lower()
        if form.price.data > 10000000000:
            return render_template('add_objects.html',
                                   title='Новое объявление',
                                   form=form,
                                   files=files,
                                   id=None, incor_ln='Мы не можем брать ответственность'
                                                     ' за столь серьёзную сделку')
        else:
            obj.price = form.price.data
        obj.description = form.description.data
        obj.category = form.category.data
        obj.sold = form.sold.data
        current_user.objects.append(obj)
        sessions.merge(current_user)
        sessions.commit()
        return redirect('/')
    return render_template('add_objects.html',
                           title='Новое объявление',
                           form=form,
                           files=files,
                           id=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sessions = db_session.create_session()
        user = sessions.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.password == form.password.data:
            if user.block:
                return render_template('login.html',
                                       message='Ваша страница заблокирована'
                                               ' за нарушение правил сайта.',
                                       title='Вход', form=form)
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль',
                               title='Вход', form=form)
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/block/<int:id>')
def block(id):
    session = db_session.create_session()
    user = session.query(users.User).filter(users.User.id == id).first()
    user.block = True
    session.merge(current_user)
    session.commit()
    return redirect('/')


@app.route('/unblock/<int:id>')
def unblock(id):
    session = db_session.create_session()
    user = session.query(users.User).filter(users.User.id == id).first()
    user.block = False
    session.merge(current_user)
    session.commit()
    return redirect('/')


@app.route('/promote/<int:id>')
def promote(id):
    session = db_session.create_session()
    user = session.query(users.User).filter(users.User.id == id).first()
    user.admin = 1
    session.merge(current_user)
    session.commit()
    return redirect('/')


@app.route('/drop/<int:id>')
def drop(id):
    session = db_session.create_session()
    user = session.query(users.User).filter(users.User.id == id).first()
    user.admin = 0
    session.merge(current_user)
    session.commit()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if not chek_password_combination(form.password.data):
            return render_template('register.html',
                                   form=form, title='Регистрация',
                                   pass_message="Слишком слабый пароль")
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form, title='Регистрация',
                                   pass_message="Пароли не совпадают")
        if not check_phone(form.phone.data)[0]:
            return render_template('register.html',
                                   form=form, title='Регистрация',
                                   phone_message=check_phone(form.phone.data)[1])
        sessions = db_session.create_session()
        if sessions.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form, title='Регистрация',
                                   email_message="Пользователь с такой почтой уже существует")
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
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/<category>', methods=['GET', 'POST'])
def main_page(category='Всекатегории'):
    form = FindObjectForm()
    sort_asc_form = SortAscending()
    sort_desc_form = SortDescending()
    sessions = db_session.create_session()
    what_we_want_to_find = ''
    if sort_desc_form.sort_descending.data:
        if category != 'Всекатегории':
            objs = sessions.query(objects.Object).filter(objects.Object.sold == 0,
                                                         objects.Object.category == category)\
                .order_by(
                objects.Object.price.desc())
        else:
            objs = sessions.query(objects.Object).filter(objects.Object.sold == 0).order_by(
                objects.Object.price.desc())
        return render_template('main_page.html', category=category, current_user=current_user,
                               title='DinoTrade', objects=objs, form=form,
                               sort_asc_form=sort_asc_form, sort_desc_form=sort_desc_form,
                               name='', find=False)
    if sort_asc_form.sort_ascending.data:
        if category != 'Всекатегории':
            objs = sessions.query(objects.Object).filter(objects.Object.sold == 0,
                                                         objects.Object.category == category)\
                .order_by(objects.Object.price)
        else:
            objs = sessions.query(objects.Object).filter(objects.Object.sold == 0).order_by(
                objects.Object.price)
        return render_template('main_page.html', category=category, current_user=current_user,
                               title='DinoTrade', objects=objs, form=form,
                               sort_asc_form=sort_asc_form, sort_desc_form=sort_desc_form,
                               name='', find=False)
    if form.find_line.data:
        what_we_want_to_find = form.find_line.data
    if request.method == 'GET':
        if category != 'Всекатегории':
            objs = sessions.query(objects.Object).filter(objects.Object.sold == 0,
                                                         objects.Object.category == category)
        else:
            objs = sessions.query(objects.Object).filter(objects.Object.sold == 0)
        return render_template('main_page.html', category=category, current_user=current_user,
                               title='DinoTrade', objects=objs, form=form,
                               sort_asc_form=sort_asc_form, sort_desc_form=sort_desc_form,
                               name='', find=False)
    if form.validate_on_submit():
        objs = sessions.query(objects.Object).filter(
            objects.Object.name_for_find.like(
                f'%{what_we_want_to_find.lower()}%'), objects.Object.sold == 0)
        return render_template('main_page.html',
                               category=category,
                               current_user=current_user,
                               title='DinoTrade', sort_asc_form=sort_asc_form,
                               sort_desc_form=sort_desc_form,
                               objects=objs, form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    api.add_resource(objects_resorce.ObjectsListResource, '/api/v0.1/objects')
    api.add_resource(objects_resorce.ObjResource, '/api/v0.1/objects/<int:obj_id>')
    # ------------------------------------------------
    api.add_resource(users_resource.UsersListResource, '/api/v0.1/users')
    api.add_resource(users_resource.UsersResource, '/api/v0.1/users/<int:user_id>')
    app.run(port=8080, host='127.0.0.1')
    # log()
