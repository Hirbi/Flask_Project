import pprint
from requests import post
import datetime

print('-' * 100)
pprint.pprint(post('http://localhost:8080/api/v0.1/users', json={'id': 11,
                                                                 'name': 'Hirb',
                                                                 'phone': '89209111334',
                                                                 'email': 'hirbus@gmail.com',
                                                                 'town': 'Москва',
                                                                 'password': '123asd123',
                                                                 'created_date': '',
                                                                 'block': 0
                                                                    }).json())
