from requests import get, post, delete
import pprint


pprint.pprint(get('http://dinotrade.herokuapp.com/api/v0.1/users').json())
# запрос на получение всех данных пользоваетелей
print('-' * 100)
pprint.pprint(get('http://dinotrade.herokuapp.com/api/v0.1/users/1').json())
#  запрос получения пользователя с id = 1
print('|' * 200)
pprint.pprint(get('http://dinotrade.herokuapp.com/api/v0.1/objects').json())
# запрос на получение всех данных объектов
print('-' * 100)
pprint.pprint(get('http://dinotrade.herokuapp.com/api/v0.1/objects/21').json())
#  запрос получения объекта с id = 14

