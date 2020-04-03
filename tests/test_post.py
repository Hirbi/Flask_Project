import pprint
from requests import post


print('-' * 100)
pprint.pprint(post('http://localhost:8080/api/v0.1/users', json={'id': 11, 'name': 'Hirb',
                                                                 'phone': '89209111334',
                                                                 'email': 'hirbus@gmail.com',
                                                                 'town': 'Москва',
                                                                 'password': '123asd123',
                                                                 'created_date':
                                                                     '2020-02-28 10:29:36.403707',
                                                                 'block': '0'}).json())
