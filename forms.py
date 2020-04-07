from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms import IntegerField, RadioField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=15)])
    town = StringField('Город', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ObjectsForm(FlaskForm):
    categories_arr = [('Одежда', 'Одежда'), ('Техника', 'Техника'), ('Мебель', 'Мебель'),
                      ('Животные', 'Животные'), ('Другое', 'Другое')]
    # список с категориями который работает НЕПОНЯТНО НО РАБОТАЕТ
    name = StringField('Название', validators=[DataRequired()])
    category = RadioField('Выберите категорию товара', choices=categories_arr,
                          validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    sold = BooleanField('Продано')
    submit = SubmitField('Сохранить')


class SortAscending(FlaskForm):
    sort_ascending = SubmitField('Возрастанию')

    def __repr__(self):
        return 'Возрастание'


class SortDescending(FlaskForm):
    sort_descending = SubmitField('Убыванию')


class EditProfileForm(FlaskForm):
    new_name = StringField('Новое имя')
    new_email = StringField("Новая почта")
    new_password = StringField('Новый пароль')
    new_password_again = StringField('Подтвердите новый пароль')
    new_town = StringField('Новый город')
    new_phone = StringField('Новый телефон')
    submit = SubmitField('Подтвердить изменения')


class FindObjectForm(FlaskForm):
    find_line = StringField('Поиск по названию', validators=[DataRequired()])
    find_button = SubmitField('Найти')


class ConfirmPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
