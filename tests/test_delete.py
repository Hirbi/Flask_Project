from requests import get, post, delete
import pprint


print('-' * 100)
pprint.pprint(delete('http://localhost:8080/api/v0.1/users/3').json())
# запрос на удаление пользователя с id = 3
print('|' * 100)
pprint.pprint(delete('http://localhost:8080/api/v0.1/objects/14').json())
# корректный запрос на удаление объекта с id = 14

