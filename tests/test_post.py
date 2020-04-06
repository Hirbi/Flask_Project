import pprint
from requests import post

pprint.pprint(post('http://localhost:8080/api/v0.1/users', json={'id': 11,
                                                                 'name': 'Hirb',
                                                                 'phone': '89209111334',
                                                                 'email': 'hirbus@gmail.com',
                                                                 'town': 'Москва',
                                                                 'password': '123asd123',
                                                                 'created_date': '',
                                                                 }).json())
print('|' * 100)
pprint.pprint(post('http://localhost:8080/api/v0.1/objects', json={'id': 1,
                                                                   'name': 'РАМАН',
                                                                   'user_id': 1,
                                                                   'price': 120,
                                                                   'description':
                                                                       'Описание объекта',
                                                                   }).json())
